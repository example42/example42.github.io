---
layout: blog
title: Tip of the Week 77 - What you need to know about Puppet facts. Part 4 - Trusted facts
---

We continue our series with Facter with another thing you need to know: **trusted facts**, and their very particular nature.

But before beginning, if you missed something, here are the previous posts:
- [Part 1 - Facter and core facts](https://www.example42.com/2018/05/28/what-you-need-to-know-about-puppet-facts-part-1-core_facts/)
- [Part 2 - Custom facts](https://www.example42.com/2018/06/04/what-you-need-to-know-about-puppet-facts-part-2-custom_facts/)
- [Part 3 - External facts](https://www.example42.com/2018/06/11/what-you-need-to-know-about-puppet-facts-part-3-external_facts/)


### Trusted facts are Certificates's attributes

We call trusted facts what are, more precisely, [extensions](https://puppet.com/docs/puppet/5.3/ssl_attributes_extensions.html) to the Puppet agent x509 certificates, used in all the https communications with the server.

Trusted facts must be set before Puppet is executed the first time, and once set they can't be changed (unless the Puppet client certificate is recreated).

This is done by editing the file ```csr_attributes.yaml``` in the ```confdir```, so by default it's ```/etc/puppetlabs/puppet/csr_attributes.yaml```, here, in valid yaml format we can set:

- **custom_attributes**, key values that are added to the CSR but won't appear in the certificate, once signed.
They are typically used for managing [nodes' auto sign](https://puppet.com/docs/puppet/5.3/ssl_autosign.html)

- **extension_requests**, key values which are added to the CSR and in the generated certificate. These are what we call **trusted facts** in Puppet world.

A sample ```/etc/puppetlabs/puppet/csr_attributes.yaml``` can look like:

    ---
      extension_requests:
        pp_role: 'ci'
        pp_zone: 'lab'
        pp_environment: 'devel'
        pp_datacenter: 'us1'
        pp_application: 'jenkins'


### The $trusted fact

Puppet provides the $trusted variable, an hash containing information about the client certificate with the following keys:

- ```authenticated``` — if the catalog request was authenticated (remote, local, false)
- ```certname``` — the node’s certname
- ```domain``` — the node’s domain, as derived from its validated certificate name.
- ```extensions``` — the hash containing any custom extensions we have set in csr_attributes.yaml. Keys here are the extensions OIDs, or, if they must registered extensions, their relevand short names.

There's already a list of Puppet registered [ID extensions](https://puppet.com/docs/puppet/5.3/ssl_attributes_extensions.html#puppet-specific-registered-ids), and it's possible to add custom IDs to map by editing the [custom_trusted_oid_mapping.yaml](https://puppet.com/docs/puppet/5.3/config_file_oid_map.html) file.

So, we can access our trusted facts with ```$trusted[extensions][<EXTENSION OID>]```, the above sample csr_attributes.yaml file would generate a $trusted fact with these values:

    {
      'authenticated' => 'remote',
      'certname'      => 'jenkins.lab.psick.io',
      'domain'        => 'lab.psick.io',
      'extensions'    => {
                          'pp_application' => 'jenkins',
                          'pp_datacenter' => 'us1',
                          'pp_environment' => 'devel',
                          'pp_role' => 'ci',
                          'pp_zone' => 'lab',
                          '1.3.6.1.4.1.34380.1.2.1' => 'ssl-termination'
                       },
      'hostname'      => 'jenkins'
    }

In our Puppet code we can have something like:

    if $trusted['extensions']['pp_role'] and !has_key($facts,'role') {
      $role = $trusted['extensions']['pp_role']
    }
    if $trusted['extensions']['pp_environment'] and !has_key($facts,'env') {
      $env = $trusted['extensions']['pp_environment']
    }
    if $trusted['extensions']['pp_datacenter'] and !has_key($facts,'datacenter') {
      $datacenter = $trusted['extensions']['pp_datacenter']
    }
    if $trusted['extensions']['pp_zone'] and !has_key($facts,'zone') {
      $zone = $trusted['extensions']['pp_zone']
    }
    if $trusted['extensions']['pp_application'] and !has_key($facts,'application') {
      $application = $trusted['extensions']['pp_application']
    }

If we do this in our main ```manifests/site.pp``` we have top scope variables like $role, $env and so on which can be used in our Hiera hierarchies.



Alessandro Franceschi
