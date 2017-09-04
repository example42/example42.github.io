---
layout: blog
title: Tip of the Week 36 - Testing any role on any OS with a PSICK control repo
---

Short version of the post:

    cd vagrant/environment/ostest
    ln -sf hieradata/role/${::role}.yaml hieradata/role/ostest.yaml
    vagrant up [vm]

Long version of the post: PSICK explained, again :-)

PSICK is the Puppet control repo of reference we use in example42 to bootstrap new projects and to test new modules and design patterns.

It contains the evolving synthesis of our best practices and 10 years of Puppet experience, so it's full of stuff, from tools to help with Puppet development, to CI for testing Puppet deployments, from a rich set of opinionated profiles to a solid and flexible classification approach.

It's intended to be forked, morphed, adapted and customised, or cherry picked.

It's a ongoing forge of ideas and solutions, and even if every part of it can be adapted or modified according to any need, there's is a design approach that defines PSICK: it is **self contained** and entirely **data driven**.

It has all, by default, we need to manage and provision an infrastructure with Puppet.

## Entirely Hiera driven

PSICK, for the user perspective, can be entirely Hiera driven, based on hierarchies containing concepts like roles, operational environments (envs, tiers) and zones (datacenters).

The default ```hiera.yaml``` looks like:

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

Names, layers and logic may differ, as the same way we assign these variables.

The basic principle should be: In our environment/control-repo ```hiera.yaml``` we use hierarchies which reflect and map how our configurations change in the nodes of our infrastructure.

We don't generally care about changes in Operating Systems (data in profiles and modules care of them), we focus on our infrastructure, and how data can adapt to it.

## Setting top scope variables used in hierarchy

We may set the top scope variables used in hierarchy paths in different ways:

  - As trusted facts defined during server provisioning, before Puppet's first run
  - As external facts set during provisioning
  - As normal facts pluginsynced from our site modules
  - As global variables set via an ENC (Puppet Enterprise, Foreman)
  - Directly in the main manifest, in the top scope, outside any class

PSICK's default expects the variables used in the hierarchy as trusted or normal facts, this implemented in ```manifest/site.pp```, where everything happens, with something like:

    if $trusted['extensions']['pp_role'] {
      $role = $trusted['extensions']['pp_role']
    }

To give the idea, [these](https://github.com/example42/psick/blob/production/bin/ec2_userdata/) are sample user-data files to set such trusted facts on ec2 instances.

## Nodes classification

By default, in the main manifest we manage also nodes classification, as follows.

First, we include, in all the nodes, a settings profile, used only as entry point for (Hiera driven) variables shared across profiles.

    contain '::profile::settings'

Variables like $::profile::settings::proxy_server may be used by different profiles and this should be the default value for their own proxy settings.

Then we include a prerequisites class, which provides the prerequisites resources we want to to evalutate first (typically package repositories and proxy settings)

    contain '::profile::pre'

Finally a general baseline class is included, distinct for each OS kernel:

    $kernel_down=downcase($::kernel)
    contain "::profile::base::${kernel_down}"

Every group of resources managed by the pre and base profiles is declared inside a class, using a class name exposed as a parameter, manageable via Hiera:

    class profile::base::linux (
      # General switch. If false nothing is done.
      # Set to false to skip base classes management.
      Boolean $manage         = true,
      String $network_class = '',
      String $mail_class    = '',
      String $puppet_class  = '',
      [...]
      ) {
       if $network_class != '' and $manage {
         contain $network_class
         }
      [...]
     }


So we can set, in ```common.yaml``` or anywhere in the hierarchy, params like the following to fine tune what common classes, local profiles or directly public module we want:

    profile::base::linux::mail_class: '::profile::mail::postfix'
    profile::base::linux::puppet_class: '::puppet'
    profile::base::linux::ssh_class: '::profile::ssh::openssh'
    profile::base::linux::users_class: '::profile::users::static'
    profile::base::linux::sudo_class: '::profile::sudo'
    profile::base::linux::monitor_class: '::profile::monitor'
    [...]

For windows, many resources are different and it makes sense to manage them in a separated base profile:

    profile::base::windows::puppet_class: ''
    profile::base::windows::features_class: '::profile::windows::features'
    profile::base::windows::registry_class: '::profile::windows::registry'
    profile::base::windows::network_class: ''


Additional profile classes, which are specific for [group of] nodes, are looked via Hiera (using the ```profiles``` key) and included:

    lookup('profiles', Array[String], 'unique', [] ).contain

We also ensure they are applied after all the base profiles.

    lookup('profiles', Array[String], 'unique', [] ).each | $p | {
      Class["::profile::base::${kernel_down}"] -> Class[$p]
    }

## No roles (classes)

There are no role classes, they function is replaced by the profiles included via hiera: we can reproduce the tipical roles and profiles pattern by defining under ```hieradata/role/$::role.yaml``` something like:

    ---
      profiles:
        - profile::git
        - profile::puppet::gems
        - profile::ci::octocatalog
        - profile::ci::danger
        - profile::gitlab::runner
        - profile::gitlab::ci
        - docker

This would be the same of having a class like ```site/role/manifests/cirunner.pp``` with:

    class role::cirunner {
      include profile::git
      include profile::puppet::gems
      include profile::ci::octocatalog
      include profile::ci::danger
      include profile::gitlab::runner
      include profile::gitlab::ci
      include docker
    }

But here we have the flexibility of Hiera and the possibility to manage exceptions, or add new roles, just working with yaml files.


## Vagrant to test multiple OS

PSICK includes several Vagrant multi VM environments that can be used to test the code and the data of the control repo itself.

We have made them easily configurable (check the [Vagrant docs](https://github.com/example42/psick/blob/production/docs/vagrant.md) for details) by editing a single ```config.yaml``` where it's possible to test role, operating systems both in Puppet agent and apply mode.

We have a vagrant environment called ostest, when we can test our control repo on the following machines:

    al@lab psick [development] $ cd vagrant/environments/ostest/
    al@lab ostest [development] $ vagrant status
    Current machine states:

    centos7.ostest.psick.io             running (virtualbox)
    centos6.ostest.psick.io             not created (virtualbox)
    ubuntu1604.ostest.psick.io          poweroff (virtualbox)
    ubuntu1404.ostest.psick.io          not created (virtualbox)
    ubuntu1204.ostest.psick.io          not created (virtualbox)
    debian9.ostest.psick.io             poweroff (virtualbox)
    debian8.ostest.psick.io             not created (virtualbox)
    debian7.ostest.psick.io             not created (virtualbox)
    suse12.ostest.psick.io              not created (virtualbox)
    suse11.ostest.psick.io              not created (virtualbox)
    opensuse-tumbleweed.ostest.psick.io not created (virtualbox)
    opensuse-42-1.ostest.psick.io       not created (virtualbox)
    alpine3.ostest.psick.io             not created (virtualbox)
    fedora23.ostest.psick.io            not created (virtualbox)
    cumulus.ostest.psick.io             not created (virtualbox)
    windows2012-ostest                  not created (virtualbox)
    windows2008-ostest                  not created (virtualbox)

Yes also Windows, yes it works.

These VMs are configured as follows in ```vagrant/environments/ostest/config.yaml```, note how we set ex external fact ```$::role``` to ```**ostest**```.

    ---
    # Default settings for all vms (they can be overridden on each node)
    vm:
      memory: 1024                 # MB or RAM to assign
      cpu: 1                       # Number of vCPU to assign to the VM
      role: ostest                 # Default role
      box: centos7                 # Box used for the VM, from the box list in vagrant/boxes.yaml
      puppet_apply: true           # Run puppet apply on the local control-repo during provisioning
      puppet_agent: false          # Run puppet agent during provisioning
      facter_external_facts: true  # Create external facts in facts.d/$fact.txt. Note 1
      facter_trusted_facts: false  # Create csr_attributes.yaml. Note 1

    # A local network is created among the VM. Here is configured.
    network:
      range: 10.42.45.0/24        # Network address and mask to use
      ip_start_offset: 101        # Starting ip in the network for automatic assignement
      domain: ostest.psick.io     # Name of DNS domain for the created machines

    # Puppet related settings
    puppet:
      version: latest             # Version to use for OSS
      install_oss: true           # If to install Puppet OSS agent on the VMS
      install_pe: false           # If to install Puppet Enterprise agent on the VMS
      env: devel                  # Setting for the env fact (may be used in hiera.yaml)
      zone: ostest                # Setting for the zone fact (may be used in hiera.yaml)
      datacenter: vagrant         # Setting for the datacenter fact (may be used in hiera.yaml)
      application: puppet         # Setting for the application fact (may be used in hiera.yaml)
      master_vm:  foreman.fab.psick.io    # Name of the VM which play as Puppet server for the others
      master_fqdn: 'foreman.fab.psick.io' # FQDN of the Puppet server to use with puppet agent
      link_controlrepo: true      # Add a link for a Puppet environment to the development control-repo
      environment: host           # Puppet environment to link to local control-repo

    # Nodes shown in vagrant status
    nodes:
      - hostname_base: centos7
        box: centos7
      - hostname_base: centos6
        box: centos6
      - hostname_base: ubuntu1604
        box: ubuntu1604
      [...]

Now we actually have a [sample](https://github.com/example42/psick/blob/production/hieradata/role/ostest.yaml.sample) ```hieradata/role/ostest.yaml``` but we can, better, use a symlink instead, pointing to the actual role we want to test without the need to write any extra code.

    cd vagrant/environment/ostest
    ln -sf hieradata/role/${::role}.yaml hieradata/role/ostest.yaml
    vagrant up [vm]

Alessandro Franceschi
