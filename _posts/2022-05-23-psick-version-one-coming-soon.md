---
layout: blog
title: Psick module version 1 coming soon!
---

Psick (Puppet Systems Infrastructure Construction Kit) is a project that aims to provide a top of the notch Puppet infrastructure in a quick and easy way. It's composed by:

- The [Psick Control-repo](https://github.com/example42/psick){:target="_blank"} featuring useful features like Vagrant and CI integrations
- The [Psick Module](https://github.com/example42/puppet-psick){:target="_blank"} with a set of reusable profiles for the most common sysadmin activities

Version 1 of the psick module, after years of lazy developments and a recent and abundant code-rush, is going to be released soon, and there are really a lot of new things which are worth some explanations.

This is the reason of this post.

### What the psick module does?

The psick module has some unique and diverse features which can be optionally chosen.


#### Classification

Its first feature is **classification**, you can use it to manage what classes to assign to your nodes and it does it entirely in a (Hiera) data driven way.

Something like this:

    psick::base::linux_classes:
      ssh: psick::openssh
      sudo: psick::sudo

This feature has been present since the early days and there are no changes with version 1, which is therefore completely backward compatible for the classification feature.

#### Base profiles

The second big feature is a presence of several reusable profiles to manage common resources like users, ssh keys, limits, kmod, logs, time, nfs, mounts, sudo, sysctl, repos, openssh, networking, resolver and the setup of languages like php, ruby and python.

Also for this common baseline profiles there are no significant backwards incompatibilities with version 1, which just introduces new profiles like:

- psick::network, to manage networking, based on the works on version 4 of example42-network module (which is now deprecated)
- psick::rclocal, to manage rc.local also in different files, based on example42-rclocal module (now moved to voxpupuli)
- psick::systemd for basic systemd management
- psick::kmod for basic kmod management


#### Applications profiles: psick_profile

The third big feature of psick module was the presence of several application specific profiles. This is where most of the changes have happened.

In the current version the psick module has some of these profiles directly embedded and uses **example42-tp_profile** module to manage, via Tiny Puppet, these applications.

##### What changes with Psick 1

With version one the following happens:

- All/most the applications profiles are moved from psick module to the new **[psick_profile](https://github.com/example42/puppet-psick_profile)** module

- The **[tp_profile](https://github.com/example42/puppet-tp_profile)** module is now deprecated, its classes (all with the same structure and content) have been moved to **tp** classes in psick_profile.

- The new **psick_profile** module basically contains all you may cherry pick to manage applications like Grafana, Icinga2, Jenkins, Keepalived, Mongo, OpenSwan, OpenVpn, Oracle (prerequisites), Prometheus, VirtualBox, Sensu, Ansible, CheckMK, Docker, Foreman, InfluxDB, MariaDB, MySql, Nagios, Newrelic, NRPE, Postfix, PostgreSQL, Redis RabbitMQ... 

Most of the backwards incompatibilities are actually due to changes in these classes, and mostly, their move from psick and tp_profile modules.

In order to cope with them, you can check the official migration documentation.

In short:

-   just the class names change, not their behavior.
-   for the classes you use, you have to rename the relevant Hiera keys.

Relevant code changes are in these pull requests:

- PR for [Psick Version 1](https://github.com/example42/puppet-psick/pull/114)
- Module [psick_profile](https://github.com/example42/puppet-psick_profile) (changes have already been merged into this module)
- PR for the sample psick [Hieradata](https://github.com/example42/psick-hieradata/pull/8) which gives a good idea of the Hiera keys to rename


## Antipatterns condensed or just a different approach?

Psick might be considered a concentration of anti-patterns: a single module that does too many things, which is exactly, according to all best practices, what a module shouldn't do.

My stance here is this: I understand and agree with the risks of such an approach, but still I prefer to have a single module that tackles, in a coherent and comprehensive way, several common configurations that we generally add to our base profiles, rather than selecting, adapting, and chasing the dependencies of several different other component modules.

You have benefits both in terms of performance (generally with Psick we use the least amount of resources possible and, reducing the number of module dependencies, control-repo deployments are faster) and ease of use.

Also, all the features of psick are optional and you can and should cherry pick them.

All you need to do is to include the psick module, which by default, does nothing, and then configure via Hiera what you want to do: the whole classification process, if you want, or just the data for the single profiles you have classified. Like this, for the `psick::sudo` class:

    psick::sudo::directives:
      al:
        content: 'al ALL=(ALL) NOPASSWD:ALL'


## example42 "stack"

I have done Puppet modules for years, I love the modularity and the possibility to extend Puppet.

I written hundreds of different modules for different applications.

My search for optimization has driven me to develop Tiny Puppet to manage applications in a generic way, and then the psick control-repo where to have the ideal development environment, and the psick module, with all its profiles to manage common system resources and applications.

It has became clear that such open edged modules can grow uncontrolled, and that's actually what I hope, in some way: having a growing number of application profiles, which can work for most of the use cases, and are fully configurable to adapt to special needs.

Always knowing that you can **cherry pick** them and there will be on the Forge a better module to handle the same application.

The example42 stack of modules is now composed as follows, in Puppetfile format:

    mod 'example42/tp'            # Tiny Puppet         - The general purpose universal installer
    mod 'example42/tinydata'      # Tiny data           - Required by Tiny Puppet to manage every application on every OS

    mod 'example42/psick'         # psick module        - The [optional] infrastructure module to manage most of the common OS resources
    mod 'example42/psick_profile'  # psick_profile module - The [optional] psick addendum with profiles to manage different applications

plus the usual and eventual other dependencies for specific profiles.

Four modules, or just two if you need only Tiny Puppet, not too many plugins to sync, nothing done by default, but several options available a Hiera data key away.

I'm available to explain in chats or live development sessions, for free, how to better use these modules.


Alessandro Franceschi
