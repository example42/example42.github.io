---
layout: blog
title: Tip of the Week 11 - Using a second mount point for files
---

Credentials with a certain level of security should never be stored in plain text on a Puppet server.

How about items that shpuld be managed by another team (e.g. Security and Compliance) but the team insists that these data may not be part of the standard Puppet environments?

In this case one can make use of a second file mountpoint.
Using a second mount point within Puppet code follows the already well known pattern for delivering static configuration files using file resource type and source property:

    class my_certs {
      file { '/etc/ssl/certs/my_company_ca.pem':
        ensure => file,
        source => 'puppet:///certs/my_company_ca.pem',
      }
    }

Do you recognize the pattern?

Let's compare this with a "normal" file source declaration where we fetch the file from the module files directory:

    class my_old_certs {
      file { '/etc/ssl/certs/my_company_ca_old.pem':
        ensure => file,
        source => 'puppet:///modules/my_old_certs/my_company_ca_old.pem',
      }
    }

The second declaration uses the file from the module. Directory layout is the following:

    <modulepath>/my_old_certs/
                        |- manifests/
                        |         \- init.pp
                        \- files/
                               \- my_company_ca_old.pem

Adding a second mount point is straight forward.
Just add the following snippet to ```/etc/puppetlabs/puppet/fileserver.conf```.

    # /etc/puppetlabs/puppet/fileserver.conf
    [certs]
    path /opt/security/data/certs/
    allow *

Don't forget to restart the puppetserver process

    # On Open Source
    service puppetserver restart
    # On Puppet Enterprise
    service pe-puppetserver restart

Now one can use the new mountpoint easily in Puppet code:

    class my_certs {
      file { '/etc/ssl/certs/my_company_ca.pem':
        ensure => file,
        source => 'puppet:///certs/my_company_ca.pem'
      }
    }

File system layout looks the following:

    /opt/security/data/certs
                        \- my_company_ca.pem

This concept allows you to easily store information on the master in a specific path without these information being part of the Puppet environment DSL code.

Martin Alfke
