---
layout: blog
title: Puppet Tip 107 - Request for Tiny Data
---

If you know something about example42, you should know that we developed Tiny Puppet, a Puppet module which allows to manage potentially **any application** on any **Operating System**.

What application? Anything that can be installed via a Puppet **package** resource.

What Operating Systems? Mainly **Linux** (RedHat, Debian, Suse and derivatives) but also **Solaris**, **BSDs** and **Darwin** (with brew-cask), **Windows** (with Chocolatey).

It's supposed to be used in local profiles, when for a given application we just need to manage package, service, and configuration file(s) triplet. Just to give you the following code:

    class profile::openssh (
      String $template = 'profile/openssh/sshd_config.erb',
      Hash $options    = {},
    ) {

      tp::install { 'openssh': }
      tp::conf { 'openssh':
        template     => $template,
        options_hash => $options,
      }
      # Alternative to do the same:
      # tp::conf { 'openssh':
      #   content => template($template),
      # }      
    }

Will install the package, configure the file, manage the service (taking care of dependencies and different names and paths) for openssh.

The example used here for openssh can be done virtually for all applications you can think about (for which there's a package to install).

This can be useful when *we know how to configure* our application, and we want a quick way to puppettize it in the way the allow us to concentrate just on Hiera data, which, for the above example, could be as follows:

    profile::openssh::template: profile/openssh/sshd_config.erb
    profile::openssh::options:
      Protocol: 2
      PermitRootLogin: 'no'
      UsePAM: 'yes'
      TCPKeepAlive: 'yes'

Content of the template, to be placed in our profile module, could be something like what follows (plus all the necessary extra settings we may want to hard-code):

    # File managed by Puppet
    <% @options.each do |k,v| -%>
    <%= k %> <%= v %>
    <% end -%>

### Tiny data 

Tiny Puppet actually has a, non intrusive, dependency: the [tinydata](https://github.com/example42/tinydata) module.

Here is where the tp **magic** becomes plain information easy to read, fix, and improve.

Tinydata contains the info on package, service, files names, paths for any application supported by Tiny Puppet.

For example, openssh default tiny data looks as follows:

    ---
    openssh::settings:
      package_name: 'openssh-server' # The name (can be empty or an array) of the package to install
      service_name: 'ssh'            # The name (can be empty or an array) of the service to manage
      config_file_path: '/etc/ssh/sshd_config' # What you configure with a default tp::config { 'openssh': ... }
      config_file_mode: '0600'       # Mode of the main configuration file
      config_dir_path: '/etc/ssh'    # Path of the main configuration dir
      tcp_port: '22'                 # Listening port. This can be used for automatic monitoring
      pid_file_path: '/var/run/sshd.pid' # Can be used for automatic monitoring
      log_file_path: '/var/log/messages' # Used by the tp log command
      process_name: 'sshd'               # Can be used for automatic monitoring
      process_user: 'root'
      process_group: 'root'
      nodaemon_args: '-D'                # Used when starting the app in a container
      validate_cmd: 'sshd -t -f %'       # If present, the syntax of the config file is automatically validated before change

But there are variations for Debian and Derivatives:

    openssh::settings:
      config_file_mode: '0644'
      init_file_path: '/var/default/ssh' # The path of the 'init' file
      log_file_path: '/var/log/syslog'

or Solaris:

    openssh::settings:
      package_name: ''
      service_name: 'ssh'
      config_file_mode: '0600'
      log_file_path: '/var/adm/authlog'

### Adding tinydata

The current list of applications support by Tiny Puppet is basically the list of directories in the [data directory](https://github.com/example42/tinydata/tree/master/data),
in each of these directories, there's a `hiera.yaml` file which configures the hierarchy of the files where to look for the tinydata for each app on different OS.

For example, a common hierarchy, used also for the openssh application, is: 

    ---
    :hierarchy:
      - "%{title}/osfamily/%{osfamily}/%{operatingsystemmajrelease}"
      - "%{title}/osfamily/%{osfamily}"
      - "%{title}/default"
      - "default/%{operatingsystem}"
      - default

This tells tiny puppet in what files to look for tinydata starting from:

- OSfamily files specific for the app, here in [data/openssh/osfamily](https://github.com/example42/tinydata/tree/master/data/openssh/osfamily)
- Application defaults [data/openssh/default.yaml](https://github.com/example42/tinydata/tree/master/data/openssh/default.yaml)
- OS specific general data in [data/default/](https://github.com/example42/tinydata/tree/master/data/default)
- the defaults in [data/default.yaml](https://github.com/example42/tinydata/blob/master/data/default.yaml), 

Lookup is an hiera like (note that Hiera is not actually used to get his data): first value found while crossing the hierarchy has precedence on values found, for any key, at lower hierarchy levels.

### Managing repositories

Tinydata does not only contains info on the packages to install, the services to manage and the typical configuration files to manage, it can provide information on additional software repositories, to automatically configure before trying to install the relevant application's package.

There are different keys available for managing repos:

Specifying the typical data to use in apt repos:

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

or, alternatively, just setting the url of the release package, with all the necessary configurations:

    puppet::settings:
      repo_package_url: 'https://yum.puppet.com/puppet/puppet-release-el-7.noarch.rpm'

We have recently added to to the tp::install a very powerful parameter : upstream_repo, which allows users to install an app from its upstream repositories:

So, if you want to install a package using the native OS packages, you simply can have a manifest with:

    tp::install { 'puppet': }
    
but if you want to install the same application using the upstream repositories, provided by the same application authors, you can write:

    tp::install { 'puppet':
      upstream_repo => true,
    }

All the tinydata necessary and specific to the upstream repo packages, in placed in (for this case with puppet) the [data/puppet/upstream](https://github.com/example42/tinydata/tree/master/data/puppet/upstream) directory.

This is a new feature and we currently have very few application with upstream data info. 

### Request for tinydata

So, here is our call for tiny data.

We have tinydata for *some* applications, the ones we needed or found interesting, but we don't know what people might be interested to.

Or what OS support they would like.

Or for what applications they want the option to choose native or upstream packages.

Just open a [ticket on Github](https://github.com/example42/tinydata/issues), either with the name of the app you want to manage with Tiny Puppet, or which ones needs fixing, support for new OS versions, or data for upstream packages.

And if you feel brave enough, submit your tinydata to improve the app and os coverage.