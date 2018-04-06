---
layout: blog
title: Tip of the Week 67 - example42 Puppet Tutorial - Part 1
---

### example42 Puppet Tutorial - Part 1

This is the first post of a series of articles covering an introduction to Puppet.

I start with Puppet agent installation and how to use Puppet and Facter to analyze a system. Next topics are the introduction to the Puppet programming language (DSL), how to setup a central Puppet master and how to connect Puppet agents to a Puppet master.

The second part will cover Puppet modules, code logic and variables and how to add external facts to your systems. Besides this I will introduce parameters and the concept of separating code and data by using hiera.

The third part will explain how to make use of upstream Puppet libraries when describing your own infrastructure, how to best classify nodes and where to place the code.

At the last posting I will combine what I have shown and how to make use of the example42 [PSICK control repository](https://github.com/example42/psick.git), the [PSICK module](https://github.com/example42/puppet-psick.git) and the [PSICK hieradata](https://github.com/example42/psick-hieradata).

* Table of content
{:toc}

#### Introduction

[Puppet](https://puppet.com) is a client-server based configuration management solution written in Ruby (Agent) and Java (Server).
When using Puppet, you write a declarative description of your systems and infrastructure. This means that you are not providing information on how to change something, but you describe the desired configuration state, e.g. by providing the complete configuration file.

The declarative description is done by using resource types like `user`, `group`, `package`, `file`, `service`, `cron`, `mount`. We are going to explain these within this posting.

Your infrastructure description must be written in Puppet [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) code. The files in which you place your code are called Puppet manifests.

Puppet allows you to run even without a central Puppet server. This usage of Puppet is called Masterless Puppet and will be our starting point - even for setting up our Puppet server. 

The Puppet server can only run on Linux based systems (see [Puppetserver Supported Platforms](https://puppet.com/docs/puppetserver/latest/services_master_puppetserver.html#supported-platforms)). The Puppet agent supports a large variety of [different operating systems](https://puppet.com/docs/puppet/latest/system_requirements.html) like Linux, Windows, OS X and macOS, Juniper, Arista, BSD.

#### Puppet installation

You start with installing Puppet agent on a Linux system. This tutorial uses CentOS 7, descriptions on how to install Puppet agent on other Linux distributions can be found on the [Puppet Platform](https://puppet.com/docs/puppet/latest/puppet_platform.html) website.

As the first system also will become your Puppet server, you have to take care on proper hardware sizing. A Puppet server should have at least 2-4 GB of RAM and at least 1-2 CPU cores. The harddisk should have enough space to hold your code, plus information and reports from your agents. Usually Puppet recommends 100 GB free space. Further information can be found on the [Puppet Server Installation](https://puppet.com/docs/puppetserver/latest/install_from_packages.html) page.

Note: in larger environments (more than 400 nodes) a Puppet server should have 4-12 cores and 12 to 24 GB RAM.

Some Linux distributions have Puppet packages added to their repositories. Usually the shipped versions are outdated - sometimes even without security fixes from Puppet.

At the time of writing this posting, Puppet has recently released version 5.5.
You will therefor use the Puppet repositories to install the agent using root user account:

    rpm -Uvh https://yum.puppetlabs.com/puppet5/puppet5-release-el-7.noarch.rpm

Now you can install the Puppet Agent package:

    yum install puppet-agent

The Puppet Agent package installs into `/opt/puppetlabs` directory and has everything the Puppet Agent needs bundled inside:

- ruby
- openssl

The configuration files for Puppet agent are located in `/etc/puppetlabs/puppet`. The main configuration file is the `puppet.conf` file. You will leave this file untouched as you also want to manage the Puppet setup in an automated way.

#### Puppet and Facter

Now you already have everything required to start playing and working with Puppet.

The Puppet binary is located at `/opt/puppetlabs/puppet/bin/puppet`. The installer provides a profile.d snippet in `/etc/profile.d/puppet-agent.sh` which add the puppet binary path to the PATH environment variable. You can either log out and log in again or refresh your shell by running `exec bash`.

The puppet binary has several subcommands like `agent`, `apply`, `describe`, `resource`, `...`.

A complete list of commands can be found when running `puppet --help`.

At the beginning you use the `puppet describe` command. This command prints the documentation which is part of the Puppet code. When running `puppet describe --list` you will receive a list of all available resource types on your system. At the moment these will be the built in [Puppet Types](https://puppet.com/docs/puppet/latest/type.html).

You can either refer to the online documentation or print the documentation using `puppet describe <resource type>`.

As you now know about existing resource types, you are able to use the `puppet resource` command to read existing resources and print them in Puppet DSL code.

Read a user resource:

    # puppet resource user root
    user { 'root':
      ensure           => 'present',
      comment          => 'root',
      gid              => 0,
      home             => '/root',
      password         => '$1$FQDy6m9T$5JJ5fqv9ylivZNQIj5Eet0',
      password_max_age => 99999,
      password_min_age => 0,
      shell            => '/bin/bash',
      uid              => 0,
    }

Read a package resource:

    # puppet resource package puppet-agent
    package { 'puppet-agent':
      ensure => '5.5.0-1.el7',
    }

Read a file resource:

    # puppet resource file /etc/motd
    file { '/etc/motd':
      ensure   => 'file',
      content  => '{md5}d41d8cd98f00b204e9800998ecf8427e',
      ctime    => '2017-09-11 18:34:44 +0000',
      group    => 0,
      mode     => '0644',
      mtime    => '2013-06-07 14:31:32 +0000',
      owner    => 0,
      selrange => 's0',
      selrole  => 'object_r',
      seltype  => 'etc_t',
      seluser  => 'system_u',
      type     => 'file',
    }

Read a servcie resource:

    # puppet resource service puppet
    service { 'puppet':
      ensure => 'stopped',
      enable => 'false',
    }

Read a mount resource:

    # puppet resource mount /
    mount { '/':
      ensure  => 'mounted',
      device  => '/dev/mapper/VolGroup00-LogVol00',
      dump    => '0',
      fstype  => 'xfs',
      options => 'defaults',
      pass    => '0',
      target  => '/etc/fstab',
    }

As you can see Puppet always uses the same layout and syntax for resources:

    <resource_type> { '<resource title>':
      parameter  => 'value',
      parameter2 => 'other value',
    }

This pattern is named a "resource type declaration".

Another important utility which is part of the pupept agent package is `facter`. `facter` collects different system information covering hardware (RAM, CPU, manufacturer), network (interfaces, IPv4 and IPv4 addresses), operating system (name, version) and many more.

You can print the whole set of information by running `facter` on the command line as root user.
A single element can be read when adding the fact name: `facter os`, `facter networking`.

    # facter os
	{
	  architecture => "x86_64",
	  family => "RedHat",
	  hardware => "x86_64",
	  name => "CentOS",
	  release => {
	    full => "7.4.1708",
	    major => "7",
	    minor => "4"
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

#### Start with Puppet DSL

Now let's start using Puppet and prepare the system to become our Puppet master.

At the moment there are only a couple of things to do: install the package `puppetserver` and start the process. Let's additionally place the information that this is the puppet server into `/etc/motd`.
You are now writing your first Puppet manifest:

    # /root/puppetserver.pp
    # install puppetserver package
    package { 'puppetserver':
      ensure => present,
    }
    # ensure that puppetserver is running and started at reboot
    service { 'puppetserver':
      ensure => running,
      enable => true,
    }
    # put information into motd
    file { '/etc/motd':
      ensure  => file,
      content => "This is Puppet Server\n",
    }

As you can see I have omitted the single quotes around the words `present`, `running` and `true`.
Maybe it is obvious why I am not quoting the bool value. But what about the others? There are some special words within Puppet which do not need quoting. Mostly these are [Ruby Symbols](https://ruby-doc.org/core-2.2.0/Symbol.html).

At the file resource I am managing the content. This is easy to do for small configuration files, but leads to hard to read Puppet code when it comes to larger configuration files. In Part 2 I will introduce another solution for providing file content.

But how do you now "execute" the manifest we have written?

First: in Puppet you never "execute" something. Instead you want to apply a specifc declaration onto a system. This is done by Puppet first parsing the manifest and rendering it into a catalog. This process is called "catalog compile".
No worries, this is not binary code, the Puppet compiler returns minified JSON to the Puppet agent, who will then start working on the returned catalog.

#### Puppet apply

As you are not (yet) having a Puppet master you must run Puppet in masterless mode. This is possible by running `puppet apply` and providing the filename.

    # puppet apply /root/puppetserver.pp

Now you have Puppet server process listening on Port 8140 and you can start adding other systems to your Puppet server.

But there is one more thing: what happens if you run the puppet apply command again?

    # puppet apply /root/puppetserver.pp

As you can see, nothing happens. This concept is called [idempotence](https://en.wikipedia.org/wiki/Idempotence). Puppet will always first check the actual system state, compare it with the desired declarative state and only perform actions in case that there is a mismatch.

#### Puppet CA and Puppet agents

Puppet uses client SSL certificates to authenticate and authorize Puppet agent connections to the Puppet server process. Per default the Puppet server uses a self signed CA to retrieve certificate signing requests and sign certificates.

Information about the Puppet CA can be read using the `puppet cert` command.

    # puppet cert list --all

You can even read the CA by using the print parameter:

    puppet cert print puppetmaster.domain.com
    [... output truncated ...]

In the next posting we will dig deeper into Puppet DSL, how to write flexible Puppet code instead of writing per node Puppet code, how to make use of existing Puppet module libraries how to deal with slight differences between systems and how to store Puppet code and Puppet data.

Martin Alfke
