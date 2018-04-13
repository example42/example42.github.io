---
layout: blog
title: Tip of the Week 68 - example42 Puppet Tutorial - Part 2
---

### example42 Puppet Tutorial - Part 2

This is the second post of a series of articles covering an introduction to Puppet.

In the [first post](https://www.example42.com/2018/04/09/puppet_tutorial_part_1/) I started with Puppet agent installation and how to use Puppet and Facter to analyze your system. Next topics have been the introduction to the Puppet programming language (DSL), how to setup the central Puppet master and how to connect Puppet agents to the Puppet master.

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

But what happens if the SSH daemon is already running? Puppet will ensure that the config file will get updated. But the service will continue running with the old configuration.

In this case you must tell the service resource that it should restart upon config file changes. This is done by using a metaparameter.

    file { '/etc/ssh/sshd_config':
      ensure => file,
      source => 'puppet:///modules/ssh/sshd_config',
      notify => Service['sshd'],
    }

The notify parameter uses a reference to a declared resource type. The resource type is written with capital letter and afterwards you use the title in brackets.

    Type['title']

Another solution is to use the chaining pattern:

    File['/etc/ssh/sshd_config'] ~> Service['sshd']

Let's put everything together:

    # /etc/puppetlabs/code/environments/production/modules/ssh/manifests/init.pp
    class ssh {
      package { 'openssh-server':
        ensure => present,
      }
      package { 'openssh-client':
        ensure => present,
      }
      file { '/etc/ssh/sshd_config':
       ensure => file,
       source => 'puppet:///modules/ssh/sshd_config',
       notify => Service['sshd'],
      }
      service { 'sshd':
        ensure => running,
        enable => true,
      }
    }

And the configuration file:

    # /etc/puppetlabs/code/environments/production/modules/ssh/files/sshd_config
    Port 22
    PermitRootLogin no
    PubkeyAuthentication yes
    AuthorizedKeysFile      .ssh/authorized_keys
    UsePAM yes
    UseDNS no
    Subsystem       sftp    /usr/libexec/openssh/sftp-server

#### Puppet Variables

But what if one system needs a different configuration? e.g. allow root access or switch port.
This would require a second configuratoin file and a class adopted to only one specifc system.
Or what if you must manage SSH on another UNIX system where paths are different?

Puppet allows you to build flexible code by making use of variables. A variable in Puppet is easily identified by having a dollar sign: `$variable`.

You can assign values to variables - but within a class you can not reassign the same variable a second time. Variables in Puppet are more like static artifacts and Puppet is not a scripting language.

Next you can check variables whether they have a value, you can check for specifc values or for regular expressions.

Check for variable having a value:

    $var1 = false
    if $var1 {
      # Puppet code
    } else {          # <- else is optional
      # Puppet code
    }
    
Checking a variable like in the example above will return true in the following cases:

1. the variable has the bool value `true`
2. the variable has any content (Array, Hash String or even an empty string)

Check for variable having specific value:

    $var2 = 'dbmaster'
    if $var2 == 'dbmaster' {
      # Puppet code
    }

Check for variable using regular expression

    $var3 = 'db22.domain.com'
    if $var ~= /^db\d+\.domain\.com$/ {
      # Puppet code
    }    

#### Puppet Code Logic

Variables will be mostly used in Puppet code logic: use correct package names or file paths depending on Linux distribution name.

This is where the `case` function will be useful:

    case $::facts['os']['name'] {
      'CentOS', 'Amazon', 'RHEL': {
        # Puppet code for RedHat based systems
      }
      'Ubuntu', 'Debian': {
        # Puppet code for Debian based systems
      }
      'SLES': {
        # Puppet code for SuSE based systems
      }
      default: {
        # Optional default for any other OS
      }
    }

What is this `$::facts['os']['name']` thing? Remeber post 1 when I was introducing `facter`?
Facts are available to Puppet code within a special variable: `$::facts`. All data are stored as a hash inside this variable.

On the command line you were using `facter os` or `facter os.name` to access specific facts. Within Puppet code you must use the `$::facts` variable and put the elements into brackets and quote them.

You might want to add your own set of variables during system provisioning. e.g. information on which datacenter the system is running in, what is the usecase of the system and whether it is a development or production system.

You can add these facts easily by placing files into a specific directory (`/etc/puppetlabs/facter/facts.d/`). Don't worry, if the directory does not exist, just create it.

In this directory you can place:

  - .yaml files - with yaml syntax
  - .json files - with json syntax
  - .txt files - with key=value syntax

Now you can create information on your datacenter to a node:

    # /etc/puppetlabs/facter/facts.d/provision_facts.yaml
    ---
    datacenter: 'london'
    application:
      name: 'cms'
      stage: 'dev'

You can query these facts by using `facter -p`:

    facter -p datacenter
    london
    facter -p application
    {
      "name" => "cms",
      "stage" => "dev"
    }

Let's get back to the Puppet code:

Now we can rewrite the SSH class to also work on Debian systems:

    # /etc/puppetlabs/code/environments/production/modules/ssh/manifests/init.pp
    class ssh {
      case $::facts['os']['family'] {
        'RedHat': {
          $packages = ['openssh-server', 'openssh-client']
        }
        'Debian': {
          $packages = ['ssh']
        }
      }
      package { $packages:
        ensure => present,
      }
      file { '/etc/ssh/sshd_config':
       ensure => file,
       source => 'puppet:///modules/ssh/sshd_config',
       notify => Service['sshd'],
      }
      service { 'sshd':
        ensure => running,
        enable => true,
      }
    }

Here we use another thing within Puppet: at a title you are able to use an array. Puppet internally will split the array up into single package resource type declarations.

#### Class Parameters

But how do you deal with a single node to allow root ssh access?

You have multiple possible solutions like creating an external fact on the node, and check for existance of the fact. But that is highly unflexible. Instead you can use class parameters.

    # /etc/puppetlabs/code/environments/production/modules/ssh/manifests/init.pp
    class ssh (
      Boolean $permit_root = true,
    ){
      # Puppet code
    }

At the parameter we specify the expected data type and we provide a default value.

But how to now declare the class?

#### Node classification

The most simple approach (on small platforms) is the manifest based node classification. Remeber the environment directory structure where I showed the `manifests` directory with `site.pp` file inside? THis is the place where you will place information on your nodes.

    # /etc/puppetlabs/code/environments/production/manifests/site.pp
    
    node 'agent1.example42.training' {
    }

There are two ways on how to inform the Puppet server that he should add a class to the node's catalog:

    include ssh
or

    class { 'ssh':
    }

When using the second approach, you are able to specify class parameters:

    class { 'ssh':
      permit_root => true,
    }

#### Dynamic configuration files

Now we must ensure that Puppet uses the provided parameter inside a configuration file. Which means the configuration file must be built during Puppet catalog compilation. This is where templates come into place.

Puppet templates are plain text files which use opening (`<%`) and closing (`%>`) tags to identify where the template engine should do something. The content within the tags is just Puppet DSL code.

Templates are - like files - part of the module, but are not in the files folder, but in the templates directory. Modern Puppet uses the EPP template engine which requires that templates must have the file ending `.epp`.

In this case you want the template engine to check for the value of the parameter `permit_root` and set the correct configuration value:

    # /etc/puppetlabs/code/environments/production/modules/ssh/templates/sshd_config.epp
    Port 22
    <% if $ssh::permit_root { %>
    PermitRootLogin yes
    <% } else { %>
    PermitRootLogin no
    <% } %>
    PubkeyAuthentication yes
    AuthorizedKeysFile      .ssh/authorized_keys
    UsePAM yes
    UseDNS no
    Subsystem       sftp    /usr/libexec/openssh/sftp-server

Using the template is different to using a static file. At the static file we were managing the `source`. Now you must manage the `content`:

    file { '/etc/ssh/sshd_config':
      ensure  => file,
      content => epp('ssh/sshd_config.epp'),
    }

The template validation takes place on the Puppet master while compiling the catalog. So there is no need to specify the protocol or the server or telling the server that it should look in a module. You only specify the module and the name of the file in the templates directory.

This will give you the following Puppet code:

    # /etc/puppetlabs/code/environments/production/modules/ssh/manifests/init.pp
    class ssh (
      Boolean $permit_root = true,
    ){
      case $::facts['os']['family'] {
        'RedHat': {
          $packages = ['openssh-server', 'openssh-client']
        }
        'Debian': {
          $packages = ['ssh']
        }
      }
      package { $packages:
        ensure => present,
      }
      file { '/etc/ssh/sshd_config':
       ensure  => file,
       content => epp('ssh/sshd_config.epp'),
       notify  => Service['sshd'],
      }
      service { 'sshd':
        ensure => running,
        enable => true,
      }
    }
    
#### Separation of Code and Data

But what if you have a large number of systems and each system needs to get configured slightly different. In this case it will become a nightmare when you add each node individually to `manifests/site.pp` file or by writing specific puppet code.

This is where Hiera jumps in.
Hiera allows you to do data lookups, so you can separate code from data.

Think about the following Puppet code:

    class ssh {
      case $::facts['datacenter' {
        'amsterdam': {
          case $::certname {
            'gateway.ams.example42.training': {
              $permit_root = false
            }
            'default': {
              $permit_root = true
            }
          }
          $ssh_port = '22'
          $ssh_listen = 'enp0s3'
        }
        'london': {
          if $::certname == 'firewall.lon.example42.training' {
            $permit_root = false
          } else {
            if $::certname = 'devel.lon.example42.training {
              $permit_root = true
            }
          }
          $ssh_port = '222'
          $ssh_lisen = 'any'
        }
      }
      file { '/etc/ssh/sshd_config':
        ensure  => file,
        content => epp('ssh/sshd_config.epp'),  # <- template uses variables from above
      }
    }

Looks like nightmare? Yes, this is nightmare. Let's start using hiera:

    class ssh {
      $permit_root = lookup('permit_root', Boolean, first, false)
      $ssh_port = lookup('ssh_port', String, first, '22')
      $ssh_listen = lookup('ssh_listen', String, first, 'enp0s3')
      file { '/etc/ssh/sshd_config':
        ensure  => file,
        content => epp('ssh/sshd_config.epp'),  # <- template uses variables from above
      }
    }

Puppet code now looks cleaner. But where have you hidden the data?
First: you need a Hiera configuration file located in `/etc/puppetlabs/code/environment/production/hiera.yaml`.
Within the hiera.yaml file, one specifies different layers of data.

Think of hiera layers being a huge 'chessboard'. At the default 'chessboard' every field means a key and has the value written on it.
With every hiera layer, hiera looks whether it has another 'chessboard' which can be placed over the default one. The new layer 'chessboard' has some elements unset, which means, you can look through the layer and you see the data from the default 'chessboard', some data are overwritten.

I try to visualize (the effective data are printed in **bold**

1. node agent.ams.example42.training

  - Datacenter: Amsterdam
  - Certname: agent.ams.example42.training

Level | permit_root | ssh_port | ssh_listen
--- | --- | --- | ---
Common Data | false | **22** | any
Amsterdam Data | **true** | --- | **enp0s3**
Node Data | --- | --- | ---

2. node gateway.ams.example42.training

  - Datacenter: Amsterdam
  - Certname: gateway.ams.example42.training

Level | permit_root | ssh_port | ssh_listen
--- | --- | --- | ---
Common Data | false | **22** | any 
Amsterdam Data | true | --- | **enp0s3**
Node Data | **false** | --- | ---

3. node agent.lon.example42.training

  - Datacenter: London
  - Certname: agent.lon.example42.training

Level | permit_root | ssh_port | ssh_listen
--- | --- | --- | ---
Common Data | **false** | 22 | **any** 
London Data | --- | **222** | ---
Node Data | --- | --- | ---

4. node firewall.lon.example42.training

  - Datacenter: London
  - Certname: firewall.lon.example42.training

Level | permit_root | ssh_port | ssh_listen
--- | --- | --- | ---
Common Data | **false** | 22 | **any** 
London Data | --- | **222** | ---
Node Data | --- | --- | ---


5. node devel.lon.example42.training

  - Datacenter: London
  - Certname: devel.lon.example42.training

Level | permit_root | ssh_port | ssh_listen
--- | --- | --- | ---
Common Data | false | 22 | **any** 
London Data | --- | **222** | ---
Node Data | **true** | --- | ---

Based on these inforation you can build your hierarchies into your hiera.yaml file:

    # /etc/puppetlabs/code/environments/production/hiera.yaml
    ---
    version: 5
    defaults:
      datadir: data
      data_hash: yaml_data
    hierarchy:
      - name: 'Node Data'
        path: "nodes/%{trusted.certname}.yaml"
      - name: 'Data Center Data'
        path: "datacenters/%{facts.datacenter}.yaml"
      - name: 'Common Data'
        path: 'common.yaml'

The data for hiera are placed inside the (relative) path `data` (`/etc/puppetlabs/code/environments/production/data`).

Your directory structure (using the above examples) will be the following:

    /etc/puppetlabs/code/environments/production/data
      |- common.yaml
      |- datacenters/
      |  |- london.yaml
      |  \- amsterdam.yaml
      \- nodes/
         |- gateway.ams.example42.training.yaml
         \- devel.lon.example42.training
         
The content of the files will be YAML structured data containing `key: value`.
e.g.

    # common.yaml
    permit_root: false
    ssh_port: '22'
    ssh_listen: 'any'

But now it is up to you to take care to not use duplicate key names.

There is another even more simple way: When declaring a parameterozed class using the `include` function, Puppet will automatically query hiera for data.

So you move the lookups to parameters:

    class ssh (
      Boolean $permit_root = false,
      String  $ssh_port    = '22',
      String  $ssh_listen  = 'enp0s3',
    ){
      file { '/etc/ssh/sshd_config':
        ensure  => file,
        content => epp('ssh/sshd_config.epp'),  # <- template uses variables from above
      }
    }

When you just `include ssh` Puppet will ask hiera for the parameters in the given namespace: "Hey hiera, do you have a value for namespace `ssh` and parameter `permit_root`? Or to be short: `ssh::permit_root`.

All you have to do is add the namesapces to your keys:

    # common.yaml
    ssh::permit_root: false
    ssh::ssh_port: '22'
    ssh::ssh_listen: 'any'

The next posting will explain the concept of re-using existing modules and provide information on why you should see modules similar to libararies. Additionally I will explain the concept of Roles and Profiles and the Node Classification.


Martin Alfke
