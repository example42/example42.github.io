---
layout: blog
title: Tip of the Week 69 - example42 Puppet Tutorial - Part 3
---

### example42 Puppet Tutorial - Part 3

This is the third post of a series of articles covering an introduction to Puppet.

In the [first post](https://www.example42.com/2018/04/09/puppet_tutorial_part_1/) I started with Puppet agent installation and how to use Puppet and Facter to analyze your system. Next topics have been the introduction to the Puppet programming language (DSL), how to setup the central Puppet master and how to connect Puppet agents to the Puppet master.

The [second posting](https://www.example42.com/2018/04/16/puppet_tutorial_part_2/) covered Puppet modules, code logic and variables and how to add external facts to your systems. Besides this I introduced parameters and the concept of separating code and data by using hiera.

This third part will explain how to make use of upstream Puppet libraries when describing your own infrastructure, how to best classify nodes and where to place the code.

At the last posting I will combine what I have shown and explain how to make use of the example42 [PSICK control repository](https://github.com/example42/psick.git), the [PSICK module](https://github.com/example42/puppet-psick.git) and the [PSICK hieradata](https://github.com/example42/psick-hieradata).

* Table of content
{:toc}

#### Technical Component (Library) Modules

Usually we encourage you to write your own Puppet code, because this is the best way to learn Puppet DSL. But once there will be the time where you ask yourself whether you have to maintain a large code base by yourself unless you have super simple Puppet code only.
This is the time where you will rethink your Puppet usage.

There are many people and organizations which provide Puppet modules. Main search starting point is the [Puppet Forge](https://forge.puppet.com). Another search might lead you to [GitHub](https://github.com) and here especially to [voxpupuli](https://github.com/voxpupuli) or [example42](https://github.com/example42).

The modules which can be found at the above mentioned lilnks are very generic, usable on many different opratingsystems and (hopefully) can be adopted to your specific implementation.

From now on we refer to the upstream developed, generic modules as ***Technical Component Modules***. Best way is to see them like libraries for a programming language.

But when you search e.g. for an Apache Module you will find [1056 matching modules](https://forge.puppet.com/modules?utf-8=%E2%9C%93&page_size=25&sort=rank&q=apache). So which one is the one you should use?

Luckily the Puppet Forge has some more information on modules. First there are supported modules. These modules are usually managed by Puppet itself and are included in the Puppet Enterprise Support Contract and are therefore a good choice.

Next Puppet added the "approved" flag. These are modules developed by community or organlizations and had a creful review regarding supported Operatingsystems, Tests included and have active maintainer.

Other information for each module is the number of downloads and the community feedback (Quality score).

If you find errors or misbehavior on Technical Component Modules, you are encouraged to collaborate with upstream development to get the issue fixed. It makes no sense to only locally fix the issue as you will loose upgradeability.

We recommend to mirror Technical Component Modules on your internal Git server to not rely on foreign infrastructure (network, servers, storage,...) when deploying them to your Puppet Master.

Technical Component Modules only manages the smallest possible set of configuration. A Tomcat Module only manages Tomcat, the required Java installation is managed by a Java Module. Apache Module configured Apache, PHP module does the same for PHP only.

#### Implementation Profiles

So most of the work has been made with Technical Component Module development. Now it is up to you to describe how these Modules should be implemented and adopted to your infrastructure and requirements.

This work is also placed in a Puppet Module but this module serves a secific need. It describes your implementation. Implementation Modules are now called **Profiles**.

A Profile is the smallest set of infrastructure artefacts.
Think of an authentication Profile which uses SSH, SSSD and PAM Technical Component Modules.

Now it is easy to do additional infrastructure artifacts:
Your Mail Profile uses Postfix and Clamav Modules, your logging Profile uses rsyslog and splunk Module, your Monitoring Profile uses prometheus and grafana Module.

Technically a Profile is also a Module. It has a manifests path, it can have a files and templates directory.
To better visualize the different usage, it is recommended to place Profiles into a separate modulepath.
This can be done by configuring the environment.conf file:

    # /etc/puppetlabs/code/environments/production/environment.conf
    modulepath = ./site:./modules:$basemodulepath

Within your environment you place Technical Component Modules in the `modules` directory and your profiles in a profile directory located in the `site` folder.

Differences among your platform can be laced in hiera. Usually we recommend to do lookups in profiles and to declare Technical Component Classes by specifying all required parameters.
This prevents from having hiera data with module name space.

Example - Puppet Profile

    # /etc/puppetlabs/code/environments/production/site/profile/manifests/authentication.pp
    class profile::authentication (
      Array[String] $ssh_allow_groups = [],
      Boolean       $permit_root      = false,
    ){
      # Puppet DSL code
    }

Example - Hiera Data

    # /etc/puppetlabs/code/environments/production/data/stage/dev.yaml
    profile::authentication::permit_root: true

Following this pattern allows you to easily identify which profile uses which data.

#### Business Use Case Role

When you have many identical systems it will be error prone when you just use Profiles for node classification.
In this case you want to reconsider that any system in your infrastructure servers a specific buisiness need. Some systems might be of value to IT only (metrics and backup server) some have a generic value to everybody (Mail and DNS server), some are used by customers (Login server and invoicing system).

You want to try to identify the business use case for each system. Sometimes it will be hard for IT to provide a correct name. Just head to the business owner and ask what they use the system for.
e.g. everybody knows the vacation planner, but when you ask HR they will tell you that this is the HR self service portal.

Each busines suse case is built based on profiles. We call them now **Roles**.

#### Node Classification

#### The Puppet Control Repository

The upcoming posting will explain the concept of PSICK and how you can easily adopt it to your infrastructure.

Martin Alfke
