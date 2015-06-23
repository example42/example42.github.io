---
layout: blog
title: Rethinking modules - Part 2
---

In the first part of this blog series I expressed my opinions about these points:

- The general reusability features a component module should have
- The difference between component and higher abstraction modules
- What are the challenges we have to face when we want to make reusable higher abstraction modules

I also underlined two fundamental issues that I think are still open in the Puppet modules ecosystem:

- Patterns to extend reusability of higher abstraction layer modules
- Standardization in the component application modules

Some preliminary exploration on the first topic has been expressed in Part 1. There's much more to do about it.

The second point is what we are going to discuss in this post.

In the last months there has been the effort to stimulate collaboration around a standard set of naming properties for modules parameters: the [StdMod](https://github.com/stdmod/) initiative seems quite stale, it doesn't seem to be a high priority for Puppet's community.

Still I think that a coherent and standard set of class and defines parameters, would be of great benefit.

It sounds obvious, because it is obvious.

How many times we just need, from a module, to simply install its application and have the possibility to manage freely and easily its configuration?

How many times we had to write our own code for very simple needs because existing modules were too complex, or didn't offer enough flexibility, or had dependency issues, or they forced us to study the module's parameters in order to make them do what we wanted?

Modules that just install and configure a single application (what we are calling component modules) should just do that, in the simplest, quickest, and most predictable way.

During the years I wrote dozens of modules that had a standard interface: a common set of parameters that implemented basic reusability features, whose usage was easy  and predictable.
With a code like the following you could manage the ERB template of your application, whatever the module:

    class { 'openssh:'
      template => 'site/openssh/sshd.conf.erb'
    }

Most of Example42 modules, therefore, had a standard layout which was duplicated for each module. The horrible side of such an approach is that when I had to fix some "core" code, duplicated on all the modules, I had to do it on several places.
For example, most of the existing spec tests in Example42 modules are failing on Travis because they are not compliant with the latest versions of rspec-puppet. I should fix them, I don't have enough time, will and motivation to do that.

So I wondered if it was possible to replicate the reusability and coherency features of these modules in a more manageable way.

### Extreme component modules standardization: Tiny Puppet

Well, it seems possible.

Here is [TP (Tiny Puppet)](https://github.com/example42/puppet-tp ), if it will turn out as I hope, it will rock.

Consider Tiny Puppet as the essence of most of Example42 modules + some grains of Puppi.

It's a single module that allows the installation and configuration of different component applications, using a set of common defines.

It's supposed to be a replacement for simple application modules, when they just install and configure basic stuff, and a complementary tool for more complex modules, when they offer specific resources and options you may need.

The project is still at its very early stages, consider it as ReadMe driven development, various of the features which are described in the following lines have still to be developed or refined.

#### Installation and usage

Tiny Puppet is a normal module, you can install it by placing the content of the [GitHub repository](https://github.com/example42/puppet-tp ) in your modulepath. It will be published on the Forge, when it will be more complete and tested.

It depends on Puppet Labs's stdlib module, and, optionally (if you use specific features) on the vcsrepo and concat modules.

It contains few basic defines that allow very specific functions:

- ```tp::install```. It just installs an application and starts its service, with default settings
- ```tp::conf```. It allows to manage configuration files of an application with whatever method possible for files (as an ERB template, as an EPP template, via the fileserver, managing directly its content...)
- ```tp::dir```. Manages the content of a directory, either sourced from the fileserver or from repositories of the most common VCS tools (Git, Mercurial, Subversion, Bazaar, CVS)
- ```tp::stdmod```. Manages the installation of an application using StdMod compliant parameters.
- ```tp::line```. (TODO) Manages single lines in a configuration file
- ```tp::concat```. (TODO) Manages file fragments of a configuration file

These are the basic tools, but they would be of relative use if they weren't coupled with application specific data.

In the ```data``` directory of the tp module, for each supported application (currently very few, as I'm still defining the most optimal data structure and naming, but once this is defined it will be very quick to add support for new applications) there is a Hiera-like hierarchy of yaml files for different Operating Systems.

This data, which the user can always override, allow usage patterns like the one we see in the following paragraphs.

Worth noting is that the module is not invasive, it has limited dependencies and you can decide to use it only for the cases you need. For example you can use PuppetLabs PostgreSQL module's types to manage grants and credentials and eventually use ```tp::install``` to install it and ```tp::conf``` to manage specific configuration files. Also, you can use a third party Apache module to install and configure it and ```tp::dir``` to manage the content of the documents root based on a VCS repository.

#### Tiny Puppet usage in manifests

Her are some sample snippets of code that fulfil specific needs. They all refer to redis, as this is the frst application I used to test data structure, but are going to work for all the applications dfined in the data dir.

Install an application with default settings (package installed, service started)

    tp::install { 'redis': }

Install an application specifying a custom dependency class (where, for example, you can add a custom package repository)

    tp::install { 'redis':
      dependency_class => 'site::redis::redis_dependency',
    }

Install custom packages:

    tp::install { 'redis':
      packages => {
        'redis' => { 'ensure' => 'present' }
        'redis-addons' => { 'ensure' => 'present' }
      },
    }

Install custom packages, services and files ( The parameters feed a create_resource function, so they might be populated from a Hiera call ):

    tp::install { 'redis':
      packages => hiera('redis::packages'),
      service  => hiera('redis::services'),
      files    => hiera('redis::files'),
    }


Configure a file of an application providing a custom erb template:

    tp::conf { 'redis::redis.conf':
      template    => 'site/redis/redis.conf.erb',
    }


Configure a file of an application providing a custom epp template:

    tp::conf { 'redis::redis.conf':
      epp   => 'site/redis/redis.conf.epp',
    }


Provide a file via the fileserver:

    tp::conf { 'redis::redis.conf':
      source      => 'puppet:///modules/site/redis/redis.conf',
    }


Provide a whole configuration directory from the fileserver:

    tp::dir { 'redis':
      source      => 'puppet:///modules/site/redis/',
    }

Provide a whole configuration directory from a Git repository (it requires Puppet Labs' vcsrepo module):

    tp::dir { 'redis':
      source      => 'https://git.example.42/puppet/redis/conf',
      vcsrepo     => 'git',
    }

Populate any custom directory from a Subversion repository (it requires Puppet Labs' vcsrepo module):

    tp::dir { 'logstash': # The title is irrelevant, when 'path' is defined 
      path        => '/opt/apps/my_app',
      source      => 'https://git.example.42/apps/my_app/',
      vcsrepo     => 'svn',
    }

Provide a data directory (the default DocumentRoot, for apache) from a Git repository (it requires Puppet Labs' vcsrepo module):

    tp::dir { 'apache':
      # Prefix is a tag that defines the type of directory to use
      # Default: config. Other possible dir types: 'data', 'log', 'confd', 'lib'
      #  available according to the application
      prefix      => 'data' 
      source      => 'https://git.example.42/apps/my_app/',
      vcsrepo     => 'git',
    }


Configure a single line in an existing file (TODO):

    tp::line { 'redis::redis.conf::port':
      value => '1234',
    }


Configure a fragment of a given file (TODO):

    tp::concat { 'redis::redis.conf':
      order   => '10',
      content => 'port 1234',
    }


Install an application and provide custom settings for internally used parameters (TODO):

    tp::install { 'redis':
      settings => {
        config_dir_path => '/opt/redis/conf',
        tcp_port        => '3242',
        pid_file_path   => '/opt/redis/run/redis.pid',
      },
    }


#### Tiny Puppet usage on the Command Line

The previous code samples are expected to be used in manifests, mostly in higher abstraction modules where the single components applications have to be installed and configured as needed.

All the logic on how to correlate and configure different applications may stay in these higher abstraction classes, which can use the tp defines to configure specific files as needed or lines inside existing files.

Note also that  tp  defines are relatively light, and even if in most cases they just wrap native resources like package, service and file, they are probably slimmer and less resource intensive than a dedicated module.

Still there's something more that such a Tiny Puppet module can do: bring Puppet knowledge to the cli.

It's an old idea of mine which I implemented with Puppi but required some extra code on Exaple42 modules for a seamless integration: with Puppet we install and configure everything, we have complete knowledge on how an application is installed on a system, and it would be useful to query and use this information directly via a command line tool.

Once you can do something with a single unattended command on your shell, you can do that in many different ways: inside scripts, on cron jobs, as remote command execution during a continuos delivery pipeline or an orchestrated sequence.

That's why I plan to introduce a tp Puppet face that can allow the execution of simple, and powerful, commands as the ones that follow.

 
Install a specific application (TODO)

    puppet tp install redis


Retrieve contextual info about an application (TODO). For example the relevant network connection, the output of diagnostic commands, the status of the managed application

    puppet tp info redis


Check if an application is running correctly (TODO)

    puppet tp check redis


This last command, still not implemented, reflects one of the features I liked most of Puppi when used with Example42 NextGen modules: the ability to immediately check on a system if the resources provided by the installed modules deliver a working application.

Launch it from the shell, via Mcollective, as a step in a CI pipeline and verify immediately if your application, as configured with your own parameters, is running correctly on the provisionined system... a bit simpler than writing Beaker tests, isn't it?

Since ```puppet tp``` would be a face it could leverage on Puppet libraries and functions, and this may bring to some interesting interactions. For example a failing ```puppet tp check``` (eventually executed via cron) command may trigger a report message that could be used, by the report server (typically the Puppet Master) to send alarms or trigger the execution of other activities (for example a Puppet run), with an orchestration tool like MCollective.


### So what?

Well, these are more or less the points behind Tiny Puppet.

I'm genuinely interested in knowing opinions and suggestions about them.
There are various implementation details to define and some decision on the structure of the data directory.
The repository is on [GitHub](https://github.com/example42/puppet-tp) open for contributions.

Alessandro Franceschi