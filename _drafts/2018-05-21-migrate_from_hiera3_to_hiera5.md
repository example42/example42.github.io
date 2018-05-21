---
layout: blog
title: Tip of the Week 73 - Migrate from Hiera v3 to Hiera v5
---

Hiera is the Puppet concept of seaprating code from data. This concept allows you to describe your infrastructure in code and to let you put differences amongts your platform into the data source.

With Pupept 4.9 Hiera config version 5 was introduced.
The new Hiera version allows you to place data globally, in environments and modules.

As of Puppet 4.9.2 Hiera has the following backends pre installed:
- yaml
- json
- eyaml (hiera-eyaml gem still required)

This posting describes how to migrate from Hiera config version 3 to the new usage.

* Table of content
{:toc}

## Location of Hiera configuration file and data

With new version of Hiera you can have three different location for data:

Global Hiera data are the same as they have been with the older Hiera version.
Data in modules are a replacement for params pattern and inheritance.
Data in environments allow you to stage data and hiera config changes.

Global Hiera uses a global configuration file which must be placed in the Puppet configuration directory (usually `/etc/puppetlabs/puppet/hiera.yaml`).

If you keep this configuration file in place, the provided Hiera data will have highest priority!
**Don't forget to remove the global Hiera config file, once the migration has been finished.**

The location of the global data is either in a separate directory (e.g. `/etc/puppetlabs/hieradata`) or already within your environments ( `/etc/puppetlabs/code/environments/${environment}/hieradata`).

Consider migrating from a global path to an environment path prior migrating to new Hiera.

Next layer is environment data. The required Hiera configuration file is within each environment (e.g. `/etc/puppetlabs/puppet/code/environments/production/hiera.yaml`).
Usually data are also placed within the environment in a `data` directory.

On module level it is also possible to have a hiera configuration file at module root (e.g. `/etc/puppetlabs/code/environments/production/modules/ntp/hiera.yaml`).
This layer is usually only used by module authors and you are encouraged to overwrite the provided data within your environment data.

## Content of Hiera configuration file

In older hiera configuration files backends and hierarchies were seaparated settings. First you provided an array of used backends and then you listed the hierarchies. Backends were searched in order of occurence in the configuration file.

The new hiera config allows you to specify backends globally (as default) or on a per hierarchy level.

Let's assume the following existing Hiera config v3 file:

    # Hiera config v3
    :backends:
      - eyaml
      - yaml
    :yaml:
      :datadir: "/etc/puppetlabs/code/environments/%{environment}/hieradata"
    :eyaml:
      :datadir: "/etc/puppetlabs/code/environments/%{environment}/hieradata"
      :pkcs7_private_key: /etc/puppetlabs/puppet/eyaml/private_key.pkcs7.pem
      :pkcs7_public_key:  /etc/puppetlabs/puppet/eyaml/public_key.pkcs7.pem
    :hierarchy:
      - "nodes/%{trusted.certname}"
      - "location/%{facts.whereami}/%{facts.group}"
      - "groups/%{facts.group}"
      - "os/%{facts.os.family}"
      - "common"
    :logger: console
    :merge_behavior: native
    :deep_merge_options: {}

With hiera config v5 the `:logger:`, `:merge_behavior:` and `:deep_merge_options:` settings are no longer used and can be removed.

    # Hiera config v5
    version: 5
    defaults:
      datadir: data
      data_hash: yaml_data
    hierarchy:
      - name: "Per-node data (yaml version)"
        path: "nodes/%{trusted.certname}.yaml" # Add file extension
        # Omitting datadir and data_hash to use defaults.

      - name: "Per-group secrets"
        path: "groups/%{facts.group}.eyaml"
        lookup_key: eyaml_lookup_key
        options:
          pkcs7_private_key: /etc/puppetlabs/puppet/eyaml/private_key.pkcs7.pem
          pkcs7_public_key:  /etc/puppetlabs/puppet/eyaml/public_key.pkcs7.pem

      - name: "Other YAML hierarchy levels"
        paths: # Can specify an array of paths instead of a single one.
          - "location/%{facts.whereami}/%{facts.group}.yaml"
          - "groups/%{facts.group}.yaml"
          - "os/%{facts.os.family}.yaml"
          - "common.yaml"

Ayou can see it is now possible to group hierarchies which use the same backend.
In this special case it is also possible to completely remove the `yaml` backend and simplify the configuration file:

    # Hiera config v5 - eyaml only
    version: 5
    defaults:
      datadir: data
      lookup_key: eyaml_lookup_key
        options:
          pkcs7_private_key: /etc/puppetlabs/puppet/eyaml/private_key.pkcs7.pem
          pkcs7_public_key:  /etc/puppetlabs/puppet/eyaml/public_key.pkcs7.pem
    hierarchy:
      - name: "All hierarchies"
        paths:
          - "nodes/%{trusted.certname}.yaml" # Add file extension
          - "location/%{facts.whereami}/%{facts.group}.yaml"
          - "groups/%{facts.group}.yaml"
          - "os/%{facts.os.family}.yaml"
          - "common.yaml"

## Migrating from hiera*() to lookup() function

The new `lookup` function provides a huge amount of possible usages. The most impressing one is that the function will query hiera for lookup and merge options prior doing the real lookup on a key.

| lookup type | hiera v3 | hiera v5 with merge options hash| hiera v5 with Data type, default and merge option|
|---|---|---|---|
|single | hiera('key')|lookup('key')|lookup('key', DataType) |
|array| hiera_array('array')|lookup('array', {merge => unique})| lookup('array', Array, [], unique)
hash - first found values| hiera_hash('hash')|lookup('hash', {merge => hash})|lookup('hash', Hash, {}, hash)|
hash - merge values| hiera_hash('hash')| lookup('hash', {merge => deep})|lookup('hash', Hash, {}, deep)|
|include|hiera_include('classes')|lookup('classes', {merge => unique}).include|lookup('classes', Array, [], unique).include

If you have more complex decisions on when to do deep lookups, you have the option to place the lookup behavior into your hiera data:

    lookup_options:
      'keyname':
        merge: 'merge_option'

e.g.

    lookup_options:
      ntp::servers:
        merge: 'unique'

Then you can always use the simple `lookup` function to query data.

## How to upgrade when using another data backend

Hiera has changed the way how lookup backends are working. The old hiera 3 backends like mongodb and file are no longer working on hiera v5 in environment level. It is possible to use them on global level and specify the backend to use:

    # Only working on global hiera level
    - name: "Per-node data (MongoDB version)"
      path: "nodes/%{trusted.certname}"      # No file extension
      hiera3_backend: mongodb
        options:    # Use old backend-specific options, changing keys to plain strings
         connections:
           dbname: hdata
           collection: config
           host: localhost 

If you don't want to use the global hiera level anymore, you must use hiera v5 style lookup functions. Ask the authors whether he is able to provide you with a new function.

For file backend there is a [solution posted at the GitHub issue](https://github.com/voxpupuli/hiera-file/issues/23#issuecomment-384388992). Many thanks to [Igor Galic](https://github.com/igalic) for the solution.

Happy hacking,
Martin Alfke
