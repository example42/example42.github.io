---
layout: blog
title: Tip of the Week 40 - Tenant modules
---

The Puppet code and data we use to shape and configure our infrastructures often need to be managed by different people, sometimes belonging to different groups. Some of them may have good Puppet skills, some not and just need configurations done in the way they need.

A common scenario is where there are different teams managing the basic systems' configurations and applications: the first group may be the one which introduced Puppet and has most of the knowledge about it, the second one need to use existing code and eventually write custom one, and feed the data to configure their managed applications. In other cases different groups responsible for different applications may need to manage them independently.

A single control-repo with or without extra internal modules added to the ```Puppetfile``` may serve the purpose, but it has some drawbacks: changes needed by an applications team have to be done on a repository which manages the whole infrastructure, containing systems which they are not responsible for.

There may be different approaches to this, which can involve a strict overview and change process on the control-repo, but probably the most flexible and frictionless one is by using **tenant modules**.

A tenant module is contained in a git repository under the responsibility of a team and it can manage an application or a part of the Puppet managed infrastructure without interfering with the global infrastructure, managed by the operations team handling the control-repo.

It has the structure of a normal module, with its one classes, defines, templates and eventually data in module, but compared to a a normal module it has also a local directory which is added to the environment Hiera's hierarchy.

A Hiera 5 environment hiera.yaml using a tenant module and a fact or top scope variable identifying the tenant name, may look like:

    ---
    version: 5

    defaults:
      datadir: data

    hierarchy:
      - name: "Master control repo hierarchy node specific"
        lookup_key: eyaml_lookup_key # eyaml backend
        paths:
          - "nodes/%{trusted.certname}.yaml"
        options:
          pkcs7_private_key: /etc/puppetlabs/puppet/keys/private_key.pkcs7.pem
          pkcs7_public_key:  /etc/puppetlabs/puppet/keys/public_key.pkcs7.pem

      - name: "tenant module hierarchy certname"
        lookup_key: eyaml_lookup_key # eyaml backend
        paths:
          - "../modules/%{::tenant}/hieradata/nodes/%{trusted.certname}.yaml"
        options:
          pkcs7_private_key: "/etc/puppetlabs/puppet/keys_%{::tenant}/private_key.pkcs7.pem"
          pkcs7_public_key:  "/etc/puppetlabs/puppet/keys_%{::tenant}/public_key.pkcs7.pem"

      - name: "tenant module hierarchy common"
        lookup_key: eyaml_lookup_key # eyaml backend
        paths:
          - "../modules/%{::tenant}/hieradata/common.yaml"
        options:
          pkcs7_private_key: "/etc/puppetlabs/puppet/keys_%{::tenant}/private_key.pkcs7.pem"
          pkcs7_public_key:  "/etc/puppetlabs/puppet/keys_%{::tenant}/public_key.pkcs7.pem"

      - name: "Master control repo hierarchy"
        lookup_key: eyaml_lookup_key # eyaml backend
        paths:
          - "env/%{::env}.yaml"
          - "common.yaml"
        options:
          pkcs7_private_key: /etc/puppetlabs/puppet/keys/private_key.pkcs7.pem
          pkcs7_public_key:  /etc/puppetlabs/puppet/keys/public_key.pkcs7.pem


this means that inside the ```$::tenant``` module, under its ```hieradata``` directory it's possible to set parameters that affect a node, without the need to change anything on the control-repo and it's also possible to specify custom paths for the Hiera eyaml keys, so that each group can manage its passwords securely and independently.

Hierarchies may vary, other layers may be added and extra precautions may be taken in order to avoid a team affecting nodes managed by other teams.

Plus point anyway is that a group can place its data, templates, and eventually also custom classes, in a module which is managed independently.

In order to avoid the need to update the ```Puppetfile``` in the control-repo when a change is done on a tenant module, the special option ```:branch => :control_branch``` can be added for the tenant module:

    mod 'team_one',
      :git    => 'git@git.example.com:organization/team_one.git',
      :branch => :control_branch

This syncs the branch used in the control-repo with the one of the module, so, for example, when control-repo's production branch is deployed in Puppet's production environment, also the production branch of the tenant module is deployed.
If we configure both on the control-repo and on the tenant module, Puppet Enterprise's Code Manager or another r10k webhook to automatically deploy code as soon as a change is done in the relevant git branch, we can automate code deployment of the tenant module and give the relevant group full control of their systems, without the need of support or manual intervention from the group than manages the control-repo.

Variations on the theme are possible, yet the principle is the same: by allowing different groups to manage their own git repositories, and placing there tenant modules which are used to manage custom files and manifests AND also affect the Hiera data, we can delegate responsibilities in a safe and frictionless way.

Alessandro Franceschi
