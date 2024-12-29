---
number: '1'
layout: 'presentation'
title: 'Puppet Essentials. A tutorial on what you need to know about Puppet'
date: '20241229'
host: Alessandro Franceschi
tags:
  - Puppet
  - Infrastructure as Code
  - DevOps
---

### Introduction to Puppet

An introduction to Configuration Management tools, their principles and role in a \[DevOps\] tool chain.

An overview of Puppet and its ecosystem, composed of different tools and endless integrations.

A guided reference of Puppet learning resources, online references and core concepts.

### Language Basics

General overview of Puppet DSL with examples of common resources.

Modules principles and usage patterns.

### Using Puppet

A basic outline of Puppet installation and usage modes.

A review of what happens during a Puppet run.

### Appendix

A brief history of Puppet versions.

Some hints on Puppet 4 migration.

An overview of Hiera

Introduction
============

Contents
--------

*   What is Puppet?
*   Configuration management
*   Learning References
*   Puppet ecosystem
*   Essential Puppet concepts

Take-aways
----------

*   Know what is Puppet
*   Understand the principles behind configuration management tools
*   Know where to find information about Puppet
*   Have a general view of Puppet software ecosystem
*   Understand the logic and core principles of Puppet

What is Puppet?
===============

Puppet is an Open Source **Configuration Management** software developed by [Puppet Labs](http://www.puppetlabs.com)

More widely Puppet is a framework for **Systems Automation** since it automates the configuration and ongoing management of our servers, in a centrally managed way.

It allows to define, with a **declarative** Domain Specific Language (**DSL**), what we want to configure and manage on an Operating System (OS): packages to install, services to start, files to configure and any system resource we can map and express in Puppet language.

Puppet works on Linux, Unix (Solaris, AIX, \*BSD), MacOS, Windows ([List of Supported Platforms](http://docs.puppetlabs.com/guides/platforms.html)) and can be used also to configure network and storage devices or manage cloud resources.

It is used by [many companies](http://puppetlabs.com/customers/companies/) with a number of managed systems than ranges from few dozens to several thousands.

Puppet Labs releases also [Puppet Enterprise](https://puppetlabs.com/puppet/puppet-enterprise) (**PE**) based on the [Open Source code base](https://github.com/puppetlabs/puppet) and oriented to enterprises that need official support and want Puppet infrastructure easier to setup and with better reporting and management features.

DevOps and Configuration management
===================================

DevOps is a [term](https://en.wikipedia.org/wiki/DevOps) that involves a remarkable number of concepts, nuances and definitions.

We won't try to give another one, but we can safely say that DevOps is (also) about **culture**, **processes**, **people** and **tools**.

A complete [DevOps tools chain](https://xebialabs.com/the-ultimate-devops-tool-chest/) contains software of these categories:

*   Source Code Management (<- We use them when writing Puppet code)
*   Repository and software Management (<- Puppet can configure them)
*   Software build (<- Puppet can configure them)
*   Configuration Management (**<- Puppet is here**)
*   Testing (<- We can test our Puppet code)
*   Monitoring and data analysis (<- Puppet can configure them)
*   Systems and Applications Deployment (<- Puppet can be also here)
*   Continuous integration (<- We can manage Puppet code deployments in a CI pipeline)
*   Cloud (<- Puppet code can manage cloud resources)
*   Project management and Issue tracking (<- We can use them to manage our Puppet projects)
*   Messaging and Collaboration (<- We can use them to collaborate on Puppet works)
*   Containerization and Virtualization (<- Puppet can configure them)
*   Databases (<- Puppet can configure them)
*   Application servers (<- Puppet can configure them)

Configuration Management principles
===================================

Configuration management tools allow to programmatically define how servers have to be configured. Their main benefits are:

*   **Automation**: No need to manually configure systems
*   **Reproducibility**: Setup once, repeat forever
*   **Scale**: Done for one, use on many
*   **Coherent** and consistent server setups
*   **Aligned Environments** for devel, test, qa, prod nodes

Configuration management tools typically describe the systems setups via code or data (**Infrastructure as Code**), this involves a paradigm change in system administration:

*   Systems are managed **centrally** in an **automated** way: no more manually
*   Code is versioned with a Source Control Management tool (**git** is the most used in Puppet world)
*   Commits history shows the **history of change** on the infrastructure (who, what, when and why)
*   Code can be **tested** before deployment in production
*   Code has to be **deployed**

Configuration Management tools
==============================

Common alternatives to Puppet:

#### [Chef](https://www.chef.io/)

*   Has Chef clients that connect to Chef server
*   Has characteristic similar to Puppet
*   Community code is shared on the [Chef Supermarket](https://galaxy.ansible.com/intro#review)
*   Chef code is Ruby with dedicated extensions
*   Software developed in Ruby.

#### [CFEngine](http://cfengine.com/)

*   The first and oldest of the bunch
*   CFEngine3 is a complete and modern rework
*   Different daemons for different functions in a distributed environment
*   Based on the [Promise theory](https://en.wikipedia.org/wiki/Promise_theory)
*   Cfengine code is a test based list of pro
*   Software developed in C by Prof. Mark Burgess.

#### [Salt](http://saltstack.com/)

*   Manages deployments on multiple clouds in a fast way
*   Salt code is composed of states (Puppet resources) written in YAML files
*   [Formulas](https://github.com/saltstack-formulas) are equivalent to modules
*   Sotfware developed in Python

#### [Ansible](http://www.ansibleworks.com/)

*   Quick setup, no agents, communications over SSH
*   Ansible code is YAML based and written on playbooks
*   Roles are equivalent to modules, they are shared on the [Ansible Galaxy](https://galaxy.ansible.com/intro#review)
*   Can centralise multi node task executions, software deployments and configuration management.
*   Software eveloped in Python. Bought by RedHat in October 2015

Learning resources
==================

Useful resources to start learning Puppet:

*   The website of [Puppet Labs](http://puppetlabs.com), the company behind Puppet
*   The official [Puppet Documentation site](http://docs.puppetlabs.com/) -
*   The Learning VM, based on Puppet Enterprise, for a guided tour in Puppet world
*   A list of the available [Puppet Books](https://puppetlabs.com/resources/books)

If you have questions to ask about Puppet usage use these:

*   All the [Puppet Community](http://puppetlabs.com/community/overview/) references
*   [Ask Puppet](http://ask.puppetlabs.com/), the official Q&A site
*   The discussion groups on Google Groups: [puppet-users](https://groups.google.com/forum/#!forum/puppet-users), [puppet-dev](https://groups.google.com/forum/#!forum/puppet-dev), [puppet-security-announce](https://groups.google.com/forum/#!forum/puppet-security-announce)

To explore and use existing Puppet code:

*   Puppet modules on [Module Forge](http://forge.puppetlabs.com)
*   Puppet modules on [GitHub](https://github.com/search?q=puppet)

To inform yourself about what happens in Puppet World

*   [Planet Puppet](http://www.planetpuppet.org/) - Puppet blogosphere
*   The [PuppetConf](http://www.puppetconf.com) website
*   The ongoing PuppetCamps all over the world

To find more and deeper information:

*   [Puppet Labs tickets](https://tickets.puppetlabs.com) - The official ticketing system
*   [Developer reference](http://docs.puppetlabs.com/references/latest/developer/) - The commented Puppet code
*   [Puppet Stats](http://bitergia.dev.puppetlabs.com/browser/) - Puppet relate metrics and stats

Essential Puppet concepts
=========================

When approaching Puppet it's important to understand it's basic concepts and terminology.

A complete official [glossary](http://docs.puppetlabs.com/references/glossary.html) is online, use it.

Here we outline a few essential Puppet concepts, be sure to understand them all:

*   A typical Puppet setup is based on a client-server architecture: the client is also called **agent** (or **agent node** or simply **node**), the server is called **master**
*   When the puppet client connects to the server, it sends it's own ssl **certname** and a list of **facts** (units of information about the client's system generated by the command **facter**)
*   Based on the client **certname** and its facts, the master replies with a **catalog** that describes what has to be configured on the client
*   The catalog is based on Puppet code, which is written in **manifests** (files with **.pp** extension)
*   In the Puppet code we declare **resources** that affect elements of the system (files, packages, services ...)
*   Resources are grouped in **classes** which may expose **parameters** that affect their behavior.
*   The values of the class parameters can be defined in different ways, one of them is **Hiera**
*   **Hiera** is a very common and versatile tool to store the values of parameters
    
*   Classes and the configuration files that are shipped to nodes are organized in **modules**.
    

Puppet ecosystem
================

Puppet Labs software products
-----------------------------

Puppet ecosystem is composed of many software projects. The ones developed by PuppetLabs are:

*   [Puppet](http://docs.puppetlabs.com/puppet/) - Official Puppet Open Source documentation
*   [Puppet Enterprise](http://docs.puppetlabs.com/pe/) - The commercial enterprise version of Puppet
    
*   [Facter](http://docs.puppetlabs.com/facter/) - Complementary tool to retrieve system's data
    
*   [Puppet Server](http://docs.puppetlabs.com/puppetserver/) - The next generation server service
    
*   [Hiera](http://docs.puppetlabs.com/hiera/) - Key-value lookup tool where Puppet data can be placed
    
*   [PuppetDB](http://docs.puppetlabs.com/puppetdb/) - Stores all the data generated by Puppet
    
*   [MCollective](http://docs.puppetlabs.com/mcollective/) - Infrastructure Orchestration framework
    
*   [Razor](http://docs.puppetlabs.com/pe/latest/razor_intro.html/) - A provisioning system
    
*   [Geppetto](http://puppetlabs.github.io/geppetto/) - A Puppet IDE based on Eclipse
    
*   [r10k](https://github.com/puppetlabs/r10k/) - A tool to manage deployments of Puppet code
    

Puppet ecosystem
================

Community resources
-------------------

Soe of the most known Puppet related community projects are:

*   [Puppet Community](https://puppet.community/) - Modules and tooling for and by the Puppet Community
*   [Puppet CookBook](http://www.puppetcookbook.com/) - A collection of task oriented solutions in Puppet
*   [Puppet DashBoard](https://github.com/sodabrew/puppet-dashboard/) - A Puppet _Web frontend_ and External Node Classifier (ENC)
*   [The Foreman](http://theforeman.org/) - A well-known third party provisioning tool and Puppet ENC
*   [PuppetBoard](https://github.com/puppet-community/puppetboard) - A web frontend for PuppetDB
*   [Puppet Lint](http://puppet-lint.com/) - A tool to check Puppet code style
*   [Rspec Puppet](http://rspec-puppet.com/) - A tool to make unit tests of Puppet code
*   [Kermit](http://www.kermit.fr/) - A web frontend for MCollective

Language Basics
===============

Contents
--------

*   Nodes classification
*   The Catalog
*   Variables and parameters
*   Resource types
*   Classes and defines
*   Modules

Take-aways
----------

*   Understand how Puppet delivers the right configurations to each node
*   Know what is the Catalog
*   Understand usage of variables and facts
*   Know how is declared a Puppet resource
*   Understand the RAL (Resource ABstraction Layer) principles
*   Know how are Puppet classes and defines
*   Understand modules structure, usage and paths conventions
*   Know how to write erb templates

Nodes classification
====================

When clients connect, the Puppet Master generates a **catalog** with the list of the resources that clients have to apply locally.

The Puppet Master has to _classify_ nodes and define for each of them:

*   The **classes** to include
*   The **parameters** to pass
*   The Puppet **environment** to use

Nodes classification can be done in different ways (more details will follow):

*   Using the `node` definition in Puppet code
*   Using and **External Node Classifier** (ENC): a separated tool that provides classification info
*   Using the `hiera_include` function
*   Using a nodeless setup: the classes to include are defined according to variables and facts.

The Catalog
===========

The **catalog** is the complete list of resources, and their relationships, that the Puppet Master generates for the client and sends it in Json format.

It's the result of all the puppet code and logic that we define for a given node in our manifests and is applied on the client after it has been received from the master.

The client uses the RAL (Resource Abstraction Layer) to execute the actual system's commands that convert abstract resources like

    package { 'openssh': }
    

to their actual fulfillment on the system, such as

    apt-get install openssh # On Debian derivatives
    yum install openssh     # On RedHat derivatives
    

The catalog is saved by the client in:

    $libdir/client_data/catalog/$certname.json
    

Resource Types (Types)
======================

Resource Types are single **units of configuration** composed by:

*   A **type** (package, service, file, user, mount, exec ...)
*   A **title** (how is called and referred)
*   Zero or more **arguments**

The syntax is as follows:

    type { 'title':
      argument  => value,
      other_arg => value,
    }
    

Example for a **file** resource type:

    file { 'motd':
      path    => '/etc/motd',
      content => 'Tomorrow is another day',
    }
    

Resource Types reference
========================

Find online the complete [Type Reference](http://docs.puppetlabs.com/references/latest/type.html) for the latest or earlier versions.

From the shell the command line interface:

    puppet describe file
    

For the full list of available descriptions try:

    puppet describe --list
    

Give a glance to Puppet code for the list of **native** resource types:

    ls $(facter rubysitedir)/puppet/type
    

The most common native resources, shipped with Puppet by default are: package, service, file, user, group, cron, exec, mount...

Simple samples of resources
===========================

Installation of OpenSSH package:

    package { 'openssh':
      ensure => present,
    }
    

Creation of /etc/motd file:

    file { 'motd':
      path => '/etc/motd',
    }
    

Start of httpd service:

    service { 'httpd':
      ensure => running,
      enable => true,
    }
    

Creation of oscar user:

    user { 'oscar':
      ensure => present,
      uid    => 1024,
    }
    

Each of these resources have several other arguments that allows to define every characteristic of the resource.

More complex examples
=====================

Here are some more complex examples with usage of variables, resource references, arrays and relationships.

Management of nginx service with parameters defined in module's variables

    service { 'nginx':
      ensure     => $::nginx::manage_service_ensure,
      name       => $::nginx::service_name,
      enable     => $::nginx::manage_service_enable,
    }
    

Creation of nginx.conf with content retrieved from different sources (first found is served)

    file { 'nginx.conf':
      ensure  => present,
      path    => '/etc/nginx/nginx.conf',
      source  => [
          "puppet:///modules/site/nginx.conf--${::fqdn}",
          "puppet:///modules/site/nginx.conf"
      ],
    }
    

Installation of the Apache package triggering a restart of the relevant service:

    package { 'httpd':
      ensure => $ensure,
      name   => $apache_package,
      notify => Class['Apache::Service'],
    }
    

Resource Abstraction Layer
==========================

Resources are abstracted from the underlying OS, this is achieved via the **Resource Abstraction Layer** (RAL) composed of resource **types** that can have different **providers**.

A type specifies the attributes that a given resource may have, a provider implements the relevant type on the underlying Operating System.

For example the `package` type is known for the great number of providers (yum, apt, msi, gem ... ).

    ls $(facter rubysitedir)/puppet/provider/package
    

With the command `puppet resource` we can represent the current status of a system's resources in Puppet language (note this can be done for any resource, even the ones not managed by Puppet):

To show all the exisiting users on a system (or only the root user):

    puppet resource user
    puppet resource user root
    

To show all the installed packages:

    puppet resource package
    

To show all the system's services:

    puppet resource service
    

It's also possible to directly modify them with `puppet resource` (note that this is not generally the way Puppet is used to manage the system's resources):

    puppet resource service httpd ensure=running enable=true
    

Variables
=========

Variables is Puppet codes are basically **constants**: once defined in a class we can't change them.

We can set variables in our Puppet code with this syntax:

    # Normal variable assignment
    $role = 'mail'
    
    # The value of a variable is based on another variable (here used the **selector** costruct)
    $package = $::operatingsystem ? {
      /(?i:Ubuntu|Debian|Mint)/ => 'apache2',
      default                   => 'httpd',
    }
    

Puppet automatically provides also some **internal** variables, the most common are:

    # The name of the node (the certname setting in its puppet.conf)
    $clientcert # Default is the client's Fully Qualified Domain Name)
    
    # The Puppet's environment where the Master looks for the code to compile
    $environment # Default is "production"
    
    # The Master's FQDN and IP address
    $servername $serverip
    
    # Any configuration setting of the Puppet Master's puppet.conf
    $settings::<setting_name>:
    
    # The name of the module that contains the current resource's definition
    $module_name
    

Facter and facts
================

**Facter** is a tools shipped with Puppet. It runs on clients and collects **facts** which are sent to the server. In our code we can use facts to manage resources in different ways or with different arguments.

Here follows a list of the most common and useful facts:

    al$ facter
    
    architecture => x86_64
    fqdn => Macante.example42.com
    hostname => Macante
    ipaddress_eth0 => 10.42.42.98
    macaddress_eth0 => 20:c9:d0:44:61:57
    operatingsystem => Centos
    operatingsystemrelease => 6.3
    osfamily => RedHat
    virtual => physical
    

It's easy to create custom facts. They can be of 2 types:

*   **Native facts** written in ruby and shipped with modules (in the `lib/facter` directory)
*   **External facts** can be simple ini-file like texts (with `.txt` extension), Yaml files or even commands in any language, which returns a fact name and its value. External facts are located in the nodes' `/etc/facter/facts.d` directory and can be shipped also from modules (in the `facts.d` directory)

Classes
=======

Classes are **containers** of different resources. Since Puppet 2.6 they can have parameters.

Example of a class **definition** (here we describe what the class does and what parameters it has, we don't actually add it and its resources to the catalog):

    class mysql (
      root_password = 'default_value',
      port          = '3306',
    ) {
      package { 'mysql-server': ensure => present }
      service { 'mysql': ensure => running }
      [...]
    }
    

When we have to use a class previously defined, we **declare** it. Class declaration can be done in 2 different ways:

"Old style" class declaration, without parameters (inside a catalog we can have multiple `include` of the same class but that class it's applied only once):

    include mysql
    

"New style" (from Puppet 2.6) class declaration with explicit parameters (Syntax is the same of normal resources and the same class can be declared, in this way, only once inside the same catalog):

    class { 'mysql':
      root_password => 'my_value',
      port          => '3307',
    }
    

Defines
=======

Also called: **Defined resource types** or **defined types**

Similar to parametrized classes but can be used multiple times (with different titles).

**Definition** of a define:

    define apache::virtualhost (
      $ensure   = present,
      $template = 'apache/virtualhost.conf.erb' ,
      [...] ) {
    
      file { "ApacheVirtualHost_${name}":
        ensure  => $ensure,
        content => template("${template}"),
      }
    }
    

**Declaration** of a define:

    apache::virtualhost { 'www.example42.com':
      template => 'site/apache/www.example42.com-erb'
    }
    

Modules
=======

Self Contained and Distributable _recipes_ contained in a directory with a predefined structure

Used to manage an application, system's resources, a local site or more complex structures

Modules must be placed in the Puppet Master's modulepath

    puppet config print modulepath
    /etc/puppet/modules:/usr/share/puppet/modules
    

Puppet module tool to interface with Puppet Modules Forge

    puppet help module
    [...]
    ACTIONS:
      build        Build a module release package.
      changes      Show modified files of an installed module.
      generate     Generate boilerplate for a new module.
      install      Install a module from the Puppet Forge or an archive.
      list         List installed modules
      search       Search the Puppet Forge for a module.
      uninstall    Uninstall a puppet module.
      upgrade      Upgrade a puppet module.
    

GitHub, also, is full of Puppet modules

Paths of a module
=================

Modules have a standard structure:

    mysql/            # Main module directory
    
    mysql/manifests/  # Manifests directory. Puppet code here.
    mysql/lib/        # Plugins directory. Ruby code that extends Puppet here.
    mysql/templates/  # ERB and EPP Templates directory
    mysql/files/      # Static files directory
    mysql/spec/       # Puppet-rspec directory
    mysql/tests/      # Tests / Usage examples directory
    
    mysql/Modulefile  # Module's metadata descriptor
    

This layout enables useful conventions

Modules paths conventions
=========================

Classes and defines autoloading:

    include mysql
    # Main mysql class is placed in: $modulepath/mysql/manifests/init.pp
    
    include mysql::server
    # This class is defined in: $modulepath/mysql/manifests/server.pp
    
    mysql::conf { ...}
    # This define is defined in: $modulepath/mysql/manifests/conf.pp
    
    include mysql::server::ha
    # This class is defined in: $modulepath/mysql/manifests/server/ha.pp
    

Provide files based on Erb Templates (Dynamic content)

    content => template('mysql/my.cnf.erb'),
    # Template is in: $modulepath/mysql/templates/my.cnf.erb
    

Provide static files (Static content). Note we can't use content AND source for the same file.

    source => 'puppet:///modules/mysql/my.cnf'
    # File is in: $modulepath/mysql/files/my.cnf
    

ERB templates
=============

Files with .erb extension used typicall by in `file` resources.

Inside these files ruby code can be interpolated inside the `<%` and `%>` tags.

Example of an erb template:

    # Show facts values
    hostname = <%= @::fqdn %>
    
    # Show values of variables outside local scope, two methods:
    ntp_server = <%= scope.lookupvar('::ntp::server') %>
    ntp_server = <%= scope['::ntp::server'] %>
    
    # Iteration over an array
    <% @::dns_servers.each do |ns| %>
    nameserver <%= ns %>
    <% end %>
    
    # Conditional blocks of texts
    <% if scope.lookupvar('puppet::db') == "puppetdb" -%>
    storeconfigs_backend = puppetdb
    <% end -%>
    

Note the ending `-%>`: when dash is present, no new line is introduced on the generated file.

Practice: Language Basics
=========================

On a test machine **install Puppet** if not already installed.

Practice with the **commands**:

    puppet describe
    puppet resource
    facter
    

Create a **manifest** file and in that file manage the installation of the package and the management of the service of _nginx_.

Use `puppet apply` to apply the resources declared in our manifest.

Using Puppet
============

Contents
--------

*   Installation of different Puppet versions
*   Configuration files and parameters
*   Puppet cli commands
*   Files paths
*   Troubleshooting

Take-aways
----------

*   Know how to install different versionf of Puppet
*   Know where to find the most important files
*   Understand the basics of Puppet configuration
*   Understand Puppet run modes (agent/apply)
*   Use puppet command
*   Have to basics to troublshoot Puppet

Open Source Puppet Puppet installation
======================================

Puppet can be found by default in most distributions.

It generally recommended to use [Puppet Labs repositories](http://docs.puppetlabs.com/guides/puppetlabs_package_repositories.html) for the latest updates.

Check the [Installation Instructions](http://docs.puppetlabs.com/guides/installation.html) for different OS.

Puppet 3.x installation
-----------------------

On Debian and derivates, you can install it with:

    apt-get install puppet       # On clients (nodes)
    apt-get install puppetmaster # On server (master)
    

On RedHat and derivates you need to add the EPEL repository or RHN Extra channel:

    yum install puppet        # On clients (nodes)
    yum install puppet-server # On server (master)
    

Puppet 4 installation
---------------------

Puppet version 4 can be installed using [Puppet Labs Software Collections](https://puppetlabs.com/blog/welcome-puppet-collections), once added the relevant repositories for your distro you can install it with:

    [apt-get|yum] install puppet-agent   # On clients (nodes)
    [apt-get|yum] install puppet-server  # On server (master)
    

Puppet Enterprise installation
==============================

For complete installation instruction check the [Official Documentation](https://docs.puppetlabs.com/pe/latest/install_basic.html)

Puppet Enterprise is licenced software, you can request an trial version from [the Download page](https://puppetlabs.com/download-puppet-enterprise), it's free up to 10 managed nodes

Puppet Enterprise Server setup
------------------------------

*   Get the tar from [the Download page](https://puppetlabs.com/download-puppet-enterprise)
    
*   Unpack and run:
    
    tar -xf cd sudo ./puppet-enterprise-installer
    
*   Via browser open `https://<server_name>:3000` and follow up with web based installation (don't close your installer terminal window)
    
*   Choose between **all in one** installation or split installation, set the puppet server certname and aliases, set the console admin password and other installation options
    
*   Once installed, open the **Puppet Enterprise Console** via browser at `https://server_name>`, with user **admin** and the password set before
    

Puppet Enterprise agent setup
-----------------------------

Check the official [install client documentation](http://docs.puppetlabs.com/pe/latest/install_agents.html) for complete reference.

Different alternatives:

*   Run the remote installation script:
    
        curl -k https://<puppet_server>:8140/packages/current/install.bash | sudo bash
        
    
*   Distribute the tarball and eventually use an answer file for unattended setup:
    
        sudo ./puppet-enterprise-installer -a ~/pe_answers.txt
        
    
*   Use dedicated public modules
    

Puppet configuration: puppet.conf
=================================

It's Puppet main configuration file.

On open source Puppet 3 is generally in:

    /etc/puppet/puppet.conf
    

On Puppet Enterprise and Puppet 4 is in:

    /etc/puppetlabs/puppet/puppet.conf
    

On Windows is in:

    C:\ProgramData\PuppetLabs\puppet\etc
    

When running as a normal user can be placed in the home directory:

    /home/<user>/.puppet/puppet.conf
    

Configurations are divided in \[stanzas\] for different Puppet sub commands

Common for all commands: **\[main\]**

For puppet agent (client): **\[agent\]** (Was \[puppetd\] in Puppet pre 2.6)

For puppet apply (client): **\[user\]** (Was \[puppet\])

For puppet master (server): **\[master\]** (Was \[puppetmasterd\] and \[puppetca\])

Hash sign (#) can be used for comments.

Main configuration options
==========================

To view all or a specific configuration setting:

    puppet config print all
    puppet config print modulepath
    

Important options under **\[main\]** section:

    vardir = /var/lib/puppet # Path where Puppet stores dynamic data.
    ssldir = $vardir/ssl # Path where SSL certifications are stored.
    

Important options Under **\[agent\]** section:

    server = puppet.example42.com # Host name of the PuppetMaster. (Default: puppet)
    certname = web01.example42.com # Certificate name of the client. (Default is its fqdn)
    runinterval = 60 # Number of minutes between Puppet runs, when running as service. (Default: 30)
    report = true # If to send Puppet runs' reports to the **report_server**. (Default: true)
    

Important options under **\[master\]** section:

    autosign = /etc/puppet/autosign.conf # If new clients certificates are automatically signed. (Default: false)
    reports = puppetdb # How to manage clients' reports (Default: store)
    storeconfigs = true # If to enable store configs to support exported resources. (Default: false)
    

Full [configuration reference](http://docs.puppetlabs.com/references/latest/configuration.html) on the official site.

Using the Puppet command
========================

Puppet has different subcommands for different purproses. It's possible to add seamlessly new commands using the **face** interface.

    puppet help
    
    Usage: puppet <subcommand> [options] <action> [options]
    
    Available subcommands: (here shown the most used ones)
    
    agent             The puppet agent daemon
    apply             Apply Puppet manifests locally
    ca                Local Puppet Certificate Authority management.
    cert              Manage certificates and requests
    config            Interact with Puppet's settings.
    describe          Display help about resource types
    device            Manage remote network devices
    doc               Generate Puppet references
    facts             Retrieve and store facts.
    master            The puppet master daemon
    module            Creates, installs and searches for modules on the Puppet Forge.
    node              View and manage node definitions.
    parser            Interact directly with the parser.
    resource          The resource abstraction layer shell
    

Puppet operational modes
========================

Master / Client - puppet agent
------------------------------

It's the typical Puppet setup

*   We have clients, our managed nodes, where Puppet agent is installed.
    
*   We have one or more Masters where Puppet server runs as a service
    
*   Client/Server communication is via https (**port 8140**)
    
*   Clients certificates have to be accepted (**signed**) on the Master
    
*   Command used on the client: `puppet agent` (generally as **root**)
    
*   Command used on the server: `puppet master` (generally as **puppet**)
    

Masterless - puppet apply
-------------------------

Master less mode doesn't use a client-server infrastructure.

*   Our Puppet code (written in manifests) is applied directly on the target system.
    
*   No need of a Puppet Master
    
*   We have to distribute our modules and data to the managed nodes.
    
*   Command used: `puppet apply` (generally as **root**)
    

Puppet paths
============

The paths of the most important locations are different on Puppet versions on Linux systems. Check the [Official specification](https://github.com/puppetlabs/puppet-specifications/blob/master/file_paths.md) for all the details.

Configuration directory (`$confdir`):

    /etc/puppet/            # Puppet 3 or earlier
    /etc/puppetlabs/puppet/ # Puppet 4 and PE
    

Log directory (`$logdir`):

    /var/log/puppet # Puppet 3 or earlier
    /var/log/puppetlabs/puppet # Puppet 4
    

Lib directory (`$libdir`) (contains Puppet operational data such as catalog, backup of files...):

    /var/lib/puppet # Puppet 3 or earlier
    /opt/puppetlabs/puppet/lib # Puppet 4
    

SSL directory (`$libdir`) (contains all the SSL certificates)

    $libdir/ssl  # Puppet 3 or earlier
    $confdir/ssl # Puppet 4
    

Manifest file (the first manifest parsed by the Master when compiling the catalog

    /etc/puppet/manifests/site.pp # Puppet 3 with config-file environments
    /etc/puppet/environments/$environment/manifests/site.pp # Puppet 3 with directory environments
    /etc/puppetlabs/code/environments/$environment/manifests/site.pp # Puppet 4
    

Modulepath (comma separated directories where modules are stored):

    /etc/puppet/modules:/usr/share/puppet/modules # Puppet 3
    /etc/puppet/environments/$environment/modules # Added modules dir in Puppet 3 when using **directory environments**
    /etc/puppetlabs/code/environments/$environment/modules # Puppet 4
    

Code directory in Puppet 4:

    /etc/puppetlabs/code # $codedir
    /etc/puppetlabs/code/environments/$environment # $environmentpath
    

Inside the $environmentpath

    hieradata/ # Hiera files dir
    modules/   # User modulepath    
    manifests/ # Manifests dirs
    environment.conf
    

Anatomy of a Puppet Run
=======================

Execute Puppet on the client

    Client shell # puppet agent -t
    

If pluginsync = true (default from Puppet 3.0) the client retrieves all extra plugins (facts, types and providers) present in modules on the server's $modulepath

    Client output # Info: Retrieving plugin
    

The client runs facter and send its facts to the server

    Client output # Info: Loading facts in /var/lib/puppet/lib/facter/... [...]
    

The server looks for the client's hostname (or certname, if different from the hostname) and looks into its nodes list

The server compiles the catalog for the client using also client's facts.

    Server's logs # Compiled catalog for <client> in environment production in 8.22 seconds
    

If there are not syntax errors in the processed Puppet code, the server sends the catalog to the client, in PSON format.

    Client output # Info: Caching catalog for <client>
    

The client receives the catalog and starts to apply it locally If there are dependency loops the catalog can't be applied and the whole tun fails.

    Client output # Info: Applying configuration version '1355353107'
    

All changes to the system are shown here. If there are errors (in red or pink, according to Puppet versions) they are relevant to specific resources but do not block the application of the other resources (unless they depend on the failed ones).

At the end ot the Puppet run the client sends to the server a report of what has been changed

    Client output # Finished catalog run in 13.78 seconds
    

The server eventually sends the report to a Report Collector.

Appendix
========

Contents
--------

*   History of Puppet versions
*   Migrating to Puppet 4
*   Introduction to Hiera

Take-aways
----------

*   Have an idea of Puppet versions history and evolution
*   Understand the main challenges involved in migration to Puppet 4
*   Have online references on Puppet 4 migration
*   Have a general Hiera of what Hiera is and how is used
*   Have a general idea of how to configure Hiera

History of Puppet Versions
==========================

During its history Puppet has constantly improved and added features, still most of the core principles are the same and have't changed.

From version 2 Puppet follows [Semantic Versioning](http://semver.org/) standards to manage versioning, with a pattern like: MAJOR.MINOR.PATCH

This implies that MAYOR versions might not be backwards compatible, MINOR versions may introduce new features keeping compatibility and PATCHes are for backwards compatible bug fixes.

This is the history of the main Puppet versions and some relevant changes Check also [Puppet Language History](http://docs.puppetlabs.com/guides/language_history.html) for a more complete review:

*   `0.9.x` - First public beta
*   `0.10.x` - 0.21.x - Various "early" versions
*   `0.22.x` - 0.25.x - Improvements and OS wider support
*   `2.6.x` - Many changes. Parametrized classes
*   `2.7.x` - Windows support
*   `3.0.x` - Many changes. Disabled dynamic variables scope. Data bindings
*   `3.2.x` - Future parser (experimental, will be default in Puppet 4)
*   `4.x.x` - Released in early 2015. New parser, new type system and lot of changes, various language cleanups and some backwards incompatibilities

Migrating to Puppet 4
=====================

With Puppet 4 many things have changed:

*   New Parser, new Type system, a lot of code tuning
*   Puppet agent and its components (facter, mcollective and the relevant stack) is shipped with All In One package (AIO) to retrieve from PuppetLabs site
*   All directory paths are changed
*   The Master function is done via **Puppet Server** (a new dedicated clojure application)

Migration from previous versions to Puppet 4 probably need some code refactoring.

Good online resources to prepare the migration to Puppet 4 are:

*   Online reference for [upgrading manifests](https://docs.puppetlabs.com/puppet/latest/reference/experiments_future.html) from 3.x to 4.x
*   Article on how to [prepare our code](http://www.camptocamp.com/en/actualite/getting-code-ready-puppet-4/) for Puppet 4.

Use the [Puppet Forge search](https://forge.puppetlabs.com/modules?) page to look for Puppet 4 compatible modules (note that most of them may not exploit fullt Puppet 4 power due to backwards 3.x compatibility).

Some other useful links about Puppet 4:

*   Puppet 4 [release notes](https://docs.puppetlabs.com/puppet/4.0/reference/release_notes.html)
*   Online reference for [agent](https://docs.puppetlabs.com/puppet/4.0/reference/upgrade_agent.html) upgrade
*   Online reference for [server](https://docs.puppetlabs.com/puppet/4.0/reference/upgrade_server.html) upgrade

Introduction to Hiera
=====================

Hiera is the most used solution to manage the data we need to configure our systems according to the logic we need.

It allows to separate data from code, allowing us to avoid to place inside our Puppet manifests information which is strictly related to our infrastructure and its settings.

It's shipped together with Puppet from version 3 and it's strictly integrated: for each class parameter Puppet does an automatic lookup on a corresponding Hiera value.

Hiera can use different backends to store it's data. The default one is Yaml (all data is placed in simple Yaml files). Other backend are Json, Mysql, Redis and so on.

Data is looked on Hiera following a hierarchy based on Puppet variables, in this way we can attribute to an Hiera Key (for example `ntp::server`) different values according to different conditions (for example the role, the environment or the location of a server).

Inside Puppet code with can use the `hiera()` function to look for a given Hiera key. For example the following code assign to the variable `$server` the value of the Hiera key called `ntp_server`. An optional parameter can be added to set the default value (here `ntp.pool.org`) to return if the key is not found on Hiera:

    $server = hiera('ntp_server','ntp.pool.org')
    

Since Puppet 3 Puppet does an automatic lookup on Hiera for each parameter of a class. In the following example the parameter `server` (whose value can be referred, inside the same class, using the `$server` variable and, inside any other class with its _fully qualified name_: `$::ntp::server`) can be changed by setting, on Hiera a value for the key called `ntp::server`:

    class ntp (
      server = 'ntp.pool.org',
    ) { }
    

Hiera configuration
===================

Hiera's configuration file for Puppet is `/etc/puppet/hiera.yaml` (On Puppet 4 `/etc/puppet/puppetlabs/hiera.yaml`). It's a Yaml file which looks like this:

    ---
      :backends:
        - yaml
    
      :hierarchy:
         - "%{::environment}/nodes/%{::fqdn}"
         - "%{::environment}/roles/%{::role}"
         - "%{::environment}/zones/%{::zone}"
         - "%{::environment}/common"
       :yaml:
         :datadir: /etc/puppet/hieradata
    

In the above sample it's configured the **backend(s)** to use, the **hierarchy** based on Puppet variables (inside `%{}`) and the configuration specific to the used backend (here is set the **datadir** when Yaml files containing Hiera keys are placed, named acconding to the defined hierarchy).
