---
layout: blog
title: Tip of the Week 74 - What you need to know about Puppet facts - Part 1: Core facts
---

Whoever works with Puppet is probably familiar with facts.

In this series of posts we are going to review the different kind of facts we can deal with, when working with Puppet, hopefully clarifying dark zones or revealing new informations.

### Facter basics

Whenever we install Puppet's agent on a node, another tool, called **Facter** is installed.

Its task it to collect information about the system and present them as **facts**.

We can run it and see the facts it collects on our system, it shows them in alphabetical order:

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

There are a lot of use case for facts, basically everything Puppet related revolves around them:

  - In public or local modules facts like ```os, operatingsystem, osfamily, kernel...``` are used to provide correct resource names (packages, paths, services...) and behaviour for different OS.
  - Public modules can provide custom facts, for example application's version or anything needed for the managed resources
  - In our profiles we may create and add custom facts used according to our needs  
  - In our Hiera hierarchy we often use facts, eventually custom ones, based on local topologies
  - In our main manifests we may set global resource defaults or set top scope variables based on the values of facts
  - In our main manifests we can manage nodes classification based on some local fact (```include "role::${role}"```)
  - On web frontends like Puppet Enterprise Console, Foreman we may configure and classify nodes based on facts values
  - The above products, or others which just act as web frontend to PuppetDB, basically cover the best benefits of an **Inventory system**, giving easy visibility on actual status parameters, easily expandable
  - Facter can be used as standalone tool, or integrated with 3rd party software, as system's data collector (more suitable for relatively static data than data series)


We have different kind of facts:

- **Core** facts are shipped with Facter itself, we can find them in any Puppet installation

- **Custom** facts are written in Ruby and can be shipped in modules

- **External** facts are simple text files or commands (in any language) which also can be shipped in modules

- **Trusted** facts are extension requests added to Puppet's client SSL certificates. They must be defined before Puppet is run the first time and can't be changed (unless the client certificate is recreated and resigned)

Let's start, in this post to review:

### Core facts

These are the typical and most common facts we deal with when using Puppet, they are shipped with Facter itself and, starting from Facter version 3 they are written in C++ and are much faster to generate.

Earlier Facter versions had facts written in Ruby with a structure and content similar to the one we can use in Custom facts (we will review them in the next post).

Starting from version 2, facts can have values different from simple strings, so **structured facts** have  been introduced, as replacements for commonly used (and still supported) facts.

So for example ```os``` fact is an hash with values like:

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

Needless to say that it's always good practice to use $:: when referring to facts and rarely a good idea to use in our classes variables with the same names of existing facts.
