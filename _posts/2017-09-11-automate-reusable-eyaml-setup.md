---
layout: blog
title: Tip of the Week 37 - Automated, reusable hiera eyaml setup
---

Many people prefer to have sensitive data not in plain text in hiera. Instead of plain text the [eyaml](https://github.com/voxpupuli/hiera-eyaml) - encrypted yaml - hiera extension is widely used.
But how to deal with public/private key pair? Where to store them? Where to place them?

Why do you want to store your keys?

After bootstrapping your Puppet server and installing eyaml you usually run the ```eyaml createkeys``` command. This generates a private/public key pair.

Now you start encrypting your data using ```eyaml encrypt```.
For encryption only the public key is required.

Normally you will work with a larger group of people on your configuration automation and management. So you will not directly work on the puppet server.
Additionally you want everybody to encrypt data, but only dedicated users or systems should be able to decrypt data.

To allow everybody encrypting data, you can easily place the public key into your control-repository.

The private key must be protected and kept safe. So you will not put it into the control-repo.

When re-bootstrapping your Puppet server, you must ensure that you are re-using the old keys which already have been used to decrypt data.
Otherwise the hiera lookup will complain about a bad key if keys gets re-created.

Which systems must have the private key?

First it is your Puppet server(s) so data lookups can be decrypted.

Depending on your spec tests you want your ci systems to also have the private key at hand. On the CI systems you can easily place the key via Puppet, using another file serving mount point (see post [Using a second mount point for files](https://www.example42.com/2017/03/13/second_mount_point/)).

On the Puppet server bootstrapping you must install the private key from a secure location, e.g. vault.

Your hiera.yaml file can now use the public key in the control-repository and the private key in a separate directory:

    ---
    version: 5

    defaults:
      datadir: hieradata

    hierarchy:
      - name: "Eyaml hierarchy"
        lookup_key: eyaml_lookup_key # eyaml backend
        paths:
          - "nodes/%{trusted.certname}.yaml"
          - "role/%{::role}-%{::env}.yaml"
          - "role/%{::role}.yaml"
          - "zone/%{::zone}.yaml"
          - "common.yaml"
        options:
          pkcs7_private_key: /etc/keys/private_key.pkcs7.pem
          pkcs7_public_key:  keys/public_key.pkcs7.pem # relative path in control-repository

example42 wishes everybody fun and success at encrypting data.

Martin Alfke
