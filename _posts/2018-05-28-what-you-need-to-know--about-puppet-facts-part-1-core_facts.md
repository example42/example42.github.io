---
layout: blog
title: Tip of the Week 74 - What you need to know about Puppet facts. Part 1 - Core facts
---

Whoever works with Puppet is probably familiar with facts.

In this series of posts we are going to review the different kind of facts we can deal with, when working with Puppet, hopefully clarifying grey zones or revealing new informations.

### Facter basics

Whenever we install Puppet's agent on a node, another tool, called **Facter** is installed.

Its task it to collect information about the system, *any* Operating System, and present them as **facts**.

We can run it from the command line and see the facts it collects on our system, it shows them in alphabetical order:

    $ facter

    aio_agent_version => 5.3.2
    [...]
    timezone => CEST
    virtual => virtualbox

Facter is executed at the beginning of every Puppet run and the collected facts are included in the catalog request by the Puppet agent to the Puppet server.

After receiving a client's catalog request, the Puppet server does the following:

- [Usually] stores the client's facts on PuppetDB, so that they can be queried and **visualised** in some web frontend
- Uses the facts, together with our code and data, to compile the client's catalog which is then sent back

So the actual catalog applied during a Puppet run on the client, can be based on data coming from the client itself, collected as facts.

Facts are or can be used in a lot of places in our Puppet control-repo:

  - In public or local modules facts like ```os, operatingsystem, osfamily, kernel...``` are used to provide correct resource names (packages, paths, services...) and behaviour for different OS.
  - Modules can provide custom facts, for example application's version or anything needed for the managed resources
  - In our profiles we may create and add custom facts used according to our needs  
  - In our Hiera's hierarchy we often use facts, eventually custom ones, based on local topologies
  - In our main manifests we may set global resource defaults or set top scope variables based on the values of facts
  - In our main manifests we can manage nodes classification based on some local fact (```include "role::${role}"```)
  - On web frontends like Puppet Enterprise Console, Foreman we may configure and classify nodes based on facts values
  - Any web frontend able to access PuppetDB can have a function of an **Inventory system**, giving easy visibility to [semi] realtime, easily customisable, facts about the system
  - Facter can be installed as standalone tool, without Puppet, and be integrated with 3rd party software, as system's data collector (more suitable for relatively static informations than data series)

We have different kind of facts:

- **Core** facts are shipped with Facter itself, we can find them in any Puppet installation

- **Custom** facts are written in Ruby and can be shipped in modules

- **External** facts are simple text files or commands (in any language) which also can be shipped in modules

- **Trusted** facts are extension requests added to Puppet's client SSL certificates. They must be defined before the very first Puppet run and once set, can't be changed (unless the client certificate is recreated and resigned)

Let's start, in this post to review:

### Core facts

These are the typical and most common facts we deal with when using Puppet, they are shipped with Facter itself and, starting from Facter version 3 they are written in C++ and are much faster to generate.

Earlier Facter versions had facts written in Ruby with a structure and content similar to the one we can use in Custom facts (we will review them in the next post).

Starting from Facter 2, facts can have values different from simple strings, so **structured facts** have been introduced.

In Puppet 3 a neater distinction has been promoted:
- New, mostly structured, **modern facts** are the recommended onesaas
- The, widely used, older **legacy facts** are still supported, but not visualised by default from the command line.

So, for example, legagy facts, like ```operatingsystem```, ```osfamily```, ```architecture``` are now replaceable with subkeys of the modern, structured fact ```os```:

    [vagrant@git ~]$ facter  os
    {
      architecture => "x86_64",
      family => "RedHat",
      hardware => "x86_64",
      name => "CentOS",
      release => {
        full => "7.5.1804",
        major => "7",
        minor => "5"
      },
      selinux => {
        config_mode => "enforcing",
        config_policy => "targeted",
        current_mode => "enforcing",
        enabled => true,
        enforced => true,
        policy_version => "28"
      }
    }

Being an hash, we can access the values of its subkeys as we normally do in Puppet code:

    class report_os {
      notice ("Operating system: ${::os['name']}")
      if $::os['family'] == 'RedHat'
      and has_key('os','selinux') {
        notice ("Selinux current mode ${::os['selinux']['current_mode']}")
      }
    }

We have actually different ways to access to facts in Puppet code:

- Referring directly to them: ```$factname```
- Using the ```$facts``` hash: ```$facts[$factname]```
- Using the ```fact``` function from stdlib module (which allows dotted notation and doesn't fail if we try to access a non existing subkey): ```fact($factname)```.

So for example, the legacy fact ```$osfamily``` can be expressed also with any of these alternatives:
- ```$os['osfamily']```
- ```$facts['os']['osfamily']```
- ```fact('os.osfamily')```

The most commonly used **legacy facts** are:
- ```operatingsystem``` ( same of ```$::os['operatingsystem']``` )
- ```osfamily``` ( same of ```$::os['family']``` )
- ```operatingsystemrelease``` ( same of ```$::os['version']['full']``` )
- ```architecture``` ( same of ```$::os['architecture']``` )
- ```ipaddress``` ( same of ```$::networking['interfaces']["${::networking['primary']}"]['ip']``` )
- ```fqdn``` ( same of ```$::networking['fqdn']``` )
- ```hostname``` ( same of ```$::networking['hostname']``` )
- ```domain``` ( same of ```$::networking['domain']``` )


The most interesting **modern facts**:

- ```os```: Basic system info
- ```networking```: Networking info and status
- ```disks```: Disks layout
- ```filesystems```: Filesystems layout
- ```identity```: Info about the user running Facter
- ```memory```: Info about system memory
- ```processors```: Info about CPUs
- ```system_uptime```: Uptime, in various units
- ```ssh```: System's ssh host public keys in various formats
- ```timezone```: The system's timezone
- ```virtual```: Name of Hypervisor, or 'physical' for physical machines

#### Digression on facts and local class variables

All the facts are available as top scope variables when we refer to them in our code, so, for example, the ```os``` fact can be expressed with the ```$::os``` variable.

Note the leading ```::``` which ensures we are referring to a top scope variable called os. We can also use just ```$os```, but doing so we are not sure if we refer to the os fact or a local class variable with the same name.

The better you give the idea, a code like this:

    class test_fact {
      notice("\$::timezone is: ${::timezone}")
      notice("\$timezone is: ${timezone}")
      $timezone = 'Local change'
      notice("\$::timezone, after local override is still: ${::timezone}")
      notice("\$timezone, after local override is now: ${timezone}")
    }
    include test_fact

generates this output:

    Notice: Scope(Class[Test_fact]): $::timezone is: CEST
    Notice: Scope(Class[Test_fact]): $timezone is still : CEST
    Notice: Scope(Class[Test_fact]): $::timezone, after local override is still: CEST
    Notice: Scope(Class[Test_fact]): $timezone, after local override is now: Local change


### Conclusions

In this first part of a a series of blog posts, we have seen the basic of Facter and its core facts, with particular emphasis on the difference between modern and legacy facts.

Next week we will start to see how we can create our own facts, customised to our needs.

Facts, not only words!

Alessandro Franceschi
