---
layout: blog
title: Exploring Puppet(4) modules design patterns
---

The enhancements coming with Puppet 4's parser and type system are starting to appear in the modules ecosystem, still the need to preserve backwards compatibility is often slowing authors from fully embracing the powers and the elegance of the new Puppet language.

When example42 announced the 4th generation of its Puppet modules and introduced a complete [control repo](https://github.com/example42/control-repo), we decided to fully embrace Puppet 4 and ignore backwards compatibility.

I, Alessandro, was struggling to find a sane way to put together the possibilities (and limitations) of Tiny Puppet, the structure of a full featured control-repo, and the usage of third party modules when I met, at the last [OSDC](https://www.netways.de/en/events_trainings/osdc/overview/), David.

He talked about new design principles for modules that found me in complete agreement, and I'm glad to have him here to describe them directly:

### Roles, Profiles, and Components

In 2012 Craig Dunn posted the seminal [Roles and Profiles](http://www.craigdunn.org/2012/05/239/) pattern. At that time we all just figured out how to write modules. Craig, and everyone else, were now learning how to apply those modules to increasingly bigger parts of their infrastructure. Fast-forward to today, where roles and profiles are an established pattern, and modules have grown to cover all the edge-cases of that pesky real world. For example, the apache::vhost define has over 130 parameters, while the apache main class can install apache with any of four different MPMs, and provides a fully specialized default configuration. It also turns out that this kind of module provides both too much opinion on configuration, standing in the way of the seasoned apache practitioner, and not enough to be immediately useful to people just needing a web server.

Craig wrote in 2012:

> [...] the profile “Tomcat application stack” is made up of the Tomcat and JDK components, whereas the webserver profile is made up of the httpd, memcache and php components. In Puppet, these lower level components are represented by your modules.

I, David, believe this to be an important part of the pattern, that we all never followed up on: modules need to provide the components - the cogs, and gears - that system engineers can use in their profiles to control their infrastructure, but - from the time before the Roles and Profiles pattern - modules also provided, and still do provide, functionality from a profile's responsibility to be useful. This additional functionality is now standing in the way of fulfilling all the other use-cases, by prescribing certain ways to do things. To solve this I propose a separation of concerns within modules into a component layer and a profile part. The main class and its associated defines in the component layer, implement platform support and do not carry any configuration content at all. All configuration values and policies move into one or more profile classes in the module.

#### Profiles in Modules

Profiles in Modules are opinionated, optional, top-level classes, and defines that address a very specific use-case for consumers of a module. Good examples are "ntp::client::local_broadcast", "ntp::client::unicast" and "ntp::server::local_broadcast", or "apache::reverse_proxy_vhost" and "apache::reverse_proxy_location". The goal here is to cover common use-cases and allow collaboration within the community on best-practice configurations. There are only very few people world-wide who really need to know how to setup and cryptographically secure a local ntp broadcast setup, but everyone would benefit from the added security and reduced bandwidth usage.

Being **opinionated** allows them to move the subject matter forward. Profiles will be written by subject matter experts of the underlying software, and need to match the concepts of that software, and the use-case they are intended to solve. Through this matching, they can speak the language of the consumers, and will be easier to understand. This also serves to say that if a system engineer has an opinion on how something should be configured, they should be encouraged to write, and share, their own profile.

Being **specific** allows them to concentrate on solving the problem, instead of trying to cater to everyone. It is better to have tow things that each solve a problem well than one thing that tries to do everything, but does nothing good.

Being **optional** allows them to control their slice of the system with bold confidence. Profiles can pull all the stops to configure the service optimally for their target use-case. Even more so than site-specific profiles, profiles in modules need to take care that they are composable with profiles from other modules. In their area of responsibility on the other hand, profiles can do everything to maximize their efficiency, and ease of use. This also means that profiles are easily replaceable, when they do not intertwine with the basic necessities of the component layer.

Being **top-level** allows them to expose critical operational knobs to the administrator. This can range from a simple file source/content parameter pair to very high-level, domain-specific use-case specific tunables, like "use X gigabytes of RAM to run this mysql instance." It is very important that profiles do expose the things that are important to their solution, and nothing else, keeping them relevant to the consumer's needs.

Being in the module itself allows them to be shared, refined, and accessed by many. Whether that is just within your own organization, your customers, or the wider open source community, I hope I do not have to explain the benefits here anymore.

This addresses the feature support.

Example:

    # Configure an NTP client to listen to local broadcasts signed by a ntp::server::local_broadcast with the same $keygroup_name.
    # $interface can be used to only bind to a specific network interface
    class ntp::client::local_broadcast(String $keygroup_name = $facts['domain'], String $interface = 'ALL') {
      include ::ntp
      ntp::conf {
        source_template => 'ntp/client/local_broadcast.cfg.erb',
      }
    }

#### Component Layer

The Component Layer is a transparent, mandatory foundation for all consumers of a specific service, or application. This layer aggregates all the platform/distribution specific logic and data, and uses that to take care of the direct management of package installation, service management, and deploying configuration. Should the managed software allows it, it would also be appropriate to install multiple instances on the same node.

Being **mandatory** enables the interaction of multiple different consumers on the same node, and avoids namespace clashes across complete environments, as everyone shares a common language to manage the basics of a thing.

Being **transparent** avoids putting untoward constraints on the component's consumer. The basic layer contains all platform knowledge, but no configuration information, or domain-specific abstractions. It also exposes this platform knowledge for consumption by the profiles, to allow them to be portable, without having to have all that logic themselves. And finally, this means that innovative profiles can still rely on the services of the component layer, as they have full control over the configuration.

Being a **foundation** requires to be broad, stable, well-tested. Being a shared resource brings great responsibilities. Foremost a broad platform support, to cover the component layer's core competency. Then, a good test coverage. Profile authors and direct consumers need assurance that they can rely on the component layer's services across all platforms. As a shared resource, the investment pays off over a bigger number of uses and improved stability for a larger number of systems.

Example:

    # install and configure NTPd
    class ntp(
      Enum[present, absent]  $ensure          = 'present',
      String                 $config_source   = undef,
      String                 $config_content  = undef,
    ) { [...]}

Beyond that, a component should expose information about the capabilities and features of the installed software. A example is which of the many mysql versions is installed, as this has consequences in details of configuration. Doing this allows all the platform- and version-specific niggles to be concentrated in one location. Whenever a profile needs to make a decision on one of those values, confident in their fidelity, without having to fall back to guessing from operating system versions, or similar.


### From theory to practice

Based on these principles just described by David, I (Alessandro) have started to work on some sample **proof of concepts**.

The first attempt was with [Apache](https://github.com/example42/puppet-apache/tree/4.x), here we have a very compact main class with a few general purpose parameters and no resource directly managed:

    class apache (
      # Manage presence
      Variant[Boolean,String] $ensure           = present,

      # The name of the class that manages apache installation. Tiny Puppet is used here by default
      String                  $install_class    = '::apache::install::tp',

      # A **single** hash to override the module general configuration settings for the
      # underlying OS (package names, file paths...)
      Hash                    $settings         = { },

      # The name of the module to use for [tiny puppet] data
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

Is this a bad idea as it breaks the first rule of modules design (Single Responsibility principle)? Maybe, or maybe it's simply a different way to define boundaries and responsibilities of Puppet classes and modules.

Note also how having different options for the install class may make the module more complete and feature rich. Check, for example, the different [install classes](https://github.com/example42/puppet-rails/tree/master/manifests/install) currently available on that module.

We have seen some sample modules following the patterns that David has described, they are not complete and may be over simplified. For example I like the *options_hash + template* pattern, and I prefer it over having classes with a huge amount of parameters (up to one for each application configuration entry), so I did these modules with this principle in mind.

Still this is not a requirement.

Once you keep a minimal "just install and do nothing else" approach for the main class (and if you do it, please use install_class indirection as it would greatly enhance its interoperability) and move into profiles in modules all the customization, typical use cases, opinionated setups, you can actually have endless options. You might even provide in the same module alternative profiles using either an essential options_hash + template approach or one based on multiple (profile class') parameters, for example.

Also the idea of using Tiny Puppet in component modules (originally I considered it mostly as a possible replacement for component modules, to be used in local profiles) has proven to be useful and practical: it saves modules authors from managing a lot of common logic and module data and provides an handy abstraction on application management.

This is the direction that the 4th generation of example42 modules are taking: this time we ABSOLUTELY don't want to follow past errors, trying to write by ourselves most of our modules.

We hope the community of modules' authors will start to write modules following similar design patterns, this would allow us, and everybody, to more easily use third party modules and integrated them in existing Puppet installations.

A good starting point to write modules based on these principles is the module skeleton [here](https://github.com/example42/control-repo/tree/production/skeleton).

To use create a module based on it from example42 [control-repo](https://github.com/example42/control-repo/) you have just to run:

    fab puppet.module_generate

The same control-repo can be used as a reference on how roles, local profiles and profiles in modules can seamlessly work together.

Alessandro Franceschi and David Schmitt
