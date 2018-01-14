---
layout: blog
title: Tip of the Week 55 - First run mode with PSICK
---

Example42's [psick module](https://github.com/example42/puppet-psick) has several features which allows user to manage most of the typical infrastructure tasks with a single module.

One of them is classification: we can use it to define which classes we want on each node via Hiera data.

The module provides different parameters to manage in which phase of a Puppet run we want to include classes for different major families of operating systems (Linux, Windows, Solaris, Darwin...).


### Classification via psick modules

Psick has a different subclass for each phase:

  - **pre**, in this phase prerequisites classes are included, applied before all the other ones.
  - **base**, base classes, common to all the nodes (but exceptions can be applied), applied in normal catalog runs after the pre classes and before the profiles.
  - **profiles**, exactly as in the roles and profiles pattern. The profile classes that differentiate nodes by their role or function. Profiles are applied after the base classes are managed.

In order to be able to access such features you just have to add the psick class to your catalog, this can be done, at top scope for each node, in the main manifest (```manifests/site.pp```):

    include psick

This does nothing by default, every psick configuration is data driven.

The classes to include in each phase can be managed via Hiera, for different OS, as follows:

    # Pre and base classes, both on Linux and Windows
    psick::pre::linux_classes:
      puppet: ::puppet
      dns: psick::dns::resolver
      hostname: psick::hostname
      hosts: psick::hosts::resource
      repo: psick::repo
    psick::base::linux_classes:
      sudo: psick::sudo
      time: psick::time
      sysctl: psick::sysctl
      update: psick::update
      ssh: psick::openssh::tp
      mail: psick::postfix::tp
    psick::profiles::linux_classes:
      webserver: apache

    psick::pre::windows_classes:
      hosts: psick::hosts::resource
    psick::base::windows_classes:
      features: psick::windows::features
      registry: psick::windows::registry
      services: psick::windows::services
      time: psick::time
      users: psick::users::ad
   psick::profiles::windows_classes:
      webserver: iis

Each key-pair of these ${kernel}_classes parameters contain an arbitrary tag or marker (users, time, services, but could be any string), and the name of the class to include.

This name must be a valid class, which can be found in the Puppet Master modulepath (so probably defined in your control-repo ```Puppetfile```): you can use any of the existing Psick profiles, or your own local site profiles, or directly classes from public modules and configure them via Hiera in their own namespace.

To manage exceptions and use a different classes on different nodes you only have to specify the alternative class name as value for the used marker (here 'ssh'), in the appropriate Hiera file:

    psick::base::linux_classes:
      ssh: ::profile::ssh_bastion

To completely disable on specific nodes the usage of a class, included in a general hierarchy level, set the class name to an empty string:

    psick::base::linux_classes:
      ssh: ''

The pre -> base -> profiles order is strictly enforced, so we sure to place your class in the most appropriate phase (even if functionally they all do the same work: include the specified classes) and, to prevent dependency cycles, avoid to set the same class in two different phases.

### First run phase

A special phase, disabled by default, is applied only at the very first time Puppet is executed.

Its purpose is to give users the possibility to make configurations on a node via Puppet before actually making a full Puppet run.

Optionally, a reboot may be triggered at the end of this first Puppet run.

The next Puppet executions will use the normal configurations expected in each nodes.

Possible use cases for Firstrun mode:

- Set a desired hostname on Windows, reboot and join an AD domain
- Install aws-sdk gem, reboot and have ec2_tags facts since the first real Puppet run
- Set external facts with configurable content (not via pluginsync) and run a catalog
   only when they are loaded (after the first run)
- Any case where a configuration or some installations have to be done
   in a separated and never repeating first run. With or without a
   system reboot.

To enable first run mode set:

    psick::enable_firstrun: true

To define which classes to include in nodes, according to each $::kernel, we have an approach similar to the one used for the pre, base and profiles phases:

    psick::firstrun::windows_classes:
      hostname: psick::hostname
      aws_sdk: psick::aws::sdk
    psick::firstrun::linux_classes:
      hostname: psick::hostname
      proxy: psick::proxy
      aws_sdk: psick::aws::sdk

To manage if we want to trigger a system reboot after the first run:

    psick::firstrun::windows_reboot: true # (Default value)
    psick::firstrun::linux_reboot: false # (Default value)

IMPORTANT NOTE: If firstrun mode is activated on an existing infrastructure or if
the 'firstrun' external fact is removed from nodes (we use this fact, configured the the same ```psick::firstrun``` class, to determine if Puppet has already been executed or not), this class will be included
in the main psick class as if this were a real first Puppet run.
This will trigger a, probably unwanted, reboot on Windows nodes (and in any other node for which reboot is configured.

Set psick::firstrun::${kernel}_reboot to false to prevent undesired reboots.

### Conclusion

Phased, hiera data driven, classification and first run mode is just one of the features of the psick module, other are available (a rich set of profiles for common application, a standardised set of tp profiles, some common use cases defines...). The good news is that you can decide which of such features to use and you can integrate psick in existing infrastructures where traditional classification techniques are used.

Alessandro Franceschi
Martin Alfke