---
layout: blog
title: Tip of the Week 89 - tp install anything (anywhere), and configure
---

We have talked about Tiny Puppet in this blog more than 3 years ago when introducing the example42 tp module and then again at release 1.0:

- [Introducing Tiny Puppet](https://www.example42.com/2015/01/02/introducing-tiny-puppet/)
- [Preparing for Tiny Puppet 1.0](https://www.example42.com/2015/10/26/preparing-for-tp-1/)
- [Tiny Puppet 1.0](https://www.example42.com/2015/11/18/tp-1-release/)

More recently, we had a Tip of the Week on using the tp command from the cli:

- [Tip of the Week 82 - A few steps to Tiny Puppet on the command line](https://www.example42.com/2018/07/23/a-few-steps-to-tiny-puppet-command-line/)

I think it's time for some updates on Tiny Puppet given that we are at version 2.3.

The module is stable, solid, used in several productions, it provides:

- The user defined types ```tp::install```, ```tp::conf```, ```tp::dir``` to manage any (\*) application

- The ruby command `tp` with actions like ```tp install```, ```tp test```, ```tp log``` to check the status of the applications installed via tp

#### (\* Any application)

The promise of installing any application (and by this we mean, package) on any  (\*\*) OS where Puppet can run is potentially matched.

The difference between potential and real is a matter or more or less present and correct tiny data.

Up to a few days ago the *any* was related to any application for which there's [tinydaya](https://github.com/example42/tinydata/tree/master/data), now, since [version 2.3.0](https://github.com/example42/puppet-tp/commit/c764b7b60727110518c8b3db0cf61aad0aaeff11), tp install defaults to the given title, if a package with that name is installable it tries to install it on the underlying (\*\*) OS, given the needed prerequisites for Windows and MacOS.  

#### On (\*\*) Any OS

By **Any OS** we mean any OS where Puppet can run.

With `tp::install` (`tp install` on cli) we can install any application, even if no tinydata is present, if there's usable tinydata we can configure it with `tp::conf` and `tp::dir`.

### Usage on the cli

On Mac and Windows some module dependencies are needed.

    puppet module install example42-tp

On Mac you need Brew installed and a valid homebrew module with the homonimous package provider:

    puppet module install thekevjames-homebrew
    puppet apply -e "class { homebrew: user => $local_user }"

On Windows you need chocolatey installed:

    puppet module install puppetlabs-chocolatey
    puppet apply -e "include chocolately"

Then, whatever the OS we can install locally the tp command with:

    puppet tp setup

Now you can try to install anything.

On Linux try:

    tp install docker
    tp install elasticsearch
    tp install apache

On Mac install anything brew can install, also via cask:

    tp install opera
    tp install dropdox ...

Usage from cli under windows is Work In Progress.

### Usage in manifests

The tp command might be nice to play around and test the status of apps managed via tp, but it's inside Puppet manifests where the tp defines can give real help in configuring our applications.

In your classes, typically in your profiles to manage a specific application you can manage the package, service, configuration files triple with:

    # Manage package (and relevant repos if needed) and service
    tp::install { 'openssh': }

    # Manage main configuration file
    # (File content can be managed with different params: content, template, source, epp...)
    tp::conf { 'openssh':
      content => $sshd_content,
    }

    # Manage other configuration file (in main configuration directory)
    tp::conf { 'openssh::ssh_config':
      content => $ssh_content,
    }

In order to install the tp command on a node, it's enough to:

    include tp

The tp class is needed and used only for this, and as entrypoint for hiera data for hashes of tp resources.
In this way, for example, you can define what applications to install with data like:

    # We can define an array or an hash of tp installs:
    tp::install_hash:
      - opera
      - dropbox

    # Similarly we can define hashes and things to do with tp install and conf:
    tp::install_hash:
      elasticsearch:
        auto_repo: false
      logstash: {}

    # A bunch of tp::conf resources:
    tp::conf_hash:
      elasticsearch:
        template: profile/elasticsearch/elasticsearch.yml
        options_hash:
          cluster.name: el-1
          index.number_of_shards: 2

      logstash::syslog:
        source: puppet:///modules/logstash/syslog

      logstash::my_app:
        source: puppet:///modules/logstash/my_app

We don't actually recommend to use the `tp` namespace for using tp, it's more handy to use tp defines in profiles, as needed and when needed.


### Custom templates and variables

When using tp::conf to manage the content of a configuration file, we have at disposal, and can interpolate in our epp or erb templates, two very useful variables:

- `$settings` is an hash with the result of the tp_lookup function, which for the given app tries to get usable tinydata. This is useful to manage in the same template cross OS differences, given to file paths and names.

- `$options` or `$options_hash` is currently just the content of the `options_hash` parameter passed to `tp::conf`. You can do with it whatever you want, according to the configured application.

So, your erb template can look in the following fragments from [erb template](https://github.com/example42/puppet-psick/blob/master/templates/mongo/mongod.conf.erb):

    storage:
      dbPath: <%= @settings['data_dir_path'] %>

    net:
      port: <%= @settings['tcp_port'] %>
      bindIp: <%= @options['bindIp'] %>

To have an idea of the available settings, give a look to the [tp::settings Data type](https://github.com/example42/puppet-tp/blob/master/types/settings.pp).


### Generic templates for standard file formats

If we like the idea of having all our configurations as (hiera) data, we can use `tp conf` to manage configurations using generic templates for standard file formats, [like these](https://github.com/example42/puppet-psick/tree/master/templates/generic) from the psick module.

On real life a quick profile to manage (with good hope to work on different OS) redis can looks like this:

    class profile::redis (
      String $ensure   = present,
      Hash $options    = {},
      String $template = 'psick/generic/spaced.erb',
    ) {

      tp::install { 'redis':
        ensure => $ensure,
      }

      tp::conf { 'redis':
        ensure       => $ensure,
        template     => $template,
        options_hash => $options,
      }
    }

With Hiera data as easy as:

    profile::redis::options:
      slaveof: '127.0.0.1 6380'
      port: 6380


### So is tp for me?

It depends on what you need and what you know.

Tiny Puppet manages packages, services, repo configurations, and files whose content is entirely up to you. It doesn't manage any application specific resource.

If you know how to configure your application and want a quick way (probably the quickest) to manage it with Puppet, and know at least Puppet basics, tp is for you.

When tp (and some DIY code) would be better than using a dedicated module from the Forge?

- If don't want to spent time testing a new module, add its dependencies, hoping it does all what you need
- When at the end there's to manage packages, services and files
- When you know exactly how our configuration files must be and want to control how they are generated (from static sources or dynamic templates with custom $options and os related $settings).
- When you don't have to manage application specific resources, which are present in a dedicated module
- When you don't have to manage complex setups for which a good dedicated module would deliver faster results

Is it for you?

    tp install fortune


Alessandro Franceschi
