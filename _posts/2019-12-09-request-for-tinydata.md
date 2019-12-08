---
layout: blog
title: Puppet Tip 107 - Request for Tiny Data
---

Before talking about Tiny data with have to mention

### Tiny Puppet (tp)

If you know something about example42, you should know that we developed [Tiny Puppet](https://github.com/example42/puppet-tp){:target="_blank"} (tp), a Puppet module which allows to manage potentially **any application** on any **Operating System**.

What exactly, currently Tiny Puppet can manage?

**Any application** that can be installed via a Puppet **package** resource.

On What Operating Systems?

- Mostly **Linux** (RedHat, Debian, Suse and derivatives)
- But also **Solaris**, **BSDs** and **Darwin** (with brew-cask)
- And potentially also **Windows** (with Chocolatey).

What you can use it for?

- Quickly install, test, show logs of the managed applications, from the shell
- Manage applications installation and configuration in Puppet manifests. such as
  - Local profiles, with our code, our files and logic 
  - Possibly, optionally, in component modules, to benefit from tp integrations
  - Ready for Hiera use collections, like the [tp-profiles],

Just to give you an idea, the following code:

    class profile::openssh (
      String $template = 'profile/openssh/sshd_config.erb',
      Hash $options    = {},
    ) {

      tp::install { 'openssh': }
      tp::conf { 'openssh':
        template     => $template,
        options_hash => $options,
      }
      # Alternative which does the same:
      # tp::conf { 'openssh':
      #   content => template($template),
      # }      
    }

will install the package, configure the file with the contents we want, manage the service (taking care of dependencies and different names and paths) for openssh.

The example used here for openssh can be done **virtually for all applications you can think about** (for which there's a package to install and the right tinydata).

This can be useful when **we know how to configure our application**, and we want a quick way to puppettize it without getting lost in finding the right component modules with its bunch of dependencies, in a way the allows us to concentrate just on the data to customise, which, for the above example, could be Hiera data as follows:

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

Tiny Puppet actually has a, non intrusive, dependency: the [tinydata](https://github.com/example42/tinydata){:target="_blank"} module.

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

The current list of applications support by Tiny Puppet is basically the list of directories in the [data directory](https://github.com/example42/tinydata/tree/master/data){:target="_blank"},
in each of these directories, there's a `hiera.yaml` file which configures the hierarchy that tp has to use to look for that application tinydata.

For example, a common hierarchy, used also for the openssh application, is: 

    ---
    :hierarchy:
      - "%{title}/osfamily/%{osfamily}/%{operatingsystemmajrelease}"
      - "%{title}/osfamily/%{osfamily}"
      - "%{title}/default"
      - "default/%{operatingsystem}"
      - default

This tells tiny puppet in what files to look for tinydata starting from:

- OSfamily files specific for the app, here in [data/openssh/osfamily](https://github.com/example42/tinydata/tree/master/data/openssh/osfamily){:target="_blank"}
- Application defaults [data/openssh/default.yaml](https://github.com/example42/tinydata/tree/master/data/openssh/default.yaml){:target="_blank"}
- OS specific general data in [data/default/](https://github.com/example42/tinydata/tree/master/data/default){:target="_blank"}
- the defaults in [data/default.yaml](https://github.com/example42/tinydata/blob/master/data/default.yaml){:target="_blank"}

Lookup is an hiera like (note that Hiera is not actually used to get his data): first value found while crossing the hierarchy has precedence on values found, for any key, at lower hierarchy levels.


Tiny data can define:

  - packages to install, services and the typical configuration files to manage
  - **date for additional software repositories** to configure before trying to install the relevant application's package
  - how to launch the application in a docker instance
  - what command to use to validate the syntax of the app configuration files
  - what ports, pids, users are used with the application, used for monitoring and availability checks

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

## Request for Tiny Data!

So, here is our **call for tiny data**.

We have tinydata for *some* applications:

    ls -la data/ | wc -l
      179

the common ones or what we needed or found interesting.

Still there's more.

A lot of wonderful applications that would be great to be able to install on a shell command:

    tp install wonderapp

or manage with a Puppet define:

    tp::install { 'wonderapp': }

On any Linux, and maybe Mac and Windows.

With the quick choice of using the default OS packages, the app upstream repo or any other repo might be configured.

    tp::install { 'wonderapp': 
      upstream_repo => true|false,
    }

We know we can add new data very easily, and relatively quickly.

We don't know what application interests you.

Please engage with, in effort order:

- **Let us know**, in any way (tweet, comment, mail, voice) **what app** you would like to quickly manage via tp
- **Open a [ticket on Github](https://github.com/example42/tinydata/issues){:target="_blank"}** for a **new app** support. Possibly provide context and relevant information
- **Open a [ticket](https://github.com/example42/tinydata/issues){:target="_blank"}** for **incorrect, incomplete or not updated** existing tiny data
- **Do directly the work** with updated tinydata and submit a **[Pull Request](https://github.com/example42/tinydata/pulls){:target="_blank"}**

Our goal is, on any OS, to:

    tp install everything

Now **let's define everything** together.
