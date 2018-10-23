---
layout: blog
title: Tip of the Week 95 - Roles and profiles - explained
---

Either during training or at onsite consulting we are confronted with the question on what a profile is, how to best build it and how it differs from a module and a role.
Within this week's tip of the week we want to show our best practices on Puppet implementation profile development covering namespaces, parameter usage, content and templates and testing.

* Table of content
{:toc}

No time to read everything and code for yourself? Jump to the end of this page.


## What is a profile?

A profile describes a technical implementation on your systems. The code may consist of all self written Puppet code (`package`, `file`, `service`) or may use existing modules (`class { ::ntp: servers => $ntp_servers, }`).

You want to have self written Puppet code in case that you are still in the process of learning Puppet and learn how to read (and check) existing modules. Once you are able to read and understand existing Puppet module code, you might want to switch to an existing module.

**Hint: Never write modules! Write profiles instead! This will not block you using an existing namespace (module directory name).**

A technical component can be something like SSH, backup, your web server with specific extensions, your virus scanner installation.

Configuration differences are either placed directly into your code (static data) or placed into hiera using automatic data binding on profile class parameters.

Additionally a profile directory structure can also hold templates or static configuration files.

## Profile naming and namespaces

You want to think about different names for related configurations. Usually these consist of several processes which must work together. Think about the following example, assuming a Linux only platform:

Your Login into a VM consists of SSH, SSSD with LDAP integration and SUDO settings. Your profile is responsible for the authorization and authentication. These are names you can use for your profile:

    # <$environmentpath><$environment>/site/profile/manifests/auth.pp
    # Class profile::auth
    #
    # @summary Authorization and Authentication for SSH users
    #
    # @param sshd_conf_allowgroups
    #   must be type array, defaults to empty array
    #   list of groupnames with ssh access used by ghoneycutt-ssh module
    #
    # @param sssd_config
    #   must be of type hash, defaults to empty hash
    #   configuration settings used by sgnl05-sssd module
    #
    # @param sudo_config
    #   must be of type hash, defaults to empty hash
    #   configuration settings for saz-sudo module
    #
    class profile::auth (
      Array $sshd_config_allowgroups= [],
      Hash  $sssd_config = {},
      Hash  $sudo_configs = {},
    ) {
      class { 'sssd':
        config         => $sssd_config,
      }
      # ...
    }

Always remember to add documentation to your modules. This is highly important and can be visualized by [puppet-strings](https://github.com/puppetlabs/puppet-strings).

Other - non basic parts of your server - can be easily grouped by placing them into a directory structure. Now we will add windows support:

    <$environmentpath><$environment>/site/profile/manifests/
     |- auth/
     |    |- linux.pp                      # <- SSH, LDAP, PAM
     |    \- windows.pp                    # <- RDP
     |- time/
     |    |- ntpdate.pp                    # <- NTP Linux
     |    \- windows.pp                    # <- NTP Windows
     |- databases/
     |    |- mysql_server.pp               # <- MySQL - Linux
     |    \- postgresql_server.pp          # <- PostgreSQL - Linux
     |- monitoring/
     |    |- alerting.pp                   # <- Prometheus Alerting - Linux
     |    |- metrics.pp                    # <- Prometheus Metrics - Linux
     |    |- node.pp                       # <- Prometheus Node <- Linux/Windows
     |    \- server.pp                     # <- Prometheus Server - Linux
     |- services/
     |    |- systemd_wait_for_port.pp      # <- Snippet to set secial setting in unit file
     |    \- docker_timeout.pp             # <- Snippet to set container max start time

## Parameters and automatic data binding with Hiera

Puppet can lookup data for classes whenever they are declared. The lookup key name passed to hiera is built programatically: `<class name>::<parameter>`.

Data for `profile::auth` class might look like this:

    profile::auth::sshd_config_allowgroups:
      - 'infastructure_admins'
      - 'all_developers'

This concept allows you to always identify which profile is using which data. For data used by multiple profiles you can do nested lookups within hiera:

    profile::auth::sssd_config:
      'domain/LDAP':
        'ldap_default_authtok': "%{lookup('ldap_pw')}"

This security artifact is stored using [hiera-eyaml](https://github.com/voxpupuli/hiera-eyaml/blob/master/README.md):

    ldap_pw: >
        ENC[PKCS7,MIIBeQ...]

Security settings are now separated from configuration settings.

## What is a role?

A role is a class that includes ones or more profiles. It's generally recommended that in role classes you just include profiles, without passing parameters or other Puppet resources.

A role class may look like:

    class role::webserver {
      include profile::base
      include profile::apache
      include profile::php
    }

This implies that as we may have a `profile` module containing all our profile classes, we can have a `role` module containing all our role classes.

So, basically, roles are used to simplify nodes classification. You just include a role class for each nodes' role and all the rest is managed according to the profiles included there. If you have a fact called $role we can just have a line like this in our control repo's `manifests/site.pp`:

    include "::role::${::role}"

For this reason, even if the roles and profiles pattern is well established as it makes things simpler, it's not necessarily the only approach we can use: we may have just profiles without roles, in this case we don't need role classes, but just other ways to define what profiles to include in a node (for example via Hiera data, or on an external node classifier).

Bear this in mind when working with roles and profiles: what you really need to define is basically what profiles you want on your nodes, how this is done, if via role classes or other methods does not make a real difference.

## Using an existing implementation

So now the real work begins: writing profiles for all the different things you have in your environment.

Profiles are typically local classes, not supposed to be shared, as they implement our own specific way to manage resources.

Still you can actually benefit from others' work on profiles: our [PSICK module](https://github.com/example42/puppet-psick/) contains several reusable profiles, some of them use [tiny-puppet](https://github.com/example42/puppet-tp/blob/master/README.md) some plain Puppet resources, and they cover [common features](https://github.com/example42/puppet-psick#psick-base-profiles) and use cases which may apply also to your setup.

The important thing to understand about the psick module, is that you can pick the profiles you want to use, and ignore the others: you decide which solution you prefer: you just have to be sure that if you include any psick profile, you should also include the main psick class (which by default, with the predefined parameters, does NOTHING):

    include psick # Prerequisite for all the psick Profiles
    include psick::time # A profile to manage NTP and timezones on Linux and Windows

All psick profiles have parameters which can be used to customise and manage their behaviour via Hiera data.

We wish everybody success.

Please provide feedback, especially when you are using our [Puppet Systems Infrastructure Construction Kit - PSICK](https://github.com/example42/psick)

Martin Alfke

Alessandro Franceschi
