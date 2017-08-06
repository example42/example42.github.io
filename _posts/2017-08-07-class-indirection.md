---
layout: blog
title: Tip of the Week 32 - Puppet class indirection via Hiera
---

There are words that we, well I, sometimes use with hesitation: we are not 100% sure about their meaning, especially when they are in a foreign language.

Puppet class **indirection** is one of these.

It's the name I give to the pattern I'm going to describe in these lines, but I'm not fully sure that's a correct one.

Anyway, I already happened to write about [class indirection](2016-05-30-exploring-puppet4-modules-design-patterns.md) driven via Hiera, let's review here the key principles and see some use case.

We are used, with Puppet, to include classes which contain other classes.

It happens in most of the modules, where the main class includes sub classes to manage installation, service, configuration or extra components of the managed application.

It may happen in our site profiles, where we group different kind of resources in different classes and we wrap then in a single handy wrapper class.

Class indirection is the possibility of defining what class to use of each of this sub function.

This can be simply accomplished by exposing in the main class (the ones that includes the other ones) parameters that define the names of the sub classes to include.

An example is from [PSICK](https://github.com/example42/psick), where there's a baseline profile for each **$::kernel** which exposes a parameter to define the name of the class to use for each sub component / group of system's resources.

    class profile::base::linux (

      # General switch. If false nothing is done in this class.
      Boolean $enable,

      String $puppet_class,
      [...]
      String $ssh_class,

    ) {
      if $puppet_class != '' and $enable {
        contain $puppet_class
      }
      [...]
      if $ssh_class != '' and $enable {
        contain $ssh_class
      }
    }

This means that it's possible to define on Hiera the names of the classes to use to manage Puppet, SSH or anything else with data like:

    profile::base::linux::puppet_class: '::profile::puppet::agent'
    profile::base::linux::ssh_class: '::profile::openssh'

Which, being Hiera driven, given us complete flexibility to manage common classification problems in handling exceptions and edge cases.

On a PuppetMaster role or node Hiera file, for example, we might have:

    profile::base::linux::puppet_class: '::profile::puppet::master'

on a SSH gateway or jump host we might have:

    profile::base::linux::ssh_class: '::profile::ssh::jump'

This approach makes it easier to test and rollout new profiles and manage a gradual puppettization of resources on a brown field environment.

For example when introducing management of ssh via Puppet on existing servers, we can disable on ```common.yaml``` to inclusion of any ssh class:

    profile::base::linux::ssh_class: ''

and then to test our class on a ```env/test.yaml``` file with our profile:

    profile::base::linux::ssh_class: '::profile::openssh'

And then eventually update ```common.yaml``` with the tested ```'::profile::openssh'```.

Note that we don't always need a custom profile to manage an application, an existing module may do all what we need. In such cases, we might include it directly:

    profile::base::linux::ssh_class: '::openssh'

and use in Hiera parameters from the used module:

    openssh::root_login: false


I found this pattern particularly fitting for baseline classes that typically include other classes, but it might be useful also in normal modules.

I'd love to see, as common practice, the usage of parameters like:

    class apache (
      String     $install_class = '::apache::install',
      String     $service_class = '::apache::service',
      String     $config_class = '::apache::config',
     ) { [...] }

Having the possibility to override the class used to manage, for example, the installation of Apache, would be make the module usable, without changes, in many environments with legacy needs (for example custom repos or packages). It's up to the user to provide a working alternative class:

    apache::install_class: '::profile::apache::install'

In other cases we might replace the classes that require external modules dependencies that conflict with ours with our own modified version, in a different namespace with the needed corrections.

These are just examples. Possibilities and use cases are many but most of all, class indirection is easy to introduce in a module and doesn't harm.

To introduce is a matter of changing code like:

    class ntp (
    ) {
      contain ntp::install
      contain ntp::config
      contain ntp::service
      Class['::ntp::install']
      -> Class['::ntp::config']
      ~> Class['::ntp::service']
    }

to something like:

    class ntp (
      String $install_class = '::ntp::install',
      String $config_class = '::ntp::config',
      String $service_class = '::ntp::service',
    ) {
      contain $install_class
      contain $config_class
      contain $service_class
      Class[$install_class]
      -> Class[$config_class]
      ~> Class[$service_class]
    }

Will users ever use such parameters to provide their own classes? In many cases never, but adding them requires low efforts and makes the module more adaptable to special cases.

Alessandro Franceschi
