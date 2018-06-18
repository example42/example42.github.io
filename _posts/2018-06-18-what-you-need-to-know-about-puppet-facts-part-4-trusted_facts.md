---
layout: blog
title: Tip of the Week 77 - What you need to know about Puppet facts. Part 4 - Trusted facts
---

Welcome to part 4 of a series of posts on what is essential to know about Facter: **trusted facts** and their very particular nature.

But before beginning, if you missed something, here are the previous posts:
- [Part 1 - Facter and core facts](https://www.example42.com/2018/05/28/what-you-need-to-know-about-puppet-facts-part-1-core_facts/)
- [Part 2 - Custom facts](https://www.example42.com/2018/06/04/what-you-need-to-know-about-puppet-facts-part-2-custom_facts/)
- [Part 3 - External facts](https://www.example42.com/2018/06/11/what-you-need-to-know-about-puppet-facts-part-3-external_facts/)


### Trusted facts are Certificate's extensions attributes

We call trusted facts what are, more precisely, [extensions](https://puppet.com/docs/puppet/5.3/ssl_attributes_extensions.html) to the Puppet agent x509 certificates, used in all the https communications with the server.

Trusted facts **must** be set before Puppet is executed the first time, and once set they can't be changed (unless the Puppet client certificate is removed recreated).

This is done by editing the file ```csr_attributes.yaml``` in the ```confdir``` (so by default it's ```/etc/puppetlabs/puppet/csr_attributes.yaml```) where, in valid yaml format, we can set:

- **custom_attributes**, key values that are added to the CSR but won't appear in the certificate, once signed.
They are typically used for managing [nodes' auto sign](https://puppet.com/docs/puppet/5.3/ssl_autosign.html)

- **extension_requests**, key values which are added to the CSR and in the generated certificate. These are what we call **trusted facts** in Puppet world.

A sample ```/etc/puppetlabs/puppet/csr_attributes.yaml``` can look like:

    ---
    custom_attributes:
      1.2.840.113549.1.9.7: 342thbjkt82094y0uthhor289jnqthpc2290  
    extension_requests:
      pp_role: 'ci'
      pp_zone: 'lab'
      pp_environment: 'devel'
      pp_datacenter: 'us1'
      pp_application: 'jenkins'


### The $trusted fact

In Puppet we have an handy ```$trusted``` variable, an hash containing information about the client certificate with the following keys:

- ```authenticated``` — if the catalog request was authenticated (remote, local, false)
- ```certname``` — the node’s certificate name
- ```domain``` — the node’s domain, as derived from its validated certificate name.
- ```extensions``` — the hash containing any custom extensions we have set in ```csr_attributes.yaml```. Keys here are the extensions OIDs, or, if they are registered extensions, their relevant short names.

There's already a list of Puppet registered [ID extensions](https://puppet.com/docs/puppet/5.3/ssl_attributes_extensions.html#puppet-specific-registered-ids), and it's possible to add custom IDs to map by editing the [custom_trusted_oid_mapping.yaml](https://puppet.com/docs/puppet/5.3/config_file_oid_map.html) file.

So, we can access our trusted facts with ```$trusted[extensions][<EXTENSION OID>]```, the above sample ```csr_attributes.yaml``` file would generate a ```$trusted``` variable as follows:

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

We can directly refer to trusted facts in our Hiera hierarchies:

      - "nodes/%{trusted.certname}.yaml"
      - "roles/%{trusted.extensions.pp_role}.yaml"
      - "zones/%{trusted.extensions.pp_zone}.yaml"

Or in our Puppet code:

    if $trusted['extensions']['pp_role'] {
      $role = $trusted['extensions']['pp_role']
    }
    if $trusted['extensions']['pp_zone'] {
      $zone = $trusted['extensions']['pp_zone']
    }

If we had the above variables set at top scope, in a place like ```manifests/site.pp``` we could have an hierarchy equivalent to the previous example, which looks like:

    - "nodes/%{trusted.certname}.yaml"
    - "roles/%{::role}.yaml"
    - "zones/%{::zone}.yaml"

### Conclusions

When have seen that trusted facts are *hardcoded* in the Puppet client certificate, that can be set by editing the ```csr_attributes.yaml``` file before launching Puppet the very first time on a node.

They can't be altered, unless the client ssl certificate is cleaned and regenerated with updated attributes, so we can decide to use them or not according to our use cases.

If we decide to use them in our Hiera hierarchies we need a way to automate the provisioning of different nodes with different trusted facts.

With this approach we can decide to use such custom facts to configure and classify our nodes entirely via Hiera.

The same can be achieved with normal custom or external facts, which have the benefit or defect of being more easily changeable during a node' lifetime.

As usual different approaches are possible, according to our needs, what's essential is to know the landscape.

Alessandro Franceschi
