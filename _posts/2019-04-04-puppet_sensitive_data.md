---
layout: blog
title: Puppet Tip 106 - Sensitive Data in Puppet
---

Securing important and sensitive information with Puppet is a long time issue.

There are at least three different locations where one has to deal with securing information.

The most well known is the Hiera data store, where many people today use **hiera-yaml** to encrypt values using a public-private key pair.

The next one is the catalog itself, where the Puppet server places data unencrypted inside. Ben Ford from Puppet provided a solution using **node_encrypt** module.

The third one is the Puppet report. Here we see file diffs, showing old and new password.

This is the topic we are dealing in today's Puppet Tip.

Let's start with the data type:

    class profile::db (
      Sensitive $password,
    ){
      file { '/etc/.db_password':
        ensure  => file,
        content => $password,
      }
    }

Within hiera one specifies the key-value pair:

    ---
    profile::db::password: ENC[PKCS7,Y22exl+O...]

But on the next Puppet agent run, we will receive an error message:

    Error: Could not retrieve catalog from remote server: Error 500 on SERVER: 
    Server Error: Evaluation Error: Error while evaluating a Function Call, 
    Class[Profile::Db]: parameter 'password' expects a Sensitive value, got 
    String (file: /etc/puppetlabs/code/environments/production/manifests/
    site.pp, line: 31, column: 3) on node master.example42.training

We need to inform hiera, that we want to receive the value as Sensitive data type by adding a lookup option:

    ---
    lookup_options:
      profile::db::password:
        convert_to: "Sensitive"
        
    profile::db::password: ENC[PKCS7,Y22exl+O...]

Any data which is based on Sensitive data type, will not be shown in a catalog diff:

    Notice: /Stage[main]/Profile::Db/File[/etc/.db_password]/ensure: changed [redacted] to [redacted]


example42 wishes everybody safety and success

Martin Alfke
