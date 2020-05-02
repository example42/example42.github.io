---
layout: blog
title: Puppet Tip 115 - Five Years of Tiny Puppet 
---

When my colleague Martin Alfke suggested me to write a blog post about Tiny Puppet, I wondered what I could write about it that I haven't written before.

So I started to look at the past blog posts and I realized that more than five years have already passed since the [first announcement](https://www.example42.com/2015/01/02/introducing-tiny-puppet/), in January 2015.

At those times Tiny Puppet came as a natural evolution of the first generation and the "NextGen" example42 Puppet modules: a large set of modules, now mostly deprecated, with a standard structure that became a pain to maintain for a single person.

Tiny Puppet was my natural solution for a problem that for me was, and still is, of some relevance: reduce the number of modules and dependencies to use, especially when resources to manage are simple packages, services and files.

For this reason I wrote a single module to manage via Puppet a cross-OS installation of several (potentially ANY) applications giving users full freedom on how to handle their configurations.

The core `tp` defines (Used Defined Type, written in Puppet DSL) were already there, since the beginning: `tp::install`, `tp::conf`, `tp::dir` and all of them were already relying on TinyData, a yaml based, hierarchical set of files where are defined the different settings of different applications on different Operating systems.

Initially the tinydata was placed in the same tp module, then, with [the release 1.0](https://www.example42.com/2015/11/18/tp-1-release/) it was separated in an autonomous git repo to allow easier upgrades and separate the tool (the tp module) from the data (the tinydata repository, which can also be user defined and customized using the `data_module` parameter, present in all the tp defines.

With the release 1.0 we started to [support Puppet 4 by default](https://www.example42.com/2015/10/26/preparing-for-tp-1/), note anyway that you can still use tp with Puppet 3 (and even Puppet 2), using the relevant defines with the `3` suffix: `tp::install3`, `tp::conf3`, `tp::dir3`. 

## tp::install

The define `tp::install` in its simplest usage just accepts, as title, the name of the application to install.

The names of the package(s) to install are derived from the relevant [Tiny Data](https://github.com/example42/tinydata/tree/master/data), or, if missing, from the same title used for the defines (this is possible since [TP version 2.3](https://www.example42.com/2018/09/10/tp-install-anything-and-configure/).

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
                                     # managed (but, hei, no kube cluster is initialised)
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

One of the Tiny Puppet added values, compared to the abstraction that Puppet already provides with the package resource, is to manage eventual repositories needed to install a package.

This is done by using different tinydata settings, more specifically, tp::repo can manage:

  - Installation of a release package, containing the configuration of a yum or apt repo, if is present for a given application the setting `repo_package_url`. In this case the settings `repo_package_name`, `repo_package_provider` and `repo_package_params` are used to define, respectively, the name of the repo release package, the Puppet provider to install it and eventual other parameters to pass to the repo package resource.
  - If no release package is provided, the package repositories can be configured directly:

    - **Yum** repositories are managed via a **yumrepo** Puppet resources using the tinydata settings `repo_url`, `repo_filename`, `repo_description`, `yum_mirrorlist`, `key_url` and `yum_priority`.
    - **Apt** repositories are managed via **exec** (to add gpg keys) and **file** (for the source list file) resources, based on the tinydata settings: `repo_url`, `aptrepo_title`, `apt_key_server`, `apt_key_fingerprint`, `key_url` and `key`.
    - **Zypper** repositories are managed via **exec** resources based on the tiny data settings: `repo_url`, `repo_name`, `zypper_repofile_url`.

All the above tinydata can be overridden by parameters passed to the `tp::repo` define. One special parameter, called `upstream_repo` allows users to specify if to install a package using the repo from the same application upstream authors or if to use the default repos from the underlying OS. Of course the relevant tinydata settings must exist in order to enforce this option.

## tp::conf

This tp define is probably the simplest one, as it just manages ONE file, related to the application specified in the title.

By default tp::conf manages the *main* configuration file of the relevant application. This is defined by the `config_file_path` tinydata setting-

So for example, a define as follows in going to manage the file `/etc/httpd/conf/httpd.conf` on RedHat derivatives or `/etc/apache2/apache2.conf` on Debian derivatives:

    tp::conf { 'apache':
      source => 'puppet:///modules/profile/apache/apache.conf',
    }

The content of the file to manage can be set using different, alternative, parameters, which are reflected on actual parameters of the file resource:

    source   => 'puppet:///modules/profile/apache/apache.conf', # Passed as is to source parameter of the file resource
    content  => '#This file has no content',                    # Passed as is to content parameter of file resource
    template => 'profile/apache/apache.conf.erb',               # Passed to content parameter as template($template)            
    epp      => 'profile/apache/apache.conf.epp',               # Passed to content parameter as epp($epp)            

When using templates it's possible to use the `options_hash` parameter to specify an Hash of custom key pairs which can be used in the templates, for dynamic, user defined, data. In the templates it's also available the variable **settings** which all the tinydata settings for the application.

For example, we can have a define as:

    tp::conf { 'mongodb':
      template     => 'profile/mongodb/mongod.conf.erb',
      options_hash => {
        'replSetName' => 'prod0',
        'bindIp'      => $::ipaddress,
      }
    }

and in the file `profile/templates/mongodb/mongod.conf.erb` a content as follows (note that the parameter $options_hash can be accessed in the template both via the `options_hash` and the `options` variable, and that the settings variable get directly the correct setting for the underlying OS):

    # File managed by Puppet - mongod.conf
    systemLog:
      destination: file
      logAppend: true
      path: <%= @settings['log_file_path'] %>

    storage:
      dbPath: <%= @settings['data_dir_path'] %>

    processManagement:
      fork: true
      pidFilePath: <%= @settings['pid_file_path'] %>

    net:
      port: <%= @settings['tcp_port'] %>
      bindIp: <%= @options['bindIp'] %>

    <% if @options['replSetName'] != '' -%>
    replication:
      replSetName: <%= @options['replSetName'] %>
    <% end -%>

So, what's important to understand here is that Tiny Puppet has no idea on how to configure any application (as a dedicated module may have) and leaves totally to the user HOW to handle its configurations. This can be good (if you know how to configure your stuff and just need a quick way to Puppettize it) or not (if you rely on a module's intelligence the logic of how to configure an app, or if there are more complex and specific resources to manage than just packages, services and configuration files). Note, however, that you can rely on Tiny Data settings to manage configuration files which may be "cross OS compatible" how of the box.

In the above template example, we have seen some other tinydata settings which may be useful when working with tp::conf.

We have seen that by default, if you just pass in the title the name of an application, tp::conf manages the "main" configuration file of that application, but you can actually manage other files for that application according to the following conventions.

If we specify a file name after the application name in the title, separated by `::`, that file is placed in the main configuration directory (setting `config_dir_path`), the following, for example, will manage `/etc/ssh/ssh_config` since openssh's config_dir_path is `/etc/ssh`:

    tp::conf { 'openssh::ssh_config': [...] }

If we explicitly set a path, that path is used and the title is only used to understand what application we are managing and handling the relevant dependencies. In the following example we manage `/usr/local/bin/openssh_check`:

    tp::conf { 'openssh::ssh_check':
      path => '/usr/local/bin/openssh_check',
      [...]
    }

If we specify a `base_dir` and use a title with the format: `application::file_name` the file is created with the defined name in the indicated base directory. For example, the following wil create (in RedHat derivatives) `/etc/httpd/conf.d/example42.com.conf`:

    tp::conf { 'apache::example42.com.conf':
      base_dir => 'conf', # Use the settings key: conf_dir_path
    }

There are different possible `base_dir` values, they may be defined according to the application. The most common ones are:

    base_dir param    Settings key       Description

    config            config_dir_path    The main configuration directory. That's the default value for base_dir.
    conf              conf_dir_path      A dir that contains fragments of configurations (usually /conf.d/)
    log               log_dir_path       Directory where are placed the application logs
    data              data_dir_path      Directory where application data lives

Why is it useful and necessary to always specify the application name in `tp::conf`? Because in this way all dependencies are automatically managed: file is managed after the installation of the relevant package and triggers a service restart. We can however disable, or change, this behavior.

To disable package and service dependencies:

    tp::conf { 'bind':
      config_file_notify  => false,
      config_file_require => false,
    }

To override the default dependencies, based on tinydata we can also specify directly the relevant resources:

    tp::conf { 'bind':
      config_file_notify  => Service['bind9'],
      config_file_require => Package['bind9-server'],
    }


## tp::dir

Tp::dir is like tp::conf but works on whole directories rather than just single files.

For example, to manage the whole content of /etc/redis, we can use (source files are supposed to be present in our profile module under `profile/files/redis`):

    tp::dir { 'redis':
      source      => 'puppet:///modules/profile/redis/',
    }

Also here the `base_dir` parameter can be used to define what directory we are using (default value is always "config" meaning the main configuration directory of an application, in case this concept might be controversial, just refer to the actual tinydata settings and act accordingly).

We haven't mentioned this before, but the following parameters cna be used, both for tp::dir and tp::conf:

    tp::dir { 'redis':
      owner => 'root',
      group => 'redis',
      mode  => '0750',
    }

We can also force the recursive purge of all the files of a directory which are not in the given source (params here beahve as in the file resource), always be careful when recursively purging files with Puppet (double check your paths!):

    tp::dir { 'redis':
      source  => 'puppet:///modules/profile/redis/',
      recurse => true,
      purge   => true,
      force   => true,
    }

In case you want to manage a directory, which might have as parent a non existing directory, you can ensure that its parent directory exists, to prvent Puppet failures:

    tp::dir { 'apache::my_app':
      path               => '/data/www/my_app',
      path_parent_create => true,
    }

You can also manage the content of a directory using a git repository ()or whatever is supported by puppetlabs-vcsrepo module, which is require for this functonality):

    tp::dir { 'apache':
      base_dir => 'data',
      source   => 'https://git.example.42/apps/my_app/',
      vcsrepo  => 'git',
    }

You can even do a poor man continuous delivery by ensuring you have always the latest version of a git repo:

    tp::dir { 'apache::my_app':
      ensure             => 'latest',
      path               => '/data/www/my_app',
      path_parent_create => true,
      source             => 'https://git.example.42/apps/my_app/',
      vcsrepo            => 'git',
    }

## Everything is data

We have talked about the tp defines, but there's actually a `tp` class, which is needed only if you want to install the tp command line on your systems and to manage tp defines via Hiera. If you include it iin your catalog you will have the tp command and the possibility to configure via Hiera basically everything.

In the following example, we are managing a full LAMP stack, included configuration files for virtual hosts and web application files with auto deployment from a Git source (don't try this at home, you miss some files and access to git repos):

    tp::install_hash:
      apache: {}
      mysql: {}
      php: {}

    tp::conf_hash:
      apache::openkills.info.conf:
        base_dir: conf
        template: psick/apache/vhost.conf.erb
        options_hash:
          ServerName: openskills.info
          ServerAlias:
            - openskill.info
            - www.openskills.info
            - www.openskill.info
          AddDefaultCharset: ISO-8859-1
      apache::deny_git.conf:
        base_dir: conf
        source: puppet:///modules/psick/apache/deny_git.conf
      apache::abnormalia.com.conf:
        base_dir: conf
        template: psick/apache/vhost.conf.erb
        options_hash:
          ServerName: abnormalia.com
          ServerAlias:
            - www.abnormalia.com
          AddDefaultCharset: ISO-8859-1
          extra:
            ErrorDocument: '404 /index.php'

    tp::dir_hash:
      apache::openskills.info:
        vcsrepo: git
        source: git@bitbucket.org:alvagante/openskills.info.git
        path: /var/www/html/openskills.info
      apache::abnormalia.com:
        ensure: latest
        vcsrepo: git
        source: git@bitbucket.org:alvagante/abnormalia.com.git
        path: /var/www/html/abnormalia.com


## tp resources defaults

If you use massively tp in your control repo, you may want to set in the main manifests/site.pp some resource defaults which are applied to all the tp resources in your catalog. Here is an example where tp cli integration is enabled (do yourself a favour, use it just for the joys of writing on your shell `tp log` and `tp test` ;-) ) and a custom tinydata module is used.

    $tinydata_module = 'my_tinydata'
    Tp::Install {
      cli_enable  => true,
      test_enable => true,
      data_module => $tinydata_module
    }
    Tp::Conf {
      data_module => $tinydata_module,
    }
    Tp::Dir {
      data_module => $tinydata_module,
    }


## Using tp for custom applications or in local profiles 

An interesting point to consider is that, besides the option `data_module` which allows the usage of a custom tinydata module, all the tp defines have also the parameter `settings_hash` which can be used to override any tiny data setting.

We can even manage via tp a custom application, packaged internally, as long as we have the relevant data in a custom tinydata module:

    tp::install { 'my_app':
      data_module => 'my_tinydata',
    }

When you use directly the upstream **tinydata** module and not a local clone (in your internal git servers) or fork of it, we **recommend** to always specify the used version in your Puppetfile and properly test changes before updating the version used:  tinydata contains info about a large number of applications, and their data might be updated if we find that is wrong for a given OS or if we want to extend support for a new OS release.  These changes don't follow [SemVer](https://semver.org/) standards and even a minor version update in Tiny Data may change some settings for an application you manage via Tiny Data.

The rule of thumb here is: know what applications you manage via tp and check, when upgrading the tinydata module, if there are changes in data for these applications that might impact you. It's not hard and not difficult, but that's the tradeoff of having a single module managing different applications.

Changes on the **tp**, which contains code and not data, instead, are much more controlled and fully follow SemVer conventions.

As alternative to the usage of a custom tinydata module or fork, you can override the defaults tinydata settings. Let's say you want to install a custom apache package, coming from some internal repo, but keep all the other settings, you can write something as follows:

    tp::install { 'apache':
      settings_hash => {
        package_name => 'my_httpd',
      }
    }

Even better, to be sure that we use the same settings for all the related defines, place your settings in a variable (whose content can come from Hiera) and use it wherever needed:

    $apache_settings = {
      package_name => 'my_httpd',
    }
    tp::install { 'apache':
      settings_hash => $apache_settings,
    }
    tp::conf { 'apache::mime.types':
      settings_hash => $apache_settings,
      [...]
    }

More information about how to use Tiny Data to configure custom applications and how to use tp defines in custom profiles, can be read in [this blog post](https://www.example42.com/2018/10/15/application-management-using-tinypuppet/).

The full list of the currently used available tinydata settings is defined in the [tp::settings data type](https://github.com/example42/puppet-tp/blob/master/types/settings.pp), note however that currently this is not enforced or used for validation of the `settings_hash` parameter.

More information on the tiny data settings you can configure and customize to adapt to local versions of supported application or totally new applications, have been described in a recent posts series, where we described and updated info on:

  - [Tiny Puppet principles](https://www.example42.com/2019/12/09/request-for-tinydata-part1/)
  - [Details on Tiny data structure](https://www.example42.com/2019/12/12/request-for-tinydata-part2/)
  - [Fancy and powerful features](https://www.example42.com/2019/12/16/request-for-tinydata-part3/) on how to check for config files syntax, how to use upstream repos or run an application in a container.
  - [How to manage ANY application](https://www.example42.com/2019/12/19/request-for-tinydata-part4/)

One of the interesting things I noticed reading the past blog posts mentioned in this article is that most of their contents are still actual and valid: I'm not sure if this is a good or bad sign.

Has Tiny Puppet been sane enough since the beginning or is it simply never evolved too much?

Whatever the answer, it's still here, and, as far as we know, it's used in Startups, Top 100 companies, Government institutions and Central Banks.

So, I guess, it just works.

Alessandro Franceschi
