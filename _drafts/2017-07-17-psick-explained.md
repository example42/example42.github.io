---
layout: blog
title: Tip of the Week 27 - PSICK explained
---

Using PSICK for the very first time confuses people as they are confronted with a highly flexible approach for managing and configuring their infrastructure.
This posting will give you a guidance on how to read, understand and use PSICK.

Normally system administrators strictly follow the approach of writing roles and profiles which consist of lots of Puppet code, describing the infrastructure.
With PSICK one has the possibility of using or adopt a predefined role/profile pattern.

Let's get to the content::

1. why PSICK
1. set up NTP
1. configure SSH
1. manage users

# Why PSICK?

Where do you usually start when working with Puppet?
Do you really want to start from scratch, re-inventing the wheel?
Do you really want to start with an empty control-repository and start coding your implementations?

Why not just take what is already there and adopt it to your needs?
You will very fast recognize that it is far more easy to remove unneeded items instead of writing everything from scratch.

This is the reason why example42 provides the Puppet Systems Infrastructure Construction Kit [PSICK](https://github.com/example42/psick.git) which has many implementations already included.
On most configuration items you only have to provide hiera data which describe your desired setup and your infrastructure.

# Setup NTP

## The classical way

Usually people classify the puppetlabs ntp module:

    class profile::time (
      $servers,
    ){
      class { '::ntp:
        servers => $servers,
      }
    }

The $servers parameter will cause an automatic data binding lookup into hiera and then the puppetlabs ntp module gets declared with data from your infrastructure. This module already does a lot more than only installing ntp and setting ntp servers. It will overwrite the existing ntp.conf file and even start the ntpd service.

But how about Windows systems? The puppetlabs ntp module is not suitable for Windows systems. This requires you to find another module which is capable of managing time server settings on Windows.
How about RedHat 7 which uses chrony instead of ntpd?

It is always up to you to provide proper suited profiles for all of your infrastructure systems.

## The PSICK way

Within PSICK we provide a profile for time settings (profile::time). This profile uses facter variables to identify which OS should get configuration and uses parameters for flexible usage either regarding the desired tools (chrony, ntpd, ntpdate).
The PSICK profile::time class already is an implementation class which uses upstream modules, like puppetlabs ntp.

There is no need for you to write code, you just need to provide data in hiera:

    profile::time::servers:
      - '8.8.8.8'

#  Configure SSH

## The classical way

Most of upstream module development not only install services, but build a configuration file and manage the service.
Some people might be happy with this approach, but what if you want to provide a sshd_config file or template by yourself? How to use this approach on existing infrastructure (brownfield). In this case you must review the upstream module whether it allows overwriting default settings. If this is not possible you can not use the upstream module.

Usually people start writing an implementation by themselves:

    class profile::ssh (
      $template,
    ){
      package { 'openssh-server':
        ensure => present,
      }
      file { '/etc/ssh/sshd_config':
        ensure  => file,
        content => epp('profile/ssh/sshd_config.epp'),
      }
    }

## The PSICK way

[TinyPuppet](https://github.com/example42/tp.git) is a module from example42 which allows you to do "tiny" things with Puppet. With TinyPuppet it is possible to tell Puppet to just install the package, provide an own configuratoin file or template with your own sets of data.

    class profile::ssh::openssh (
      $config_file_epp,
    ){
      ::tp::install { 'openssh':
        ensure => present,
      }
      ::tp::conf { 'openssh':
        ensure => file,
        epp    => $config_file_epp,
      }
    }

The code shown above is an abstract from code which is already available in PSICK.

Within your profile hiera data one only needs to specify which template should be used:

    profile::ssh::openssh::config_file_epp: 'profile/ssh/sshd_config.epp'

Now you only have to add your template to the profile module.

# Manage users

## The classical way

We still see platforms where users are not kept inside a central usermanagement but are configured locally.
What you usually learn in every training is that you use a self defined resource type for wrapping several resources together:

    define profile::usermanagement (
      $passwd = undef,
    ){
      File {
        owner => $title,
        group => $title,
      }
      group { $title:
        ensure => present,
      }
      user { $title:
        ensure => present,
      }
      file { "/home/${title}":
        ensure => directory,
        mode   => '0750',
      }
      file { "/home/${title}/.ssh":
        ensure => directory,
        mode   => '0700',
      }
    }

Other implementations might use puppetlabs/accounts module.

## The PSICK way

Within PSICK we have defined a set of self defined resource types.  These are not part of the implementation profile, as we believe that these are generic to use. Self defined resource types, custom facts and custom functions are kept inside the tools module.

Adding users with PSICK just requires to read and adopt our tools::user::managed self defined resource type to your needs and add hiera data.

    profile::users::static::managed_users_hash:
      'tom':
        uid              : '1002'
        homedir          : '/home/tom'
        id_rsa_source    : 'puppet:///modules/profile/users/tom/id_rsa'
        id_rsa_pub_source: 'puppet:///modules/profile/users/tom/id_rsa.pub'
      'ben':
        uid              : '1003'
        homedir          : '/home/ben'
        id_rsa_source    : 'puppet:///modules/profile/users/ben/id_rsa'
        id_rsa_pub_source: 'puppet:///modules/profile/users/ben/id_rsa.pub'

The users profile even allaws you to use other user management implementations like puppetlabs/accounts module or the pure user resource tpye. Selection on which solution to use is based on hiera data.

We wishes everybody fun with adopting and using PSICK.

Martin Alfke

