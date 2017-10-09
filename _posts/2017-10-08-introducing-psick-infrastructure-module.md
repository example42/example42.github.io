---
layout: blog
title: Tip of the Week 41 - Introducing PSICK - The Puppet infrastrucutre module
---

We have talked in the past about [PSICK](https://github.com/example42/psick), example42's Puppet control-repo which provides an integrated, powerful and customisable Puppet setup.

This control repo had a set of profiles to manage common configurations using either external modules or local classes. We have seen this set of profiles grow over time and we have realised that they could be useful for any user, also the ones not using our control-repo. So we have decided to make out of them a dedicated, separated module and place there some of the classification logic we had in our control-repos main manifests directory.

So here is the [PSICK module](https://github.com/example42/puppet-psick), the first Infrastructure Puppet module.

You can get it from the [Forge](https://forge.puppet.com/example42/psick) or GitHub and just include it in your main manifest or any node classifier:

    include psick

Once you do it, nothing happens :-D, as PSICK is entirely configurable via Hiera and allows you to decide what of its components and functions to use.

PSICK modules main components are:

  - **Classification**: you can use PSICK to classify, via Hiera, your nodes in well structured and robust way
  - **Base profiles**: a set of classes that manage common configuration needs (resolver, time, sysctl, users, proxy, sudo...)
  - **TP profiles**: a set of standard profiles to manage, using [Tiny Puppet](https://github.com/example42/puppet-tp), applications like apache, mysql, openssh, mongodb and basically whatever is [supported](https://github.com/example42/tinydata/tree/master/data) by Tiny Puppet

Every PSICK configuration is data driven, so if you are using the YAML backend you can have your data as in the following examples.

### Classification

Classification is based on the (opinionated) assumption that, when defining the classes and resources that are needed on a node it's easier to split them by the underlying $kernel (Linux, Windows, Solaris..) and that, typically each node has a set of classes that should be applied before anything else (```pre```), a set of common classes applied to all the nodes of the infrastructure (```base```) and a set of specific classes (```profiles```), which are different for each role.

In some cases, finally there could be some classes/resources that we want to apply only once, at the first Puppet run (```firstrun```).

The PSICK module has classes that expose parameters that allow to specify the classes to include (note: they can be psick profiles, local profiles or external modules, choice is up to the user) on each phase for each $kernel.

They can be expressed as hashes of key-values, looked up in deep merge mode, where keys are markers that allow override across the hierarchy, and the values are the names of the classes to include.

A complete example of how classification may look like is as follows:

    # First run optional settings for Linux and Windows
    psick::enable_firstrun: true # By default firstrun mode is disabled
    psick::firstrun::linux_classes:
      hostname: psick::hostname
    psick::firstrun::windows_classes:
      hostname: psick::hostname

    # Common Linux classes
    psick::pre::linux_classes:
      puppet: puppet
      hostname: psick::hostname
      hosts: psick::hosts::resource
      dns: psick::dns::resolver
      repo: psick::repo
      users: psick::users
    psick::base::linux_classes:
      mail: psick::postfix::tp
      ssh: psick::openssh::tp
      sudo: psick::sudo
      logs: psick::logs::rsyslog
      time: psick::time
      sysctl: psick::sysctl
      update: psick::update
      motd: psick::motd
      profile: psick::profile
      network: network
      systat: psick::monitor::sar

    # Pre and Base psick settings Windows
    psick::pre::windows_classes:
      hosts: psick::hosts::resource
    psick::base::windows_classes:
      features: psick::windows::features
      registry: psick::windows::registry
      services: psick::windows::services
      time: psick::time
      users: psick::users::ad

    # Profiles for specific roles (ie: webserver)
    psick::profiles::linux_classes:
      webserver: apache
    psick::profiles::windows_classes:
      webserver: iis

### Common profiles

The PSICK module provides a quite large of profiles for common configurations we do on servers. Some of them even support different common external modules as alternative to PSICK's internal resources (like [psick::sysctl](https://github.com/example42/puppet-psick/blob/master/manifests/sysctl.pp) or [psick::users](https://github.com/example42/puppet-psick/blob/master/manifests/users.pp).

The idea here is that for many common activities it's not really needed to look for a dedicated public module, deal with its dependencies, and eventually for it locally to make it fit our implementation.

An example of Hiera data configuring some of these PSICK common profiles is as follows, refer to relevant classes documentation for details:

    # Repo settings
    psick::repo::add_defaults: true

    # Time settings
    psick::time::servers:
      - 'pool.ntp.org'

    # Timezone settings
    psick::timezone::timezone: 'UTC'

    # Sample sysctl settings
    psick::sysctl::settings_hash:
      net.ipv4.conf.all.forwarding: 0

    # Users management
    psick::users::delete_unmanaged: false
    psick::users::module: 'user'
    psick::users::users_hash:
      al:
        ensure: present
        comment: 'Al'
        groups:
          - users
        ssh_authorized_keys:
          - 'ssh-rsa AAAAB3N.....'

    # Hosts management
    psick::hosts::dynamic::extra_hosts:
      'puppet.lab.psick.io':
        ip: '10.42.43.101'
        host_aliases:
          - puppet


### TP profiles

Another set of features offered by the PSICK module are TP (Tiny Puppet) profiles: they offer a standard interface to the management of configurations of applications. Technically speaking any application for which we have [tinydata](https://github.com/example/tinydata) for.

Tiny Puppet takes care to install the relevant application on different OS but it's up to the user to provide the configurations needed, with full freedom on how they are delivered (as static source files, via erb/epp templates using hashes of custom options).

An example of configuration of tp profiles looks like this:

    # Postfix configuration
    psick::postfix::tp::resources_hash:
      tp::conf:
        postfix:
          template: 'psick/postfix/main.cf.erb'

    psick::postfix::tp::options_hash:
      'mydomain': "%{facts.domain}"
      'inet_interfaces': '127.0.0.1'
      'inet_protocols': 'all'
      'my_destination': '$myhostname, localhost.$mydomain, localhost'

    # Apache configuration
    psick::apache::tp::resources_hash:
      tp::conf:
        apache::example.com.conf:
          base_dir: conf
          template: psick/apache/vhost.conf.erb
          options_hash:
            ServerName: example.com
            ServerAlias:
              - www.example.com
            AddDefaultCharset: ISO-8859-1
        apache::deny_git.conf:
          base_dir: conf
          source: puppet:///modules/psick/apache/deny_git.conf
      tp::dir:
        apache::example.com:
          vcsrepo: git
          source: git@github.com/company/example.com.git
          path: /var/www/html/example.com

Here we define an hash of tp resources to apply ([tp::conf](https://github.com/example42/puppet-tp/blob/master/manifests/conf.pp) and [tp::dir](https://github.com/example42/puppet-tp/blob/master/manifests/dir.pp) ) and an hash of custom options that we can use in our templates.

In templates we can use both the options, provided by users, and OS dependent tp settings, defined in tinydata, to easy support for multiple OS in the same template.

For example, the template ```psick/apache/vhost.conf.erb``` which follows, uses variable like ```@settings['data_dir_path']```, indicating the default DocumentRoot, which changes according the underlying OS:

    # File Managed by Tiny Puppet

    <VirtualHost *:80>
        DocumentRoot <%= @settings['data_dir_path'] %>/<%= @options['ServerName'] %>
        ServerName <%= @options['ServerName'] %>

    <% if @options['ServerAlias'] != "" -%>
    <% if @options['ServerAlias'].is_a? Array -%>
        ServerAlias <%= @options['ServerAlias'].flatten.join(" ") %>
    <% else -%>
        ServerAlias <%= @options['ServerAlias'] %>
    <% end -%>
    <% end -%>

    <% if @options['AddDefaultCharset'] -%>
        AddDefaultCharset <%= @options['AddDefaultCharset'] -%>
    <% end -%>

        ErrorLog  <%= @settings['log_dir_path'] %>/<%= @options['ServerName'] %>-error_log
        CustomLog <%= @settings['log_dir_path'] %>/<%= @options['ServerName'] %>-access_log common

    </VirtualHost>

For some applications, besides standard tp profiles, where are more complex classes to manage application specific items, give a look at the [mariadb](https://github.com/example42/puppet-psick/tree/master/manifests/mariadb) , [php](https://github.com/example42/puppet-psick/tree/master/manifests/php) , [docker](https://github.com/example42/puppet-psick/tree/master/manifests/docker) , [ansible](https://github.com/example42/puppet-psick/tree/master/manifests/ansible) classes for some examples.

All these profiles are optional, you can decide to use them or external component modules or local profiles to manage a specific application in the way you want, and you can even have a mix of them.


### Conclusion

The PSICK module does a lot of things, definitively too many according to purists of "a module for each application/function", but as we always try to do, it's always a matter of choice. You can choose what you want to use of this module, you can decide to install and configure applications via Tiny Puppet or via dedicated modules, and this choice can be done for every single component you want to manage.

PSICK has a few dependencies, the **puppet-stdlib** module, which should be already used in any Puppet environment, and **example42-tp** module (Tiny Puppet) which depends on **example42-tinydata**.

All these modules can be added to your modules' path seamlessly and without any interference with existing Puppet setups (a few extensions are pluginsynced, but we have been careful to reduce as much as possible their number).

On the other side, if you embrace the PSICK philosophy to its full, you'll have dramatically reduced the amount of modules needed to configure your systems (and much less conflicting modules dependencies hell), you will have a clean way to order your classes and you'll have extremely compact catalogs, with a limited number of resources doing a lot of things.

The PSICK module, paired with the PSICK control-repo can help you in setting up a state of the art Puppet infrastructure in a few time, with full flexibility or how and what to configure on your systems.

We hope you'll understand and appreciate them as we do and, please, do let us know what you think should be made different and better: works on them has just began, we plan to add a lot of stuff to them in order to make sysadmins life better.

Alessandro Franceschi
