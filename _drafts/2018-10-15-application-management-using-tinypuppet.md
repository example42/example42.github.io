---
layout: blog
title: Tip of the Week 94 - Application deployment using Tiny Puppet
---

This weeks tip of the day deals with application development and Puppet.
Usually developers would like to concentrate on their application development and not also write Puppet modules for application deployment and configuration.

Especially when it comes to individual, in-house developed solutions you will find no Puppet module available.

We want to show, how the module way differs from the Tiny Puppet way and what benefits we see for application developers by using Tiny Puppet in favor of modules.

* Table of content
{:toc}

## Application deployment using modules

Individual applications need individual modules or profiles.
Developers know about possible configuration flags (e.g. db connectors or feature flags) and how and where to set sepcific configurations.

They will start with the installation (hopefully `package` resource type) and then use the `file` resource to configure settings. Afterwards they use the `service` resource to ensure that the application is running.

e.g.

    class my_application (
      String[1] $version,
      Boolean   $enable_feature_432 => false,
      Boolean   $enable_feature_876 => true,
    ){
      package { 'my_application':
        ensure => $version,
      }
      file { '/etc/application/app.conf':
        ensure  => file,
        content => epp('my_application/app.conf.epp'),
      }
      service { 'my_application':
        ensure => running,
        enable => true,
      }
      File['/etc/application/app.conf']
      ~> Service['my_application']
    }

All code must be inside either a module or a profile and needs unit and acceptance testing.

WHen you have multiple applicatoins you will have multiple modules for each of your applications.

Hopefully your application modules do not interfere with any other module which might lead to duplicate resource type declarations.

## Application deployment using Tiny Puppet

Within Tiny Puppet you don't have to bother with developing Puppet code.
Tiny Puppet is an abstraction layer for any application deployment and is fully controllable by hiera data.

Let's migrate the above Puppet code to Tiny Puppet data usage. First we generate a wrapper class (profile), which can be used by all applications:

    define profile::application (
      Hash      $option_hash,
    ){
      if has_key($option_hash, 'install') {
        tp::install { $title:
          * => $option_hash['install'],  
        }
      }
      if has_key($option_hash, 'conf') {
        tp::conf { $title:
          * => $option_hash['conf'],
        }
      }
    }

Now we add the required data to hiera:

    profile::application::options_hash:
      'my_application':
        'install':
          'ensure': %{lookup('my_application_version')}
          'repo': "https://reposerver.domain.com/%{'::stage')"
        'conf':
          'path': '/etc/application/app.conf'
          'template': 'profile/my_application/conf.epp'

Now any development team just provides a set of YAML data for their application.

We wish everybody fun and success with Tiny Puppet,

Martin Alfke
Alessandro Franceschi
