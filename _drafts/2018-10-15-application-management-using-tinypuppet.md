---
layout: blog
title: Tip of the Week 94 - Custom applications management using Tiny Puppet
---

This weeks tip of the day deals with management of custom application and Puppet.

Usually developers would like to concentrate on their application development and not also write Puppet modules for application deployment and configuration.

Especially when it comes to individual, in-house developed solutions you will find no Puppet module available, so a custom profile or module has to be written.

In this post we are going to show, how we can easily manage custom applications with Tiny Puppet with limited or no Puppet code at all.

* Table of content
{:toc}

## Application deployment using modules

Individual applications need individual modules or profiles.

Developers know about possible configuration flags (e.g. db connectors or feature flags) and how and where to set specific configurations.

They will start with the installation (hopefully `package` resource type) and then use the `file` resource to configure settings. Afterwards they use the `service` resource to ensure that the application is running.

e.g.

    class my_application (
      String[1] $version,
      String[4] $admin_password,
      Boolean   $enable_feature_432 => false,
      Boolean   $enable_feature_876 => true,
    ){
      package { 'my_application':
        ensure => $version,
      }
      file { '/etc/application/app.conf':
        ensure  => file,
        content => template('my_application/app.conf.erb'),
        notify  => Service['my_application'],
        require => Package['my_application'],
      }
      file { '/etc/application/secrets':
        ensure  => file,
        content => "admin:${admin_password}",
        notify  => ['my_application'],
        require => Package['my_application'],
      }
      service { 'my_application':
        ensure => running,
        enable => true,
      }
    }

If multi OS support is needed, the module can get a lot more complex, with a params class or data in module to cope with different paths and names.

Moreover you may need to add fragments of code for each managed file.

All code must be inside either a module or a profile and needs unit and acceptance testing.

When you have multiple applications you will have multiple classes for each of your applications.

Hopefully your application modules do not interfere with any other module which might lead to duplicate resource type declarations.

## Application deployment using a Tiny Puppet profile

Within Tiny Puppet you don't have to bother with developing Puppet code.

Tiny Puppet is an abstraction layer for any application deployment and can fully controllable by hiera data.

Let's migrate the above Puppet code to a profile with Tiny Puppet defines. First we generate a wrapper class (profile), which can be used by all applications:

    class profile::my_application (
      Hash      $install_options = {},
      Hash      $conf_options    = {},
    ){
      if ! empty($install_options) {
        tp::install { 'my_application':
          * => $install_options,  
        }
      }
      if ! empty($conf_options) {
        tp::conf { 'my_application':
          * => $conf_options,
        }
      }
    }

Now we can add the required data to hiera:

    profile::my_application::install_options:
      ensure: '1.1.3'
    profile::my_application::conf_options:
      path: '/etc/application/app.conf'
      template: 'profile/my_application/conf.erb'
      options_hash:
        master: appmaster.prod.mydomain
        listen: 0.0.0.0

In the conf.erb template we can refer to our application configuration options with something like: `master = <%= @options_hash['master'] %>`.

Now any development team just provides a set of YAML data for their application based on a custom template where we can parametrise what we need to change in different environments or servers

## Application deployment using a Tiny Puppet wrapper define

An alternative to the above example, where a profile class is created for each application, can be to write a custom generic wrapper define where the tp::install and tp::conf defines are declared, and a simple class that allows to configure via Hiera data any application.

The generic wrapper could be something like:

    define profile::application (
      Hash      $tp_options_hash = {},
    ){
      if has_key($tp_options_hash, 'install') {
        tp::install { $title:
          * => $tp_options_hash['install'],  
        }
      }
      if has_key($tp_options_hash, 'conf') {
        tp::conf { $title:
          * => $tp_options_hash['conf'],
        }
      }
    }

The class that exposes a parameter to configure the profile::application defines could be as simple as:

    class profile (
      Hash $applications = {},
    ) {

      $applications.each |$k,$v| {
        profile::application { $k:
          * => $v,
        }
      }
    }

This is the only code we would need to write for any application, then we can feed it with data like:

    profile::applications:
      my_application:
        install:
          ensure: '1.1.3'
        conf:
          path: '/etc/application/app.conf'
          template: 'profile/my_application/conf.epp'

## Application deployment using Tiny Puppet and custom Tiny data

We can be even smarter and create tinydata specific for our application, in a custom tinydata module, with custom hierarchy for each application we want to manage (in case we want support for multiple OS):

    vi my_tinydata/data/my_application/hiera.yaml

    ---
    :hierarchy:
      - "%{title}/osfamily/%{osfamily}"
      - "%{title}/default"
      - default

We need a generic (valid for all applications) my_tinydata/data/default.yaml which can have the same contents of the [tinydaya default](https://github.com/example42/tinydata/blob/master/data/default.yaml).

Now we need to create at least a file with application specific data, let's just create the default file, valid for all OS:

    vi my_tinydata/data/my_application/default.yaml

    ---
    my_application::settings:
      package_name: 'my_application'
      service_name: 'my_application'
      config_file_path: '/etc/my_application/app.conf'
      config_dir_path: '/etc/my_application'

These are the minimal settings for having a typical package/service/config file setup, but we can add more options such as:

      log_file_path: '/var/log/my_application.log' # Used by tp log command
      nodaemon_args: '-D' # Optional argument to launch service in forground (useful inside Docker containers)
      validate_cmd: 'my_application -t -f %' # Optional command to check the syntax of the application configuration before restarting my_application service
      repo_package_url: 'https://repo.mydomain/my_application/my_application-release-el-7.noarch.rpm' # Optional Url of the release package which configures my_application Yum/Apt repo (if no release package is available the repo settings can be set via other keys in tinydata)

Give tinydata like this we can configure our application without writing a single line of code. We can just include the `tp` class (here needed just to expose Hiera configurable parameters to manage tp defines, the same can be accomplished with a custom class similar to the profile example before) and write Hiera data like:

    tp::install_hash:
      my_application:
        ensure: '1.1.3'
        data_module: my_tinydata
    tp::conf_hash:
      my_application:
        template: 'profile/my_application/conf.erb'
        options_hash:
          master: appmaster.prod.mydomain
          listen: 0.0.0.0
        data_module: my_tinydata
      my_application::secrets:
        content: ENC[...] # Hiera-eyaml encrypted content
        data_module: my_tinydata

The default value for the data_module parameter is 'tinydata', and for this reason the tp module has  [example42-tinydata](https://github.com/example42/tinydata) as dependency.

Still the data_module can be configured, so we can have a custom local module (here my_tinydata) where we add our own applications data.

Alternatively we could just form the tinydata module and add our applications data to our local version of the module.

## Advantages?

Besides the reduced amount of Puppet code to write, using tp to manage custom applications (when they can be installed via a package) with the relevant tinydata, has the added benefit of automatically configuring the `tp` command, which can be used on a system to check the status of all the applications installed via tp (`tp test [my_application]`) or `tail -f` all theirs logs (`tp log [my_application]`).

We wish everybody fun and success with Tiny Puppet,

Martin Alfke
Alessandro Franceschi
