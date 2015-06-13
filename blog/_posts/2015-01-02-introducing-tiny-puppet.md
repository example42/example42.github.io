---
layout: blog
title: Introducing Tiny Puppet
---

[Tiny Puppet](https://github.com/example42/puppet-tp) is a single Puppet module that can replace virtually any other single application module.

Consider it as another Puppet abstraction layer, where we abstract the interface to the management of whole applications.

I've been thinking about a similar solution for years, since when I started to create reusable modules based on a common template (all the "NextGen" version of Example42 modules).

Now it's reality.

We usually deal with different kind of modules:

  A- Public modules that manage single applications (apache, openssh, redis ...)

  B - Custom local modules that manage applications in the way we need

  C - Public modules that manage application stacks with multiple components (they are rare, think about shared and reusable profiles)

  D - Local site modules where we place our custom resources and logic (site, profiles, $project ...)


Tiny Puppet can be used as replacement or complementary for modules as in point A and B.

It features:

  - Quick, easy to use, standard, coherent, powerful interface to the managed resources

  - Out of the box and easily expandable support for most common Operating Systems

  - Support of a quickly and easily growing [list of applications](https://github.com/example42/puppet-tp/tree/master/data).

  - Smooth coexistence with any existing Puppet modules setup: you decide what to manage

  - Quick and easy integration tests

It is intended to be used in modules that operate at an higher abstraction layer (as the ones in points C and D) where we assemble and use different application modules to achieve the setup we need.

With Tiny Puppet the installation of an application is as easy as:

    tp::install { 'nginx': }

And, once installed, you can configure it with:

    tp::conf { 'nginx':
      template     => 'site/nginx/nginx.conf.erb',
      options_hash => hiera('nginx::options_hash'),
    }

Tiny Puppet can do a lot more, though, for example you can populate any custom directory from a Git repository (it requires Puppet Labs' vcsrepo module):

    tp::dir { '/opt/apps/my_app':
      source      => 'https://git.example.42/apps/my_app/',
      vcsrepo     => 'git',
    }

All the reusability features explored and implemented during the years in Example42 modules have been ported to TP, for example you have multiple (alternate) options on how to provide a configuration file (the following example shows them all, but you can use only one of them at once):

    tp::conf { 'nginx':
      content  => 'My file content',
      template => 'site/nginx/nginx.conf.erb',
      epp      => 'site/nginx/nginx.conf.epp',
      source   => 'puppet:///modules/site/nginx/nginx.conf',
    }

You can override the specific data (file paths, packages and services names and so on) for a given application:

    tp::install { 'nginx':
      settings_hash  => {
        package_name => 'my_nginx',
        service_name => 'my_nginx',
      },
    }

Tiny Puppet can handle virtually any application which may be installed via the local OS package manager, you can manage eventual custom repositories providing a custom class where you configure them:

    tp::install { 'elasticsearch':
      dependency_class => 'site/elasticsearch/repo.pp',
    }

For some applications, a default extra repository is automatically added, you can disable this automatic lookup for a repository with:

    tp::install { 'elasticsearch':
      auto_repo => false,
    }

and you can configure you own repo with the ```tp::repo``` define.


#### Use cases

You may wonder how Tiny Puppet manages all the application specific resources, such as Apache VirtualHosts, or Mysql Grants.

Well, it doesn't.

Tiny Puppet manages packages, services and files, it provides a standard and easy to use interface to them, it adds OS abstraction and a lot of collateral frills, but everything is done by common, general use, defines which are feed by application specific data.

Currently (but there are plans for that) it doesn't manage explicitly application specific configuration options (such as Apache's DocumentRoot, ServerName...): you don't have explicit parameters to handle them, but you cana manage them as pure (Hiera) data with your own templates and the ```options_hash``` parameter.

Tiny Puppet's expected user is the System Administrator who knows how to configure his/her files and doesn't want to study/import a new module just to provide resources and configure things in the desired way.

Tiny Puppet can cohexist with any other Puppet setup, its only mandatory dependency is PuppetLabs' ```stdlib``` module. Then you can decide for which application to use it or a dedicated module.

You can even choose, in some cases, to use both tp and a dedicated module to manage some applications (for example using an existing mysql module to manage grants and tp to manage the installation and configuration of Mysql).


#### Integration testing done easy

If you want to give Tiny Puppet a try, you can use the Vagrant environment delivered in its repo, which allows quick testing of an application on different OS.

You need/should install some Vagrant plugins and Librarian Puppet:

    git clone https://github.com/example42/puppet-tp
    cd puppet-tp
    vagrant status
    vagrant plugin install vagrant-cachier # Recommended for caching downloads
    vagrant plugin install vagrant-vbguest # Recommended for have updated VirtualBox Tools
    gem install librarian-puppet # Needed for the following command
    librarian-puppet install --puppetfile Puppetfile --path vagrant/modules/public

    vagrant up Centos7
    bin/test.sh nginx Centos7

The ```bin/test.sh``` script can be used to run acceptance tests for all the applications on different VMs, for example to test the installation of apache on Debian7 you can run:

    bin/test.sh apache Debian7

Tests are based on a simple script that can be customised either directly from the ```tp::install``` define:

    tp::install { 'activemq':
      test_enable              => true,
      test_acceptance_template => 'site/activemq/test.erb',
    }

or using the ```tp::test``` define.

Such a script would be placed, by default, in ```/etc/tp/test/activemq``` and might be used in any automation pipeline you want.


#### Compatibility Matrix
In the [```acceptance```](https://github.com/example42/puppet-tp/tree/master/acceptance) directory you can give a look at the current compatibility matrix of different applications on different OS.

The files you see there are the result of the execution of commands like:

    bin/test.sh all Debian7 acceptance

which runs the installation, the execution of a test script and the uninstallation of all the applications defined in ```data```.

The compatibility matrix is going to be reviewed and fixed with time, currently we have 275 successes and 165 failures on 5 different OS for the 88 supported applications (consider that some of the failures are due to recoverable or trivial reasons such as missing repos, incorrect test scripts, incorrect application data for an OS, problems with running serially all the tests on the same machine...).


#### Adding support for new applications or OS

Most of Tiny Puppet's magic is done by the [```tp_lookup```](https://github.com/example42/puppet-tp/tree/master/lib/puppet/parser/functions/tp_lookup.rb) function which retrieves all the settings for an application from the [```data```](https://github.com/example42/puppet-tp/tree/master/data)
directory using a Hiera-like lookup method based on a dedicated ```hiera.yaml``` file present in each application subdirectory.

Bacically to add support for a new application you can simply add a new directory in [```data```](https://github.com/example42/puppet-tp/tree/master/data) and populate it accordingly, or, even more easily, run the script [```bin/moduledata_clone.sh```](https://github.com/example42/puppet-tp/tree/master/bin/moduledata_clone.sh):

    bin/moduledata_clone.sh -m test -n courier

This this create a ```courier``` directory in ```data/``` based on the contents of the ```test``` directory (I use it as a "sane" starting template). Then, obviously you may have to edit the files in the ```courier``` subdir to match different operating systems settings.

#### The present and the future

Tiny Puppet works like a charm on every system with Ruby 1.9.3 or higher, this means that you Puppet Master should run on:

  - Ubuntu 14.04
  - Debian 7
  - RedHat 7 and derivatives

and it needs some extra steps (namely the installation of Ruby 1.9.x) on other distros like:

  - Ubuntu 12.04
  - Debian 6
  - RedHat 6 and derivatives

Note, however, that this applies only for the Puppet Master node, where the catalog is compiled, on your clients, unless they run in masterless mode, you may run any other OS.

Some applications have already support for FreeBSD, OpenBSD and Solaris and, as we have seen, it's quite easy and quick to enlarge support coverage.

Future developments will evolve around:

  - Support and tuning of different applications on different OS
  - Refactoring of the ```tp_lookup``` function to work on Ruby 1.8.7
  - Allow variables interpolation in the data files
  - Automatic management of firewalling and monitoring
  - Management of multiple instances of a given application
  - Support for infile line-based configuration (```tp::line```)
  - Command line interface to query, check and diagnose the status of the installed applications
  - Addition of application specific configuration options and templates

I'm quite excited about the future implications, power and impact of Tiny Puppet.

The Example42 modules set is going to incorporate Tiny Puppet and will remove from the master branch dozens of component application modules, while introducing reusable higher abstraction modules (I call them stacks, because they are different from profiles as commonly designed and used).

If you don't care at all about Example42 modules you are forgiven, give it a try in your local site modules and see if it can be useful in some cases where you want the job done in a quick, easy and predictable way.

If you have additions, fixes, suggestions or request for the support of new OS or applications, please use  [GitHub](https://github.com/example42/puppet-tp/tree/master/).

Happy smart puppettizing with Tiny Puppet.

Alessandro Franceschi
