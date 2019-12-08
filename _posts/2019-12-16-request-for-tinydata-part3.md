---
layout: blog
title: Puppet Tip 109 - Request for Tiny Data - Part 3
---

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

the second, when repo_package_url is defined, involves setting the download url of the release package, with all the necessary repository configurations:

    puppet::settings:
      repo_package_url: 'https://yum.puppet.com/puppet/puppet-release-el-7.noarch.rpm'

#### Managing application upstream repositories

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

