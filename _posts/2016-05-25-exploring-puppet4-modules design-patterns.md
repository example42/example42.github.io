---
layout: blog
title: Exploring Puppet(4) modules design patterns
---

The enhancements coming with Puppet 4's parser and type system are starting to appear in the modules ecosystem, still the need to preserve backwards compatibility is often slowing authors from fully embracing the powers and the elegance of the new Puppet language.

When example42 announced the 4th generation of its Puppet modules and introduced a complete [control repo](https://github.com/example42/control-repo), we decided to fully embrace Puppet 4 and ignore backwards compatibility.

I, Alessandro, was struggling to find a sane way to put together the possibilities (and limitations) of Tiny Puppet, the structure of a full featured control-repo, and the usage of third party modules when I met, at the last [OSDC](https://www.netways.de/en/events_trainings/osdc/overview/), David.

He talked about a few very design principles for modules that found me in complete agreement, and I'm glad to have him here to describe them in first person:

----
### David here
----

### From theory to practice

Based on these principles I've started to work on some sample **proof of concepts**.

The first attempt was with [Apache](https://github.com/example42/puppet-apache/tree/4.x), here we have a very compact main class with a few general purpose parameters and no resource directly managed:

    class apache (
      # Manage presence
      Variant[Boolean,String] $ensure           = present,

      # The name of the class that manages apache installation. Tiny Puppet is used here by default
      String                  $install_class    = '::apache::install::tp',

      # A single hash to override the module general configuration settings (names, paths...)
      Hash                    $settings         = { },

      # The name of the module to use for tiny puppet data
      String[1]               $data_module      = 'apache',

      # Here follow some useful, module wide, default behaviors.
      # These can be referenced in any module's class or define.

      # If to restart services when changes occur:
      Boolean                 $auto_restart       = true,

      # If to automatically apply default configurations (if present):
      Boolean                 $auto_conf          = false,

      # If to automatically add prerequisites resources (repos, users, packages...) when needed:
      Boolean                 $auto_prerequisites = false,
    ) { ... }

I wanted to reproduce the behavior of the current apache example42 module, adding defines to manage virtual hosts, modules and configuration files.

They were easy and quick to write, also thanks to Tiny Puppet features and the choice to use the main class as the module's general entry point for variables:

    define apache::vhost (
      Variant[Boolean,String] $ensure           = '',
      String[1]               $template         = 'apache/vhost/vhost.conf.erb',
      Hash                    $options          = { },
    ) {
      include ::apache
      tp::conf { "apache::${title}":
        ensure             => pick($ensure, $::apache::ensure),
        base_dir           => 'vhost',
        template           => $template,
        options_hash       => $::apache::options + $options,
        data_module        => $::apache::data_module,
        settings           => $::apache::real_settings,
        config_file_notify => $::apache::service_notify,
      }
    }

Finally I started to add some sample profiles to the module, and also in this case I found out that the whole model was consistent, reusable, and elegant:

    class apache::profile::passenger (
      Variant[Boolean,String]  $ensure    = '',
      Hash                     $options   = { },
      Variant[Undef,String[1]] $template  = undef,
    ) {
      include ::apache
      ::apache::module { 'passenger':
        ensure          => pick($ensure, $::apache::ensure),
        template        => $template,
        options         => $::apache::options + $options,
        package_install => true,
      }
    }

Having a minimal main class and using it as main entry point for all the general module's variables implies that that class can, and should, be included in all the other module's classes and defines.

Having a single core and separated profiles solves one of the typical dilemma of modules' authors: provide functionality vs follow the single point of responsibility pattern.


### Data in modules, the Tiny Puppet way

I continued this exploration with a [Docker](https://github.com/example42/puppet-docker) module, here integration with Tiny Puppet is even deeper, as tp is not only used to configure and install Docker, but also to build Docker images for any application, based on starting images from different Operating Systems.

This is done via the [docker::tp_build](https://github.com/example42/puppet-docker/blob/master/manifests/tp_build.pp) define which is used, for example, in the [builder profile](https://github.com/example42/puppet-docker/blob/master/manifests/profile/builder.pp) which can be applied to any node to convert it to a Docker build system, which can be configured with Hiera data like:

    docker::profile::builder::images:
      apache:
        ensure: present
        conf_hash:
          apache::mysite:
            base_dir: 'conf'
            template: 'profile/apache/sample.conf.erb'
            options:
              ServerName: 'www.example42.com'
              ServerAliases:
                - www.example42.com
                - www.example42.eu
        dir_hash:
          apache::example42.com:
            base_dir: 'data'
            vcsrepo: 'git'
            source: 'https://github.com/example42/example42.github.io'

The above data creates an apache image containing the referred configuration file(s) and data directories. Note that Puppet and Tiny Puppet are NOT installed on the image: tp_build creates the proper Dockerfile for the chosen OS and app and the relevant directories and files on the builder host.

Another small but nice use case of profiles is to provide sample code which can be used for demos, documentation or testing, such, for example, the [::docker::profile::run_examples](https://github.com/example42/puppet-docker/blob/master/manifests/profile/run_examples.pp).

The Docker module uses two different sources for module's data and this needs some more explanations:

    String[1]               $data_module         = 'docker',
    String[1]               $tinydata_module     = 'tinydata',

First of all one concept must be clear, the approach used by Tiny Puppet to get data is not based on Puppet 4's data in modules design. It uses a custom ```tp_lookup``` function that looks for data in yaml files organized according to a hierarchy defined in a hiera.yaml file (it uses Hiera's same syntax and logic but Hiera is not actually used for the lookups, [read here](http://tiny-puppet.com/tinydata.html) for more details).

The tp_lookup function allows the choice of the data module to use, by default Tiny Puppet uses the [tinydata](https://github.com/example42/tinydata) module where common settings for different applications on different OS are defined but in all the Puppet 4 modules shown here, the data_module is the module itself, which contains in its ```data``` directory not only the common settings, already defined in tinydata, but also more data, specific to the module's application.

For example in the [ansible](https://github.com/example42/puppet-ansible) module I started to add all the default Ansible [application options](https://github.com/example42/puppet-ansible/blob/master/data/ansible/default.yaml) and provide a sample ```config_file_template: '[ansible/ansible.cfg.erb](https://github.com/example42/puppet-ansible/blob/master/templates/ansible.cfg.erb)'``` which is automatically added when the ```auto_conf``` option is true.

Note that the ```<%= @options['keyname'] %>``` variables are the result of the merge of users' custom ```$::ansible::options``` and the module's default options shown before.

This follows the **options_hash + default options + [custom] template** pattern described in [this blog post](http://www.example42.com/2014/10/29/reusability-features-every-module-should-have/).

The Docker module is a particular case, as it has also a ```$tinydata_module``` parameter, which defines the data module to use to get info about any application (not Docker) and this data is used to build the relevant images.


### Stack modules

Another experiment is with the [rails](https://github.com/example42/puppet-rails) module.
Here class indirection can give the module remarkable flexibility on what components of a distributed Rails setup should be included by what nodes.

The module is intended not only to manage the installation of Rails but of all the components of a complex multi-node Rails setup. This class is similar to what I defined in the past a [stack module](http://www.example42.com/2014/05/31/rethinking-modules-part-1/): a module included by nodes of different roles that concur to setup the whole Rails stack, each one "activating", using class indirection parameters in the main class, the desired components (classes) of the stack (web server, database, caching server...)

    class rails (
      String    $install_class    = '::rails::install::gem',
      String    $proxy_class      = '',
      String    $app_class        = '',
      String    $db_class         = '',

      String    $deploy_class     = '',
      [...]
    ) {

Here the deploy class can be used to manage different Rails applications, which might be provided as dedicated profiles in the rails or in other modules.

So, bringing on this logic, the module is supposed to be a sort of super-module which not only manages the installation of the components of a distributed Rails architecture, but also the deployment and the configuration of different Rails applications, each one in their one, independent and interoperable, profile classes.

Is this a bad idea as it breaks most of the modules' basic rules? Maybe, or maybe it's simply a different way to define boundaries and responsibilities of Puppet classes.

Note also how having different options for the install class may make the module more complete and feature rich. Check, for example, the different [install classes](https://github.com/example42/puppet-rails/tree/master/manifests/install) currently available on that module.


We have seen some sample modules following the patterns that David has described, they are not complete and may be over simplified. For example I like the *options_hash + template* pattern, and I prefer it over having classes with a huge amount of parameters (up to one for each application configuration entry), so I did these modules with this principle in mind.

Still this is not a requirement.

Once you keep a minimal "just install and do nothing else" approach for the main class (and if you do it, please use install_class indirection) and move into profiles in modules all the customization, typical use cases, opinionated setups, you can actually have endless options. You might even provide in the same module alternative profiles using either an essential options_hash + template approach or one based on multiple (profile class') parameters.

Also the idea of using Tiny Puppet in component modules (originally I considered it mostly as a possible replacement for component modules, to be used in local profiles) has proven to be useful and practical: it saves modules authors from managing a lot of common logic and module data and provides an handy abstraction on application management.

This is the direction that the 4th generation of example42 modules are taking: this time we ABSOLUTELY don't want to follow past errors, trying to write by ourselves most of our modules.

We hope the community of modules' authors will start to write modules following similar design patterns, this would allow us, and everybody, to more easily use third party modules and integrated them in existing Puppet installations.

And, btw, if you want us to write a ```yourmodule::install::tp``` class for your module, just tell us: having the option to install an application also via Tiny Puppet can only be a good thing.
