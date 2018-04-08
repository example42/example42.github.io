---
layout: blog
title: Tip of the Week 68 - example42 Puppet Tutorial - Part 2
---

### example42 Puppet Tutorial - Part 2

This is the second post of a series of articles covering an introduction to Puppet.

In the [first post](https://example42.com/blog) I started with Puppet agent installation and how to use Puppet and Facter to analyze your system. Next topics have been the introduction to the Puppet programming language (DSL), how to setup the central Puppet master and how to connect Puppet agents to the Puppet master.

This posting will cover Puppet code location and structure like modules, code logic and variables and how to add external facts to your systems. Besides this I will introduce parameters and the concept of separating code and data by using hiera.

The third part will explain how to make use of upstream Puppet libraries when describing your own infrastructure, how to best classify nodes and where to place the code.

At the last posting I will combine what I have shown and explain how to make use of the example42 [PSICK control repository](https://github.com/example42/psick.git), the [PSICK module](https://github.com/example42/puppet-psick.git) and the [PSICK hieradata](https://github.com/example42/psick-hieradata).

* Table of content
{:toc}

#### Puppet code location

Puppet code is placed on the Puppet master and is usally located in `/etc/puppetlabs/code/environments/production`.

This directory has a special name: the "production environment path". The name "production" refers to the state of your Puppet code, not to the stage of your systems.

Think about the following scenario:

The Ops Team is building an infrastructure in autmated way. The Dev Team uses this infrastructure. Where will the Ops Team test their changes? On the platform where the Dev Team is doing their work? What will happen if Ops breaks the infrastructure?

In this case it is best, to see the Development platform as a stable infrastructure with SLA. But this means, that Ops must have a development platform by themselves.
Let's also rename the teams: Ops is now Infrastructure Development, Dev is now Application Development.

You can visualize the differences by the following table:

Team | Infrastructure Development | Devevelopment | Testing | Production
--- | --- | --- | --- | ---
Application Development | - | Development | Testing | Production
Infrastructure Development | Development | Production | Production |Production

Within the environment we have a strict naming convention of content:

    /etc/puppetlabs/code/environment/
      \- production/
        |- environment.conf  # <- Here you configure your environment
        |- manifests/
        |  \- site.pp        # <- Here you place the Node Classification
        \- modules/
            \- <module>      # <- Here you place modules

#### Modules and Classes

A module is a directory located in the `$modulepath` configured location. This configuration is done in `environment.conf` and has the following default setting:

    modulepath = ./modules:$basemodulepath
    
The `$basemodulepath` configuration is a Puppet default and is especially needed if you are using Puppet Enterprise.

Best option is to see a module as a small part of your platform like ssh, ldap, apache, nginx, postfix, exim, mysql, postgresql, firewall, ...

Aditionally there are some modules which don't configure anything, but which provide extensions to Puppet (e.g. stdlib, concat, inifile).

A module has again a strict directory naming convention:

    <module>/
      |- manifests/  # <- Here you place your Puppet classes
      |- files/      # <- Here you place static configuration files
      \- templates/  # <- Here you place dynamic generated configuration files

Let's start with the content of the manifests directory. Here you add classes. Classes are written in Puppet DSL (like the puppetserver.pp file from last weeks posting).

There is just one more thing which is different to the puppetserver.pp file:
In the puppetserver.pp file we directly placed Puppet DSL code. In a class we wrap this Puppet DSL content into a class definition:

    class puppetserver {
      package { 'puppetserver':
        ensure => present,
      }
      service { 'puppetserver':
        ensure => running,
        enable => true,
      }
      file { '/etc/motd':
        ensure  => file,
        content => "# THis is puppetserver\n",
      }
    }
    
The difference: a class definition is part of your Puppet code and will only be added to a nodes catalog if a class declaration is added. Class declaration is a concept we explain in the next posting.

This time I concentrate on the concept of classes, the DSL and the naming convention.

Usually I refer to classes as parts of modules. Or better: classes are within the "namespace" of a module. The name of the module (to be more precise: the directory name) will always be part of the class. This allows you to easily identify to which module a class belongs to.

Names of classes must follow a strict ruleset. There is one special class - the main class of a module, which is placed in a file called `init.pp`.

Think about a SSH module:

    /etc/puppetlabs/code/environment/prpoduction/modules/ssh/
      \- manifests/
         \- init.pp    # <- main class of ssh module

The init.pp file will start with the term "class" and then use the module name:

    class ssh {
    }

Inside of a class you can put Puppet DSL code:

    class ssh {
      package { 'openssh-server':
        ensure => present,
      }
      package { 'openssh-client':
        ensure => present,
      }
      service { 'sshd':
        ensure => running,
        enable => true,
      }
    }

This will ensure that you have an SSH daemon running with default configuration. I already showed how you can manage the content of a file. But placing the sshd\_config file content inside the class will lead to bad readable code. Let's assume that you want to deploy one version of sshd\_config file to all systems. In this case you can use the source parameter:

    file { '/etc/ssh/sshd_config':
      ensure => file,
      source => 'puppet:///modules/ssh/sshd_config',
    }

Looking weird? I will explain:

The parameter `source` will be part of the agents catalog. So the agent must learn where to get the desired file from. That is the reason why you specify an URI. The 'puppet' protocol is shorthand for https on port 8140 including client certificate (the default Puppet connectivity behavior). We omit the servername as we have that one configured in puppet.conf file. On the Puppet server you have a Puppet internal "mount point" available, pointing to the modules directory. Now you only must tell the Puppet server which module you are referring to and what is the filename inside the modules file directory.

Please note that you must omit the files directory name!

    puppet:///modules/ssh/sshd_config
    <protocol>://<server>/modules/<modulename>/<file in files directory>

#### Puppet Variables

#### Puppet Code Logic

#### Class Parameters

#### Separation of Code and Data

The next posting will explain the concept of re-using existing modules and provide information on why you should see modules similar to libararies.
I will explain the concept of Roles and Profiles and the Node Classification.


Martin Alfke
