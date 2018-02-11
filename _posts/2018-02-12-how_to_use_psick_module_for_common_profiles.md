---
layout: blog
title: Tip of the Week 59 - How to use psick module for common profiles.
---

At last [Configuration Management Camp](http://cfgmgmtcamp.eu/) we have presented [PSICK](https://www.slideshare.net/Alvagante/puppet-systems-infrastructure-construction-kit), giving some background info on the reasons behind it, an overview what it does and glimpses on how it can be used both for new and existing Puppet infrastructures.

In this post we are going to give a deeper look to how to cherry pick the profiles of the [psick module](https://github.com/example42/puppet-psick) we may need in our current infrastructure.

### Using psick module in existing infrastructures

The psick module makes large use of example42's [Tiny Puppet](https://github.com/example42/puppet-tp), which provides defines that allow installation of management of applications in a quick and powerful ways.

Tiny Puppet requires the [tinydata module](https://github.com/example42/tinydata), where is stored the data of all the supported applications on different OS.

Both psick and tp need Puppet's stdlib module, but you probably have already it.

To use psick module add to your ```Puppetfile```:

    mod 'example42/psick', :latest
    mod 'example42/tp', :latest
    mod 'example42/tinydata', :latest

In a production environment we will likely specify fixed and tested versions, the current latest version of the above modules are:

    mod 'example42/psick', :0.5.8
    mod 'example42/tp', :2.1.0
    mod 'example42/tinydata', :0.2.3

This may look a lot for not doing anything, by default, but these modules empower the possibility to manage a lot of common system configurations and applications: potentially saving you from adding several third party modules and giving you the power and flexibility of Tiny Puppet to manage applications on your site profiles.

Once you have psick in your modulepath, you have to classify the main psick class (whatever method you use to assign classes to nodes) with something like:

    include psick

This is a prerequisite for all the psick profiles, as they use common variables evaluated in the psick main class. By default, by including the psick class, nothing is done on your nodes: just a few empty classes are added to your catalog (```psick::pre```, ```psick::base```, ```psick::profiles```: they can be used for classification done directly via the psick module, but that's another feature we are not going to talk about here).

Then, when you need to manage an application or a component of your system, you will be able to choose from these options:

  - Find and use a public module that does the job
  - Write a custom profile that wraps existing modules functionalities
  - Write a custom profile or module that implements what you need without using external code (you can decide or not to use tp::install to manage your packages and service and tp::conf to manage your configuration files)
  - Find and use a psick profile that does what you need.

Usage of psick profiles is similar to the one of classes from existing modules: you classify nodes with the relevant class name, and then use hiera to configure it via it's parameters.

### PSICK profiles

Psick comes with a wide like of base profiles for common settings, here are the most significant ones:

  - psick::hosts - Manage /etc/hosts
  - psick::motd - Manage /etc/motd and /etc/issue
  - psick::nfs - Manage NFS client and server
  - psick::sudo - Manage sudo configuration
  - psick::sysctl - Manage sysctl settings
  - psick::firewall - Manage firewalling
  - psick::openssh - tp profile and keygen define
  - psick::hardening - Manage system hardening
  - psick::network - Manage networking
  - psick::puppet - Manage Puppet components
  - psick::users - Manage users
  - psick::time - Manage time and timezones

There are also several other application specific profiles, where it's generally possible to choose what module to use to manage the actual application (if a popular public module or Tiny Puppet):

  - psick::ansible - Manage Ansible installation
  - psick::aws - Manage AWS client tools and VPC setup
  - psick::bolt - Manage Bolt installation
  - psick::docker - Docker installation and build tools
  - psick::foreman - Foreman installation
  - psick::git - Git installation and configuration
  - psick::gitlab - GitLab installation and config
  - psick::mariadb - Manage Mariadb
  - psick::mysql - Manage Mysql
  - psick::mongo - Manage Mongo
  - psick::php - Manage php and modules
  - psick::oracle - Manage Oracle prereq and setup
  - psick::sensu - Manage Sensu

In PSICK all the application profiles that use Tiny Puppet have a standard structure and common parameters. They have names like ```psick::<app>::tp```, and are generated with pdk using this [template](https://github.com/example42/pdk-module-template-tp-profile).

TP encourages the usage of the template + options hash pattern, ad has some generic templates usable for common file structures. So, for example, to manage openssh with psick , we can:

    include psick::openssh::tp

and configure it with parameters like:

    psick::openssh::tp::resources_hash:
      tp::conf:
        openssh:
          template: 'psick/generic/spaced.erb'
          options_hash:
            Protocol: 2
            PermitRootLogin: 'no'
            Subsystem: 'sftp /usr/libexec/openssh/sftp-server'

Here, by including the ```psick::openssh::tp``` profile we have Openssh package installed and the relevant service started. We configure it using the ```resources_hash``` parameter, common in all tp profiles, where for each configuration file to manage via ```tp::conf```, or whole directories to manage with ```tp::dir```, we specify name, and content (by using parameters like ```source```, ```content```, ```template``` or ```epp```) and a custom ```options_hash``` where any parameter, referred in the used template, looked up in deep merge mode, can be managed via Hiera.

Alessandro Franceschi
