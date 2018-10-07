---
layout: blog
title: Tip of the Week 93 - Upgrading to Puppet 6 CA
---

In our [last blog post](https://www.example42.com/2018/10/01/what-s-new-with-puppet-6/) we covered all the new features of Puppet 6.

Now we look forward on how to migrate to the new CA.

* Table of content
{:toc}

## CA usage on Puppet 5 and earlier

The CA and certificate management was usually part of the Puppet Agent package.
All related commands were part of the `puppet` command:

    puppet cert list [--all]
    puppet cert sign <certname>
    puppet cert print <certname>
    puppet cert revoke <certname>
    puppet cert clean <certname>

## The Puppet 6 CA

Starting with Puppet 5.5 you will recognize that Puppet CA and certificate management will be moved from Puppet Agent to Puppetserver in Puppet 6.
Puppet 5.5 prepares you by providing deprecation information in the Puppet server logfile and on the command line.

The Puppetserver handles certificate management via API calls. All Puppetserver APIs are protected with an authorization layer for read and write access. This authorization and access control is also done for the certificate management API.

Within a newer Puppet server, you will find two new entries in the authorization configuration file located at `/etc/puppetlabs/puppetserver/conf.d/auth.conf`:

        {
            # Allow the CA CLI to access the certificate_status endpoint
            match-request: {
                path: "/puppet-ca/v1/certificate_status"
                type: path
                method: [get, put, delete]
            }
            allow: {
               extensions: {
                   pp_cli_auth: "true"
               }
            }
            sort-order: 500
            name: "puppetlabs cert status"
        },
        {
            # Allow the CA CLI to access the certificate_statuses endpoint
            match-request: {
                path: "/puppet-ca/v1/certificate_statuses"
                type: path
                method: get
            }
            allow: {
               extensions: {
                   pp_cli_auth: "true"
               }
            }
            sort-order: 500
            name: "puppetlabs cert statuses"
        },

Within the allow section we see the default settings, which now requires the Puppet server ca certificate to have the `pp_cli_auth` extension set.

Let's analyze the new Puppet 6 CA certificate:

    openssl x509 -noout -text -in /etc/puppetlabs/puppet/ssl/certs/$(puppet config print certname).pem
    [...]
            X509v3 extensions:
            Netscape Comment:
                Puppet Server Internal Certificate
            X509v3 Authority Key Identifier:
                keyid:B3:DC:C3:68:D5:3A:A8:A3:30:3C:EB:85:79:0F:EB:9E:1A:82:5E:7A

            X509v3 Subject Key Identifier:
                1F:32:B6:9D:D0:9F:9D:57:8A:57:D6:DE:42:45:78:6D:27:D3:A1:15
            1.3.6.1.4.1.34380.1.3.39:
                ..true
    [...]

Here we see a new entry with an OID (1.3.6.1.4.1.34380.1.3.39) and the value set to true.

## Migrating to Puppet 6 CA

In general you have multiple possibilities which you can follow when upgrading to Puppet 6:

1. new CA and certificates
2. modify auth.conf to use old CA certificate
3. modify existing CA certificate and add required extension

### New CA

Usually you barely want to follow this option as this does mean a complete CA roll-over within all of your Puppet managed systems.
Maybe this is an option in case that your CA is about to expire soon?

We will look into the two solutions which do not require new certificates:

### auth.conf

Within `/etc/puppetlabs/puppetserver/conf.d/auth.conf` you want to add your Puppet server:

        {
            # Allow the CA CLI to access the certificate_status endpoint
            match-request: {
                path: "/puppet-ca/v1/certificate_status"
                type: path
                method: [get, put, delete]
            }
            allow: {
               extensions: {
                   pp_cli_auth: "true"
               }
            }
            allow: master.example.com   # <- add your puppet master certname
            sort-order: 500
            name: "puppetlabs cert status"
        },

Please try to not set `allow-unauthenticated: true`. Even though this is technically possible (e.g. if your VM management solution is not integrated or managed by Puppet), you can easily generate a certificate on the Puppet CA and copy it over to the system which is responsible for removing or signing certificates.

Please remember to restart your Puppet server process to activate changes.

### Modify CA cert

Another solution (untested) is to add the required extension to the Puppet CA certificate.
There is a project on [GitHub from smortex](https://github.com/smortex/puppet-add-cli-auth-to-certificate) which also has links to tickets at Puppet and which provides a ruby script which adds the required extension.

## Autosigning on Puppet 6 CA

Autosigning itself has not changed from Puppet 5 to Puppet 6.
The configuration is still done in Puppet configuration file (`/etc/puppetlabs/puppet/puppet.conf`) in `master` section:

    # /etc/puppetlabs/puppet/puppet.conf
    [master]
    autosign = false                              # <- disable autosign
    autosign = true                               # <- default, sign based on content of autosign.conf file (naive autosigning)
    autosign = /etc/puppetlabs/puppet/autosign.sh # <- script to execute: on exit 0 signing will take place (policy based autosigning)

## CA and certificate management on Puppet 6

The new CA management is completely integrated into Puppet server:

    puppetserver ca list [--all]
    puppetserver ca sign <certname>
    puppetserver ca print <certname>
    puppetserver ca revoke <certname>
    puppetserver ca clean <certname>

We wish everybody fun and success with Puppet 6,

Martin Alfke
