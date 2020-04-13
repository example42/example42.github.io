---
layout: blog
title: Puppet Tip 115 - Five Years of Tiny Puppet 
---

When my colleague Martin Alfke suggested me to write a blog post about Tiny Puppet, I wondered what I could write about it that I haven't written before.

So I started to look at the past blog posts and I realized that more than five years have already passed since the [first announcement](https://www.example42.com/2015/01/02/introducing-tiny-puppet/), in January 2015.

At those times Tiny Puppet came as a natural evolution of the first generation and the "NextGen" example42 Puppet modules: a large set of modules, now mostly deprecated, with a standard structure that became a pain to maintain for a single person.

Tiny Puppet was my natural solution for a problem that for me was, and still is, of some relevance: a single module to manage via Puppet a cross-OS installation of several (potentially ANY) applications giving users full freedom on how to handle their configurations.

The core `tp` defines (Used Defined Type, written in Puppet DSL) were already there: `tp::install`, `tp::conf`, `tp::dir` and all of them were already relying on TinyData, a yaml based, hierarchical set of files where are defined the different settings of different applications on different Operating systems.

Initially the tinydata was placed in the same tp module, then, with [the release 1.0](https://www.example42.com/2015/11/18/tp-1-release/) it was separated in an autonomous git repo to allow easier upgrades and separate the tool (the tp module) from the data (the tinydata repository, which can also be used defined and customised using the `data_module` setting, present in all the tp defines.

With the release 1.0 we started to [support Puppet 4 by default](https://www.example42.com/2015/10/26/preparing-for-tp-1/), note anyway that you can still use tp with Puppet 3 (and even Puppet 2), using the relevant defines with the `3` suffix. 

## tp::install

The define `tp::install` in its simplest usage just accepts, as title, the name of the application to install.

The name of the package(s) to install are derived from the relevant [Tiny Data](https://github.com/example42/tinydata/tree/master/data), or, if missing, from the same title given (this is possible since [TP version 2.3](https://www.example42.com/2018/09/10/tp-install-anything-and-configure/).

Some examples of tp::install can be:

    tp::install { 'apache': }        # We rely on common sense, where Apache is intended as the web server and not the Foundation.
                                     # Tiny Puppet takes care of using the proper package name on different distros
    tp::install { 'redis': }         # Not so different than a plain "package { 'redis': }" since that's usually the name of the
                                     # Redis package everywhere
    tp::install { 'elasticsearch': } # Here Tiny Puppet provides some extra benefits, like installing the relevant repo, on the
                                     # underlying distro and then the elasticsearch package
    tp::install { 'gitlab-ce': }     # Under the hoods, the installation here is down in an unusual way: it downloads and runs the
                                     # install script from the GitLab website
    tp::install { 'sysdig': }        # The fastest way to install this cool tool. Tiny Puppet takes care of repos, dependencies
                                     # and package
    tp::install { 'kubernetes': }    # A recent addition to the supported apps: nothing particularly new: repos and packages are
                                     # managed (but, no, no kube cluster is initialised)
    tp::install { 'opera': }         # Since there's no specific tinydata for opera, here, if present, is just installed a package
                                     # called opera, using the underlying package manager.

So what tp::install does? Basically it uses the data in Tiny Data to handle the right package name for the underlying OS (and by OS we typically mean the most popular Linux distros (RedHat 6, 7 and 8 and derivatives, Debian 7,8,9,10 and derivatives (Ubuntu mostly LTS editions), SuSe and OpenSuse), Darwin/MacOS (relying on brew and brew-cask), Windows (relying on Chocolatey), Solaris and *BSD.

The resource tp::install, is basically a wrapper, that, according to the relevant tiny data can manage:

  - one or more **package** resources, based on the value of the following tiny data settings:
    - `package_name` the application's package(s), whose installation can be customized with settings as  `package_provider`, `package_source`, `package_install_options` and the general `package_params` hash to eventually handle all the other arguments of Puppet's package resource
    - `package_prerequisites` an array of eventual packages to install as prerequisites

  - one or more **service** resource, based on the value of the following tiny data settings:
    - `service_name` the application's service(s), whose parameters can be managed by the `service_ensure`, `service_enable` and the general `service_params` hash. 

  - one or more **exec** resources as described in one of these tiny data setting:
    - `exec_prerequisites`, an hash of exec resources with the relevant parameters to run before package installation
    - `exec_postinstall`, an hash of exec resources with the relevant parameters to run after the package installation
  
  - one or more other **tp::install** resources as defined by the tiny data setting `tp_prerequisites` (an array of prerequisite application to install via tp)

  - a **tp::repo** resource, which manages the extra package repository (for yum, apt and zypper) if any of these tinydata setting is availeble: `repo_url`, `yum_mirrorlist`, `repo_package_url`.

  - one or more **tp::conf** resources, according to the optional `conf_hash` parameter passed to the `tp::install` define

  - a **tp::conf { $app: }** resource if parameter `auto_conf` is set to true and exists the tiny data setting `config_file_template` 

  - a **tp::conf { "${app}::init": }** resource if parameter `auto_conf` is set to true and exists the tiny data setting `init_file_template` 

  - one or more **tp::dir** resources, according to the optional `dir_hash` parameter passed to the `tp::install` define 

  - a **tp::test** resource, which can be used to test the installed application, if the parameter `test_enable` is set to true

  - a **tp::puppi** resource, which can be used to integrate the installed application with [Puppi](https://github.com/example42/puppi) , if the parameter `puppi_enable` is set to true

  - the **file  { "/etc/tp/app/${app}": }** used by the tp [cli command](https://www.example42.com/2018/07/23/a-few-steps-to-tiny-puppet-command-line/) if the parameter `cli_enable` is set to true

Quite a long list of resources, indeed, but don't be scared by that, in most of the cases with a **tp::install** you just manage, via Puppet, a **package** and a **service**, needless to say that it's up to tp to handle the correct names and dependencies.

## tp::repo

## tp::conf


## tp::dir


## Using tp for custom applications or in local profiles 

An interesting point to consider is that, besides the option `data_module` which allows the usage of a custom tinydata module, all the tp defines have also the parameter `settings_hash` which can be used to override any tiny daya setting.

More information about how to use Tiny Data to configure custom applications and how to use tp defines in custom profises, can be read in [this blog post](https://www.example42.com/2018/10/15/application-management-using-tinypuppet/).

More information on the tiny data settings you can configure and customise to adapt to local versions of supported application or totally new applications, have been described in a recent posts series, where we described and updated info on:
  - [Tiny Puppet principles](https://www.example42.com/2019/12/09/request-for-tinydata-part1/)
  - [Details on Tiny data structure](https://www.example42.com/2019/12/12/request-for-tinydata-part2/)
  - [Fancy and powerful features](https://www.example42.com/2019/12/16/request-for-tinydata-part3/) on how to check for config files syntax, how to use upstream repos or run an application in a container.
  - [How to manage ANY application](https://www.example42.com/2019/12/19/request-for-tinydata-part4/)

One of the interesting thins I noticed reading the past blog posts mentioned in this article is that most of theri contents are still actual and valid: I'm not sure if this is a good or bad sign.

Has Tiny Puppet beed sane enough since the beginning os it simply never evolved?


Alessandro Franceschi