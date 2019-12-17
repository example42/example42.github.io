---
layout: blog
title: Puppet Tip 109 - Request for Tiny Data - Part 3 - Tiny, fancy and powerful features
---

Here is the is the third part of a blog series on our Request for for Tiny Data.

Previously we have:

- [Part 1](https://www.example42.com/2019/12/09/request-for-tinydata-part1/){:target="_blank"} - Introduced Tiny Puppet and where it can be used
- [Part 2](https://www.example42.com/2019/12/12/request-for-tinydata-part2/){:target="_blank"} - Described how to write Tiny Data

Here we are going to reveal some new and not so new features of Tiny Data:

### Managing additional repositories

There 2 ways to are manage repos, the first is to specify the typical data to use in apt repos:

    elasticsearch::settings:
      init_file_path: '/etc/default/elasticsearch'
      repo_url: 'http://packages.elastic.co/elasticsearch/2.x/debian'
      key: 'D88E42B4'
      key_url: 'https://packages.elastic.co/GPG-KEY-elasticsearch'
      apt_repos: 'main'
      apt_release: 'stable'
      apt_key_server: 'http://pgp.mit.edu'

or yum repos:

    elasticsearch::settings:
      init_file_path: '/etc/sysconfig/elasticsearch'
      repo_url: 'http://packages.elastic.co/elasticsearch/2.x/centos'
      key: 'D88E42B4'
      key_url: 'http://packages.elastic.co/GPG-KEY-elasticsearch'

the second, when `repo_package_url` is defined, involves setting the download url of the release package, with all the necessary repository configurations:

    puppet::settings:
      repo_package_url: 'https://yum.puppet.com/puppet/puppet-release-el-7.noarch.rpm'

### Managing application upstream repositories

We have recently added to the `tp::install` define a very powerful parameter: `upstream_repo`, which allows users to **install an app from its own upstream repositories**.

So, if you want to install a package using the native OS packages, you simply can have a manifest with:

```shell
tp::install { 'puppet': }
```

but if you want to install the same application using the upstream Puppet repositories, provided by the same application authors, you can write:

```puppet
tp::install { 'puppet':
  upstream_repo => true,
}
```

All the tinydata necessary and specific to the upstream repo packages, in placed in (for this case with puppet) the [data/puppet/upstream](https://github.com/example42/tinydata/tree/master/data/puppet/upstream){:target="_blank"} directory.

This is a new feature and we currently have very few application with upstream data info. 

### Managing checks on configuration files

Puppet has a not much known feature for the file resource: the [argument validate_cmd](https://www.example42.com/2017/11/13/checking-config-files-before-applying-them/){:target="_blank"} which allows to check, with the command passed as argument, the syntax of the file we are managing before changing it on the system.

Almost no module uses this feature, Tiny Puppet does it, potentially for any application, in reality for any application for which there's the relevant Tiny Data (and, yes, you can help us in improving Tiny Data).

This is a partial set of tinydata for apache:

  ---
  apache::settings:
    package_name: 'httpd'
    service_name: 'httpd'
    config_file_path: '/etc/httpd/conf/httpd.conf'
    config_dir_path: '/etc/httpd'
    tcp_port: '80'
    pid_file_path: '/var/run/httpd.pid'
    log_file_path: [ '/var/log/httpd/access.log' , '/var/log/httpd/error.log' ]
    log_dir_path: '/var/log/httpd'
    data_dir_path: '/var/www/html'
    process_name: 'httpd'
    process_user: 'apache'
    process_group: 'apache'
    nodaemon_args: '-DFOREGROUND'
    validate_cmd:
      config: 'httpd -t -f %'

Note the hash for validate_cmd, where we can use different commands for different kind of files (here we set the command to check for the file defined by `**config**_file_path` ).
As everything in Tiny Data, settings can be overridden for different OS, so for Debian OS family, the above data is overridden by:

    ---
    apache::settings:
      package_name: 'apache2'
      service_name: 'apache2'
      config_file_path: '/etc/apache2/apache2.conf'
      init_file_path: '/etc/default/apache2'
      config_dir_path: '/etc/apache2'
      mods-available_dir_path: '/etc/apache2/mods-available'
      mods-enabled_dir_path: '/etc/apache2/mods-enabled'
      sites-available_dir_path: '/etc/apache2/sites-available'
      sites-enabled_dir_path: '/etc/apache2/sites-enabled'
      conf-available_dir_path: '/etc/apache2/conf-available'
      conf-enabled_dir_path: '/etc/apache2/conf-enabled'
      conf_dir_path: '/etc/apache2/conf.d'
      pid_file_path: '/var/run/apache2.pid'
      log_file_path: [ '/var/log/apache2/access.log' , '/var/log/apache2/error.log' ]
      log_dir_path: '/var/log/apache2'
      data_dir_path: '/var/www'
      process_name: 'apache2'
      process_user: 'www-data'
      process_group: 'www-data'
      validate_cmd:
        config: 'apache2 -t -f %'

That's it, when you use `tp::conf { 'apache': }` you have, out of the box, automatic validation of the syntax of your Apahce (main) configuration file.

### Run app in container

In the above data you might have noticed the `nodaemon_args` setting. It's used to specify what argument has to be used to run the application in foreground.

Yes, you are guessing right, we use it to build Docker images where app has to be launched in foreground and not as a background service.

In the past we engineered a process to build images using Tiny Puppet, **without** having Puppet installed on the target image! There are fragments of such works in our psick control repo and other collateral projects but, we must admit, works here have been stale for long.


### Request for Tiny Data!

We would love to add upstream_repo support by default to all our apps and add as much validate_cmd and nodaemon_args settings as possible.

Still we have to know know what to prioritize, and you can help with that, in many ways:

- **Let us know**, in any way (tweet, comment, mail, voice) **what app** you would like to quickly manage via tp
- **Open a [ticket on Github](https://github.com/example42/tinydata/issues){:target="_blank"}** for a **new app** support. Possibly provide context and relevant information
- **Open a [ticket](https://github.com/example42/tinydata/issues){:target="_blank"}** for the **applications missing upstream repo data** you would like.
- **Do directly the work** with updated tinydata and submit a **[Pull Request](https://github.com/example42/tinydata/pulls){:target="_blank"}**

