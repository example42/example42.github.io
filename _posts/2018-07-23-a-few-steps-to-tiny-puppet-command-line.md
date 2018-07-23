---
layout: blog
title: Tip of the Week 82 - A few steps to Tiny Puppet on the command line
---

[Tiny Puppet](https://www.github.com/example42/puppet-tp) if a Puppet module that provides general defines to manage any application on any operatingsystem, using the data present in the companion [Tiny Data](https://www.github.com/example42/tinypuppet) module.

* Table of content
{:toc}

## Core defines

The user defined resource ```tp::install``` can be used to install an application package and it's service, if the relevant hieradata it also takes care of managing its repository data via the ```tp::repo``` define (either via a release package or directly configuring the repository data).

With ```tp::conf``` it's possible to configure an application configuration files using different formats and methods. With ```tp::dir``` whole directories can be managed, also with a source on a scm repo like git, mercurial and subversion.

Finally with ```tp::test``` is possible to define any test script that checks if the relevant application is correctly working.

These are defines which we can use in your classes and profiles to manage applications without the need of a dedicated module, but Tiny Puppet also offer a command line interface, which is easy to use and powerful.


## Tiny Puppet on the command line

We can install Tiny Puppet on any system where Puppet is installed, just run, as root:

    puppet module install example42-tp
    puppet tp setup

Now you can use Tiny Puppet from the command line:

    [root@lab ~]# tp

    Usage: tp <action> [app]

    Available actions:
    install: Install the given app with tp (relevant tinydata must be available)
    uninstall: Uninstall the given application with tp
    test: Test if the given (or all) application is correctly working
    log: Tail the logs of the given (or all) application (CTRL+C to exit)
    list: List ALL the applications installable with tp

    Applications installed via tp (available for tp test and log actions):
    openssh
    nginx
    ruby-dev
    ntpdate
    epel
    sysdig
    make
    ruby
    rsyslog
    virtualbox
    dkms

The command shows the available actions and the list of applications that have been installed locally via tp.

Via tp on the cli you can install or uninstall packages or repos.

For example top install epel Repository on Redhat distributions it's enough to write:

    tp install repo

To install virtualbox with relevant repositories:

    tp install virtualbox

To list all the available applications:

    tp list

But, more useful than anything else, to test if applications are correctly working:

    [root@lab ~]# tp test
    - openssh: package openssh-server OK
    - openssh: service sshd OK
    - nginx: package nginx OK
    - nginx: service nginx OK
    - ruby-dev: package ruby-devel OK
    - ntpdate: package ntpdate OK
    - sysdig: package sysdig OK
    - make: package make OK
    - ruby: package ruby OK
    - rsyslog: package rsyslog OK
    - rsyslog: service rsyslog OK
    - virtualbox: package VirtualBox-5.1 OK
    - virtualbox: service vboxdrv OK
    - dkms: package dkms OK
    - dkms: service dkms OK

The exit code of the command is 0 if everything is OK, otherwise it's 1. You can you ```tp test``` in multiple places, for example in integration tests or canary runs during a CI pipeline to test if all the applications are locally working correctly.

Finally it's useful  to use ```tp log``` to open in tail all the logs of all the applications installed via tp.

It's possible to specify an application name to just just its logs: ```tp log nginx```.

Needless to say that all the involved paths of logs, configuration files or names of packages and services are automatically detected for different OS: so using ```tp``` commands or defines we can refer to the generic application name without the need of knowing anything on how that is managed on the system.

Alessandro Franceschi
