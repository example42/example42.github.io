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
Your Mail Profile uses Postfix and Clamav Modules, your Logging Profile uses rsyslog and splunk Module, your Monitoring Profile uses prometheus and grafana Module.

Technically a Profile is also a Module. It has a manifests path, it can have a files and templates directory.
To better visualize the different usage, it is recommended to place Profiles into a separate modulepath.
This can be done by configuring the environment.conf file:

    # /etc/puppetlabs/code/environments/production/environment.conf
    modulepath = ./site:./modules:$basemodulepath

Within your environment you place Technical Component Modules in the `modules` directory and your profiles in a profile directory located in the `site` folder.

Differences among your platform can be placed in hiera. Usually we recommend to do lookups in profiles and to declare Technical Component Classes by specifying all required parameters.
This prevents from having hiera data with module name space.

Example - Puppet Profile

    # /etc/puppetlabs/code/environments/production/site/profile/manifests/authentication.pp
    #
    class profile::authentication (
      String[1]     $ldap_server,
      Array[String] $ssh_allow_groups = [],
      Boolean       $permit_root      = false,
    ){
      # Puppet DSL code
      class { 'ssh':
        permit_root_login       => $permit_root,
        sshd_config_allowgroups => $ssh_allow_groups,
      }
      # ...
    }

Example - Hiera Data

    # /etc/puppetlabs/code/environments/production/data/stage/dev.yaml
    
    profile::authentication::ldap_server: 'ldap.domain.tld'
    profile::authentication::permit_root: true

Following this pattern allows you to easily identify which profile uses which data.

Profiles may contain:

- declaration of classes and resources
- parameters
- few Puppet DSL code logic
- files and templates
- facts
- functions
- Resource ordering

Profiles should **not** contain:

- defined resource types
- custom types and providers
- Puppet data types
- OS specific case (this must be done in a Technical Component Module)

#### Business Use Case Role

When you have many identical systems it will be error prone when you just use Profiles for node classification.
In this case you want to reconsider that any system in your infrastructure serves a specific buisiness need. Some systems might be of value to IT only (metrics and backup server) some have a generic value to everybody (Mail and DNS server), some are used by customers (Login server and invoicing system).

You want to try to identify the business use case for each system. Sometimes it will be hard for IT to provide a correct name. Just head to the business owner and ask what they use the system for.
e.g. everybody knows the 'vacation planner', but when you ask HR they will tell you that this is the 'HR self service portal'.

Each business use case is built based on profiles. We call them now **Roles**.

Roles should contain:

- declaration of Profiles classes using include or contain
- Resource ordering

Roles should **not** contain:

- explizit resource declaration
- code logic
- self defined resource types
- Puppet data types
- types and providers
- facts
- functions
- parameters

An example for a Role:

    # /etc/puppetlabs/code/environments/production/site/role/manifests/ci_server.pp
    #
    class role::ci_server {
      contain profile::authentication
      contain profile::backup::client
      contain profile::jenkins::master

      Class['profile::authentication']
      -> Class['profile::backup::client']
      -> Class['profile::jenkins::master']
    }

#### Node Classification

Now you have all Puppet Code in place.
The master muss somehow identify what Roles should be compiled into the catalog for a specifc systems. This process is called Node Classification.

There are three different ways on how to do node classification:

1. manifests based per node classification
2. fact based node classification
3. hiera based node classification

The manifest based node classification might look like being the most simple one, but that is only true for small environments with only a few systems.

Just add a node declaration to your `manifests/site.pp` in your control repository:

    # /etc/puppetlabs/code/environments/production/manifests/site.pp
    # ...
    node 'id3452276.domain.com' {
      contain role::ci_server
    }

The name provided seems to look like a FQDN. In fact it is the common name of the nodes client SSL certificate.

You can also split up your node classification in multiple files and directories, located in the manifests directory:

    # /etc/puppetlabs/code/environments/production/manifests/dev_zone.pp
    # ...
    node 'jenkins.dev.domain.com' {
      contain role::ci_server
    }

The next possible solution is to make use of facts which have been placed onto a system during provisioning.
When you for example spin up a new app webserver for your infrastructure you place deploy an external fact to the system:

    # /etc/puppetlabs/facter/facts.d/classification.yaml
    #
    application: 'webserver'
    stage: 'development'

Now you can from Puppet code query the existance of the fact and use the fact for node classification. This reduces your node classification to just one default node:

    # /etc/puppetlabs/code/environments/production/manifests/site.pp
    # ...
    node default {
      if $facts['application'] {
        contain "role::${facts['application']}"
      }
    }

Now there is also no need to have the node mentioned. You can place the variable check and class declaration directly into your site.pp file:

    # /etc/puppetlabs/code/environments/production/manifests/site.pp
    # ...
    if $facts['application'] {
      contain "role::${facts['application']}"
    }

This solution is handy when you want to be able to reuse an existing system and let it have another role, as you only have to change the fact.
**Please note that changing a systems use case is not considered best practice!** Usually you want to de-provision the old system and provision a new one.

And then there is hiera. You can add node classifications also directly into hiera.

    # /etc/puppetlabs/code/environments/production/data/nodes/id3046756732.domain.com.yaml
    #
    role: 'ci_server'

In your node classification you only do a lookup on the key 'classes' and use the value:

    # /etc/puppetlabs/code/environments/production/manifests/site.pp
    # ...
    $role = lookup('role', String, first, 'base')
    contain "role::${role}"

#### The Puppet Control Repository

Now you have everything together which is needed in a Puppet environment.
But how do you develop new features, how do you refactor existing code, how to test that everything is working?

This is where the concept of a Control Repository will help you.
A Control Repository is a GIT Repository. Different to "normal" GIT repositories the default branch will not be "master". The Control Repository uses "production" as default branch.

The required modules are listed in `Puppetfile`. For each Module you will provide the GIT url and specify a tag or a commit which should be deployed:

    # Puppetfile
    # ISSUES:
    # activemq - f4b580461e1b9c1980f3141f0414512aa6b2a0ba -  has some new features, needs new build: 0.4.1 or higher
    #
    mod 'activemq',
      :git => 'ssh://git@<git server>:<port>/<path>/puppetlabs-activemq.git',
      :ref => 'f4b580461e1b9c1980f3141f0414512aa6b2a0ba'

    mod 'ssh',
      :git => 'ssh://git@<git server>:<port>/<path>/ghoenycutt-ssh.git',
      :ref => 'v3.57.0'

Any Code development is done in a feature branch. Changes are merged with fast-forward strategy from the feature branch into the production branch.

But how do you deploy the Puppet code from the feature branch? How do you update production code after a merge?

Code deployment in this case is handeled by [r10k](https://github.com/puppetlabs/r10k). The r10k application is installed and configured on the Puppet Master:

    /opt/puppetlabs/bin/gem install r10k

Configuration file is located in `/etc/puppetlabs/r10k`:

    # /etc/puppetlabs/r10k/r10k.yaml
    ---
    :cachedir: /opt/puppetlabs/puppet/cache/r10k
    :sources:
      puppet:
        basedir: /etc/puppetlabs/code/environments
        remote: ssh://git@<git server>:<port>/<path>/puppet-control-repo.git

r10k pulls the control repository and checks for existing branches. Branch names are then converted to Puppet environment paths.
In each of the environments, r10k will parse the Puppetfile and install the mentioned modules.
This is achieved by running r10k:

    /opt/puppetlabs/puppet/bin/r10k deploy environments -pv

The `-p` option enables parsing of Puppetfile and installing modules. `-v` enables verbose output so you see what r10k is doing.

From now it is up to you, whether you want to start with an empty control repository and add all required code by yourself or whether you want to adopt an existing control repository to your needs.

The upcoming posting will explain the concept of [example42 PSICK Control Repository](https://github.com/example42/psick.git) and how you can easily adopt it to your infrastructure.

Martin Alfke
