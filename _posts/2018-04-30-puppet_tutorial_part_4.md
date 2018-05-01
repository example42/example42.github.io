---
layout: blog
title: Tip of the Week 70 - example42 Puppet Tutorial - Part 4
---

### example42 Puppet Tutorial - Part 4

This is the last post of a series of articles covering an introduction to Puppet.

In the [first post](https://www.example42.com/2018/04/09/puppet_tutorial_part_1/) I started with Puppet agent installation and how to use Puppet and Facter to analyse your system. Next topics have been the introduction to the Puppet programming language (DSL), how to setup the central Puppet master and how to connect Puppet agents to the Puppet master.

The [second posting](https://www.example42.com/2018/04/16/puppet_tutorial_part_2/) covered cover Puppet modules, code logic and variables and how to add external facts to your systems. Besides this I introduced parameters and the concept of separating code and data by using hiera.

The [third part](http://example42.com/2018/04/23/puppet_tutorial_part_3/) explained how to make use of upstream Puppet libraries when describing your own infrastructure, how to best classify nodes and where to place the code.

In this posting I will combine what I have shown and explain how to make use of the example42 [PSICK control repository](https://github.com/example42/psick.git), the [PSICK module](https://github.com/example42/puppet-psick.git) and the sample [PSICK hieradata](https://github.com/example42/psick-hieradata).

* Table of content
{:toc}

#### The PSICK Control Repository

One of the biggest challenges for whoever is new to Puppet is how to organise code and data in order to safely and effectively manage the current infrastructure and be ready for future evolutions. PSICK has been done by people who have 10 years of Puppet experience, have designed and build dozens of infrastructure of any size and over the years have updated and refined the approach to Puppet design according to the evolution of the tool.

Some design choices in PSICK are rather unusual, and don't look like the typical ones in Puppet world (ie: the classic roles and profiles pattern).
We like to think they are evolutions and steps forward, even if opinionated.

Note anyway that you can decide what to use and what to change in PSICK, so ultimately the choice is always yours.

The [PSICK control repository](https://github.com/example42/psick.git) contains:

- Setup automation (Hardware, Vagrant, Fabric, Docker)
- Unit and acceptance tests (rspec-puppet, beaker)
- CI/CD integration (GitLab, Jenkins, Travis, Danger)
- Developer support (editorconfig, Vscode, RuboCop, Codacy)
- Multiple Vagrant environments where to test your code

Your main starting point is `manifests/site.pp` here you want to define the top scope variables used in Hiera, set defaults for some resources defaults and manage the server side noop mode. Then the psick class from [example42 PSICK puppet module](https://github.com/example42/puppet-psick.git) is included:

    include '::psick'

Next important file is `hiera.yaml`, the environment level hiera configuration file.

Here you see that data and data management is split into a separated hieradata repository:

    defaults:
    datadir: modules/hieradata/data # Data in separated module, defined in Puppetfile
    # datadir: hieradata            # Data in control-repo. Previous psick setting
    # datadir: data                 # Data in control-repo. Default for puppetlabs/control-repo

 We do this on PSICK control-repo in order to ease its upgrade without the need to align the sample hieradata, in some cases it may be preferred to have the hieradata directly in the control repo directory. The choice depends mostly on personal preferences and if different people need to access and edit the data from the ones who have to manage the Puppet code.

Also, by default, we use and recommend the usage of [hiera-eyaml[(https://www.example42.com/2017/08/21/encrypt-your-secrets-with-hiera-eyaml/) to encrypt sensitive data. Note that you must create your own keys in order to use it:

    pushd /etc/puppetlabs/puppet
    /opt/puppetlabs/puppet/bin/eyaml createkeys
    popd

Hiera hierarchy is probably something you may need to change and adapt to your infrastructure. The default one looks like:

    paths:
      - "nodes/%{trusted.certname}.yaml"
      - "role/%{::role}-%{::env}.yaml"
      - "role/%{::role}.yaml"
      - "zone/%{::zone}.yaml"
      - "common.yaml"

Zone may refer to a datacenter or region, the role is the function of the system (as in the roles and profiles pattern), and env is the operational environment or tier of the node.

All the variables must be top scope, so they are supposed to be set as facts, or defined in the ```site.pp``` or set via an External Node Classifier (ENC) like Puppet enterprise or The Foreman.

Upstream dependencies are placed into `Puppetfile`. This is probably another file you are going to change, adding the public module you decide to use.
By using [example42's tiny-puppet](http://tiny-puppet.com/) and the psick module we are able to manage a lot of different profiles and applications without adding extra, dedicated, modules, but as usual you can opt to chose differently.

#### The PSICK Module (Library)

The PSICK module can be considered an infrastructure library which provides 3 major features:

- Phased classification
- Profiles for common system configurations
- TinyPuppet profiles to manage applications (via tp module)

##### Phased classification

Normal nodes classification is done using the ```node``` statement, using roles classes, using an ENC, using ```hiera_include``` (or ```lookup```) or including classes in ```site.pp``` according to custom logic.

The psick module can manage classification and it does it in phased way entirely configurable via Hiera. Four phases are available:

  - **firstrun**, optional phase, in which the resulting catalog is applied only once, at the first Puppet run. At its end a reboot can optionally be triggered and the real definitive catalog is applied.
  - **pre**, prerequisites classes, they are applied in a normal catalog run (that is, always except in the very first Puppet run, if firstrun is enabled) before all the other classes. Here for example you can include classes that manage network, repositories, and everything you want to apply first.
  - **base**, base classes, common to all the nodes (but exceptions can always be managed via Hiera), applied in normal catalog runs after the pre classes and before the profiles.
  - **profiles**, exactly as in the roles and profiles pattern. The profile classes that differentiate nodes by their role or function. Profiles are applied after the base classes are managed.

Strictly speaking, besides the ordering, which you can decide to use or not, there's no difference among classes included in the pre, base or profiles phases.

To define what classes you want to include in what phases you can use parameters as follows:

    # Optional firstrun phase for Linux and Windows
    psick::enable_firstrun: true # default is false
    psick::firstrun::linux_classes:
      hostname: psick::hostname
      packages: psick::aws::sdk
    psick::firstrun::windows_classes:
      hostname: psick::hostname
      packages: psick::aws::sdk

    # Sample pre, base and profiles phases for Linux
    psick::pre::linux_classes:
      puppet: ::puppet
      dns: psick::dns::resolver
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

    # Sample pre, base and profiles phases for Windows
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

There are different key names for Linux and Windows (and Solaris and Darwin) to ease Hiera driven classification for entirely different OS without the need of adding OS dependent variables in your Hiera's hierarchy.

The classes included are defined in the values of the above hashes. They can be any class for any module in the modulepath: dedicated component modules, custom profiles, profiles from the psick module (as in many entries of the above example).

The keys of the hashes can be any string and their purpose is to allow override across Hiera hierarchies. For example of a specific node, let's say a Puppet server, you may want to use a different class to manage puppet, you can do by setting, in that node's Hiera data (here as yaml file) something like:

    psick::pre::linux_classes:
      puppet: ::profiles::puppetmaster

Using the psick module to classify nodes, is an option. You can follow more traditional (who said primitive? :-) ways and use psick only for its profiles...

##### Base profiles

Even if every infrastructure is a snowflake of its own, the kind of resources to manage on a system is more or less always the same: users, packages, authentication, dns, ntp, networking, sudo, ssh and so on.

For the most common use cases the psick module provides profiles, both for Linux and Windows. In most of the cases such profiles can be used instead of adding a dedicated module to your Puppetfile, but, as usual, you can decide if and which ones to use.

Give a look at [psick's manifests](https://github.com/example42/puppet-psick/tree/master/manifests) to have an idea of the available profiles.

Some of these profiles are able to manage common system features for Linux (users, cron, sysctl, time and timezones, hostname, hosts file, repositories, system's proxy, dns, motd, nfs, syslog, iptables...) and Windows (users, packages, features, registry keys, services, time...) other are application specific and in some cases can even provide more features than dedicated component modules (apache, openssh, bolt, ansible, mariadb, mysql, docker, gitlab, icinga, java, mongo, openvpn, oracle, openswan, prometheus, php, puppet...).

In some cases a psick profile even allows you to choose different modules to manage the same resource (users, sysctl, puppet, php, docker ...).

##### TP profiles

Besides the multitude of base profiles, in the psick module there are so called, tp profiles, they are always in manifests called ```tp.pp```, they are automatically generated and provide a standard interface to manage an application using Tiny Puppet. For example to manage apache via Tiny Puppet you can use the profile ```psick::apache::tp``` by setting something like:

    psick::profiles::linux_classes:
    'apache': psick::apache::tp

Then you can configure it with something like:

    psick::apache::tp::resources_hash:
    tp::conf:
        apache::openkills.info.conf:
        base_dir: conf
        template: psick/apache/vhost.conf.erb
        options_hash:
            ServerName: openskills.info
            ServerAlias:
            - openskill.info
            - www.openskills.info
            - www.openskill.info
            AddDefaultCharset: ISO-8859-1
        apache::deny_git.conf:
        base_dir: conf
        source: puppet:///modules/psick/apache/deny_git.conf
    tp::dir:
        apache::openskills.info:
        vcsrepo: git
        source: git@bitbucket.org:alvagante/openskills.info.git
        path: /var/www/html/openskills.info

#### The PSICK hieradata

Everything in PSICK is entirely data driven. Via Hiera you can configure classification and configuration of classes.

Infrastructure data is typically site specific, so we placed in a separated module the sample Hieradata used in the PSICK control repo, to ease the usage of custom data in custom modules (or directly in the control repo).

Give a look at the [PSICK hieradata](https://github.com/example42/psick-hieradata) module to see real world examples of the data you can use to configure an infrastructure via PSICK. In particular the [lab zone](https://github.com/example42/psick-hieradata/blob/production/data/zone/lab.yaml) with lab [hosts specific data](https://github.com/example42/psick-hieradata/tree/production/data/nodes) is actually used to configure the living servers in our [PSICK lab](http://lab.psick.io/) setup, which runs using the [Vagrant environment](https://github.com/example42/psick/tree/production/vagrant/environments/lab) in the control repo.

You can use that data as starting point to build your own infrastructure with PSICK.

Happy hacking.

Martin Alfke
Alessandro Franceschi
