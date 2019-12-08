---
layout: blog
title: Puppet Tip 108 - Request for Tiny Data - Part 2 - Tiny data exposed
---

This is the **second** of **four** post series for our call for Tiny Data.

In the first post we introduced Tiny Puppet (tp), now we are going to talk about what feeds it:

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

Tiny data can currently define:

  - packages to install, services and the typical configuration files to manage
  - **date for additional software repositories** to configure before trying to install the relevant application's package
  - how to launch the application in a docker instance
  - what command to use to validate the syntax of the app configuration files
  - what ports, pids, users are used with the application, used for monitoring and availability checks

### Request for Tiny Data!

You see? Writing tiny data is not difficult, and it's very fast once you know these principles.

If you want to improve existing data or have data for new applications, you can:

- **Let us know**, in any way (tweet, comment, mail, voice) **what app** you would like to quickly manage via tp
- **Open a [ticket on Github](https://github.com/example42/tinydata/issues){:target="_blank"}** for a **new app** support. Possibly provide context and relevant information
- **Open a [ticket](https://github.com/example42/tinydata/issues){:target="_blank"}** for **incorrect, incomplete or not updated** existing tiny data
- **Do directly the work** with updated tinydata and submit a **[Pull Request](https://github.com/example42/tinydata/pulls){:target="_blank"}**

In any case we will try to give our **example42 answer**.
