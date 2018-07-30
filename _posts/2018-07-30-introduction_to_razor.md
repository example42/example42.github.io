---
layout: blog
title: Tip of the Week 83 - Introduction to Razor
---

This is the first of a series of posts about [Razor](https://github.com/puppetlabs/razor-server), an Open Source systems provisioning tool developed by [Puppet](https://puppet.com).

Razor automates the installation of the most common Operating Systems on bare metal servers or virtual machines, as long as they can perform a network boot via [iPXE](https://ipxe.org/).

Nodes to be provisioned need to have network boot enabled and be connected to a network where a DHCP server is configured with a valid Boot server a Bootfile name.

This must be a reachable a tftp server configured to serve via network a Razor **micro kernel** (a minimal Linux distro) which uses **Facter** to collect data (facts) about the system to be provisioned and interacts with the Razor server to manage how provisioning has to be performed.

**Razor server** is a ruby application that works on RedHat and derivatives 6 and 7, it uses PostgreSQL for data persistence and HTTP(S) for APIs and client-server traffic. It can run on nodes different from the Puppet Master, the DHCP and the tftpserver.

When using Puppet Enterprise to install the Razor server it's enough to include the **pe_razor** Puppet module, which is already shipped with PE.

The FOSS version can be installed by [lavaburn-razor](https://forge.puppet.com/Lavaburn/razor) module.

Alternatively the `razor-server` package can be installed from the official Puppet repos.

In its configuration file, `/etc/puppetlabs/razor-server/config-defaults.yaml`, we can manage database endpoints, authentication methods and how Razor behaves with newly discovered hosts (by default, now, they are considered installed, to avoid unwanted re-provisioning of existing systems)

Razor uses port 8150 for HTTP communication between the server and nodes (traffic should be open to server's port 8150 from any host to be provisioned) and port 8151 for HTTPS, used for accessing the public API (server's port must be reachable from any system where the Razor client is used).

The razor client is a Ruby gem (`gem install razor-client`) which provides a command-line tool (`razor`), that interacts with Razor server's APIs (by default using the URL `http://razor:8150/api`, can be changed by the `--url` option or by setting the `RAZOR_API` environment variable).

To setup provisioning via Razor we need in our Infrastructure:

- **Nodes** to be provisioned (either VMs or Physical servers) able and configured to boot via network
- A **DHCP server** configured to provision clients using a kernel image loaded via network (next-server and filename option on ISC DHCPd)
- A **tftp server** with Razor's microkernel
- A **Razor server** installed and configured to access a PostgreSQL DB
- A minimal **configuration** of Razor resources (repos, brokers, tags, policies, tasks...)

Each node is identified by its Mac address, by default, and once it boots Razor's microkernel image, it is registered with most of its facts.

According to the node's facts, we can **tag** systems, matching any condition we need.

We can then create a **policy** which correlate tags to the other basic Razor provisioning elements.

Policies are rules that tell Razor what to do with a node and how it has to be provisioned: **repos** to use, **tasks** (commands, snippets of preseed / kickstart configs...) to include, and **brokers** (post-installation integrations) to activate, like the one that installs Puppet on the provisioned node.

We will review in future posts how to configure the various server components and how to configure Razor elements. Here is a quick preview of the minimal essentials.

First we can give a look around and show current Razor server configs:

    razor config

Then we can see if there are predefined elements (there should be at least some tasks):

    razor tasks

More generally we can specify any valid element type and eventually its name:

    razor <tags|brokers|hooks|nodes|policies|repos|tasks> [element_name]

A minimal configuration requires setting a tag for one or more nodes, accoridng to the matching rules (based on facts) we want. So, for example, strictly matching a node with its MAC:

    razor create-tag --name my_node --rule '["in", ["fact", "macaddress"], "00:0c:21:21:11:43"]'

Then we have to add at least a repo of an ISO of a OS to provision. Here we get the CentOS7 iso and associate it to the pre-existing centos/7 task:

    razor create-repo --name centos7-1804 --iso-url http://www.mirrorservice.org/sites/mirror.centos.org/7/isos/x86_64/CentOS-7-x86_64-DVD-1804.iso --task centos/7

We create a broker, a post installation activity, that is intended to hand over the provisioned system to a configuration management tool. Available broker types are: noop, puppet, puppet-pe, chef.

    razor create-broker --name mypuppet -c server=puppet.example.com -c environment=production --broker-type puppet

We can finally create a policy, that applies the given provisioning tasks, repos and broker to the nodes that match the specified tags:

    razor create-policy --name centos7 \
    --repo centos7-1804 --task centos/7 --broker mypuppet \
    --enabled --hostname 'host${id}.example.com' \
    --root-password my_root_password --max-count 20 \
    --tag my_node

We can review the commands given with:

    razor commands

This has been just a gentle introduction to Razor, with a glimpse of the commands needed for basic minima configuration, in the next posts we will see more details on how to setup an use a Razor based provisioning infrastructure.

Alessandro Franceschi
