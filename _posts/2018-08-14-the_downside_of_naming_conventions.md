---
layout: blog
title: Tip of the Week 85 - The downside of server naming conventions
---

In the past we had our servers and handled them like pets. We loved and we hated them and we gave them names so it was easy for us to recognize which system we were working on.

We had names like *dbmaster*, *dbslave01* to *dbslave99*, *lb-ext* and *lb-int*. Our shell prompt directly showed us the system we were working on:

    [dbmaster] /etc $:

Some companies even have more information placed in the fqdn of a system:

    dc1_appf_01_t.domain.com

- dc1: Data Center 1
- appf: Frontend Application Server
- 01: Number
- t: Testing environment


* Table of content
{:toc}

## Pets versus cattle

Long living systems, where we did maintenance, OS upgrades and application updates, repair broken installations are called **pets**.
Similar to your dog or cat you look at them carefully and doing healthcare when required. You usually have only a few of them (well, some people who really love pets might have more) and you take any issue serious, trying to keep them alive as long as possible.

The opposite of this are short living systems, where you don't do OS upgrades, but reinstantiate the system with a new OS underneath. Switching back to the old version in case that something is not working. These systems are called **cattle**. Similar to cows, sheeps or ducks which you grow to use them afterwards. You have plenty of them and when one is going to become ill you will rarely do healthcare but remove it from the crowd and try to get a new one instead.

From data center perspective you can compare pets to OS running on hardware whereas cattle are virtual machines.

## Puppet and the pet node classification

When we introduced Puppet to manage our infrastructure we used the system hostnames for node classification. We created a long list of all nodes:

    node 'dbmaster' {
      contain role::dbmaster
    }
    node 'lb-int' {
      contain role::lb_int
    }

For multiple systems with identical use cases we had the option to use regular expressions:

    node /dbslave\d+/ {
      contain role::dbslave
    }

Everybody was happy and we had our list of 158 node classifications in Puppet.

## The downside of naming conventions

We never saw a good naming convention which was useful when it comes to growth in numbers of nodes or applications. Additionally admins struggled with node specific declarations and - even worse - node specific modules.

The naming convention makes it hard to migrate e.g. to cloud as you usually will not be able to re-use your naming convention on any cloud provider. Yes, you can set hostnames, yes, you can have your own DNS server in cloud. How to deal with autoscaling? How to deal with containers and how to deal with the next 25 new applications?
Consider rebuilding everything and you will learn, that the naming convention blocks you from doing so.

## Puppet and the certificate trust based node classification

From Puppet point of view the common name of the client certificate (which uses the fqdn if not configured to do otherwise) is only used to be a trust chain from your node to your Puppet master.

But you can add more data to your certificate, using x509v3 openssl extensions. Puppet even does this automatically for you!

    # /etc/puppetlabs/puppet/csr_attributes.yaml
    ---
    pp_role: 'dbmaster'
    pp_region: 'Berlin1'
    pp_zone: 'vlan127'

You only must take care that this information is added to the node **prior** it generates its Puppet certificate. An existing certificate will not be updated with the information.

Now we can move on to our one line node classification:

    # manifests/site.pp
    contain "role::${trusted['extension']['pp_role']}"

No more need to add all of your systems to your node classification.
Every new machine just needs the new role deployed to the Puppet master and immediately gets its classification.

Martin Alfke
