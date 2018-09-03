---
layout: blog
title: Tip of the Week 88 - Managing packages on MacOSX with Puppet and Home Brew
---

Puppet ships natively with some providers to manage the package type on MacOS X: 

- The `macports` provider supports installation of packages via [MacPorts](https://www.macports.org).

- The `appdmg` and `apple` and `pkgdmg` providers use `/usr/bin/hdiutil` and `/usr/sbin/installer` to mount DMG disk images and installs the included applications. Generally we need to specify the source from where to get the dmg files.

Besides the App Store, Mac OS has not a native repository and package managers, and this makes it harder to automate the installation of software without specifying from where to get it. But we live in interesting and fecond times and Open Source third party tools can do the job. One of the most complete, popular and interesting package managers is [Homebrew](https://brew.sh).

Homebrew, with its big list of [formulas](https://github.com/Homebrew/homebrew-core/tree/master/Formula) allows easy installation of many OSS programs, but it's thanks to extensions like [homebrew-cask](https://github.com/Homebrew/homebrew-cask) that becomes useful to manage common desktop applications (Like Atom, Chrome, Parallels and [many more](https://github.com/Homebrew/homebrew-cask/tree/master/Casks)).

Needless to say that in Puppet's huge modules landscape we have modules that allows installation of HomeBrew, and, more important, ship with dedicated package providers also for Cask.

In particular we tested [thekevjames-homebrew](https://github.com/TheKevJames/puppet-homebrew) which is one of the most promising fork of the original Kelsey Hightower module. It provides 3 different providers to manage packages with the brew command:

- The provider `brew` installs packages using `brew install <module>` without using brewcask.

- The provider `brewcask` installs packages using `brew cask install <module>` so looks in available casks.

- The provider `homebrew` attempts to install packages using first brew and then, on failure, brewcask. This is probably the sanest to use in most of the cases.

We just need to have the homebrew module in our Puppet's modulepath and specify one of them when declaring the packages we want to install on Mac.

Puppet code would look like:

    package { 'atom':
      provider => 'homebrew',
    }

A custom profile which installs Homebrew and has parameters to list the packages to install for a given user could be as simple as:

    class profile::brew (
      String $user,
      Array $packages = [ 'docker' , 'virtualbox' , 'firefox' , 'nginx' ].
    ) {
      # Use this 
      class { 'homebrew':
        user => $user,
      }
      $packages.each | $p | {
         package { $p:
           provider => 'homebrew',
           require  => Class['homebrew'],
         }
      }
    }

If you use example42's psick module you can achive the same using the generic package profile wrapper with this Hiera data:

    psick::pre::darwin_classes:
      brew: homebrew
    psick::base::darwin_classes:
      packages: psick::packages

    psick::packages::resource_default_arguments:
      provider: homebrew
 
    psick::packages::packages_list:
      - docker
      - firefox
      - little-snitch
      - parallels
      - atom

Installing packages via Puppet on MacOsX, opening the path of Puppet management both of Mac servers and clients has never been so simple!

Alessandro Franceschi