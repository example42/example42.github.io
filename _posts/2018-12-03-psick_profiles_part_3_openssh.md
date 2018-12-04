---
layout: blog
title: Tip of the Week 101 - Psick profiles. Part 3 - Managing OpenSSH
---

On the [first post](https://www.example42.com/2018/11/12/psick_profiles_part_1_overview/){:target="_blank"} of our series on Psick profiles we introduced the psick module and had an overview of its reusable profiles.

On the [second one ](https://www.example42.com/2018/11/19/psick_profiles_part_2_proxy_and_hostname_settings/){:target="_blank"} we described how to manage hostname and proxy settings with the existing psick profiles.

In this post we are going to review the resources that psick module provides to manage OpenSSH.

The main `psick::openssh` profile, if included, installs openssh via Tiny Puppet (via the `psick::openssh::tp` class) and exposes parameters that act as entry points to configure other openssh related resources:

 - psick::openssh::configs_hash expects an hash (looked via Hiera in deep merge mode) of `psick::openssh::config` resources which permit the configuration of users' `~/.ssh/config` file

 - psick::openssh::keygens_hash expects an hash (looked via Hiera in deep merge mode) of `psick::openssh::keygen` resources which runs the keygen command to generate ssh keypairs for users.

 - psick::openssh::keypairs_hash expects an hash (looked via Hiera in deep merge mode) of `psick::openssh::keypair` resources which allow to manage ssh keypairs for users.

 - psick::openssh::keyscans_hash expects an hash (looked via Hiera in deep merge mode) of `psick::openssh::keyscan` resources which make a ssh keyscan of remote nodes and add their ssh host key to users' known hosts file.

Let's explore the mentioned resources, as they do commonly used operations.

## Define psick::openssh::config to manage users' ssh configs

The ssh config file for single users can be managed with code as (the titles snd parameters used here can be expressed via Hiera with the previously described keys):

The content of the file can be managed in different ways. With the source parameter:

    psick::openssh::config { 'al':
      source => 'puppet:///modules/profile/openssh/al/config',
    }

With an explicit content parameter (alternative to source):

    $sshconfig = @("SSHCONFIG"/L)
    Host *
      ForwardAgent no
      TCPKeepAlive yes
    | SSHCONFIG

    psick::openssh::config { 'al':
      content => $sshconfig,
    }

Or also with the template parameter, which can be coupled with a custom set of settings via the options_hash parameter:

    psick::openssh::config { 'al':
      template     => 'profile/openssh/user_config.erb',
      options_hash => $ssh_parameters,
    }

Since we need to have the directory .ssh created, we can instruct the define to automatically create it for us. Default value is false to prevent issues with duplicated resources:

    psick::openssh::config { 'al':
      source => 'puppet:///modules/profile/openssh/users/al/config',
      create_ssh_dir => true, # Default: false
    }

Note: All the psick::openssh:: defines have create_ssh_dir parameter, default value is false for all of them except psick::openssh::keypair.

## Define psick::openssh::keygen to create ssh keypairs

This define creates a ssh keypair using the ssh-keygen command. There are various options to manage where, how and for whom the ssh public and private keys have to created.

The simplest use, is just to specify as title the username to create keypairs in the default paths ( ~/.ssh/id_rsa , ~/.ssh/id_rsa.pub):

    psick::openssh::keygen { 'al': }

To customise the home, for example:

    psick::openssh::keygen { 'jenkins':
      home => '/var/lib/jenkins'
    }

## Define psick::openssh::keypair to manage ssh keypairs

If we want to manage directly the contents of our ssh keys, instead of generating them with psick::openssh::keygen, we can use the define psick::openssh::keypair where we have different options to manage the content of the ssh keys.

    psick::openssh::keypair { 'al':
      private_key_content => lookup('ssh_private_key_al'),
      public_key_source   => 'puppet:///modules/profile/openssh/al/id_rsa.pub'
    }


## Define psick::openssh::keyscan to pre fetch ssh host keys

When you need to automate ssh connection you need to have the remote hosts' ssh keys added to local users' or system's known_hosts file.

Usually this is done at the first ssh connection to a new host, by accepting manually the remote host key, the psick::openssh::keyscan does this for us.

Simple usage is:

    psick::openssh::keyscan { git.example.com:
      user => 'jenkins',
    }

## Sample hiera data for psick::openssh

Here's how Hiera data for an openssh configuration may look like:

    psick::openssh::tp::resources_hash:
      tp::conf:
        openssh:
          template: 'psick/generic/spaced.erb'
          options_hash:
            Protocol: 2
            PermitRootLogin: 'no'
            Subsystem: 'sftp /usr/libexec/openssh/sftp-server'

    psick::openssh::configs_hash:
      jenkins:
        path: /var/lib/jenkins/.ssh/config
        create_ssh_dir: true
        options_hash:
          Host puppet.lab.psick.io:
            StrictHostKeyChecking: no
            UserKnownHostsFile: /dev/null
          Host puppet:
            StrictHostKeyChecking: no
            UserKnownHostsFile: /dev/null

    psick::openssh::keyscans_hash:
      github.com:
        user: jenkins
        known_hosts_path: /var/lib/jenkins/.ssh/known_hosts


    psick::openssh::keygens_hash:
      jenkins:
      home: /var/lib/jenkins

Have fun with Puppet, Life, Universe and Everything.

Alessandro Franceschi
