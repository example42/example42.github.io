---
layout: blog
title: Tip of the Week 31 - Request for Feedback - sort_merged_arrays fix and problems with older Puppet versions
---

With Puppet 4.10.5 and 5.0.2 a fix for a missing functionality was released: [sort_merged_arrays lookup option](https://docs.puppet.com/puppet/5.0/hiera_merging.html#deep).

In earlier versions of Puppet this was named 'sort_merge_arrays' but lacked the functionality.

Unluckily Puppet did not build the fix with backward compatibility.

When using 'sort_merge_arrays' the following will happen:

- Puppet 4.10.4/5.0.1 or earlier: success - but no functionality
- Puppet 4.10.5/5.0.2 or later: compiler failure

When using 'sort_merged_arrays' the following will happen:

- Puppet 4.10.4/5.0.1 or earlier: compiler failure
- Puppet 4.10.5/5.0.2 or later: success - with functionality

How to work around this version dependent functionality when providing code for multiple Puppet versions?

We have a [pull request](https://github.com/example42/psick/pull/133) on GitHub with a really ugly hack:

1. identify version of Puppet and set a variable
1. use this variable as a hierarchy in hiera.yaml
1. add new hierarchy with corrected spelling of sort_merged_arrays

Let's look at details:

manifests/site.pp

    # Puppet 4.10.4 and older had a typo in sort_merged_array lookup option
    # to allow functinonality we add a new hierarchy to profile hiera.yaml where we use the wrong name
    if versioncmp('4.10.4', $facts['puppetversion']) >= 0 {
      $fix_sort_merge = '4'
    } else {
      $fix_sort_merge = undef
    }

site/profile/hiera.yaml

    ---
    version: 5

    defaults:
      datadir: data
      data_hash: yaml_data

    hierarchy:
      - name: "In module hierarchy"
        paths:
          - "%{facts.virtual}.yaml"
          - "%{facts.os.name}-%{facts.os.release.major}.yaml"
          - "%{facts.os.name}.yaml"
          - "%{facts.os.family}-%{facts.os.release.major}.yaml"
          - "%{facts.os.family}.yaml"
          - "common%{fix_sort_merge}.yaml"
          - "common.yaml"

site/profile/data/common.yaml

    lookup_options:
      "^profile::(.*)::(.*)_hash$":
        merge:
          strategy: deep
          knockout_prefix: "--"
          sort_merged_arrays: true
      "^profile::(.*)::(.*)::(.*)_hash$":
        merge:
          strategy: deep
          knockout_prefix: "--"
          sort_merged_arrays: true
      "^profile::(.*)::(.*)_list$":
        merge:
          strategy: deep
          knockout_prefix: "--"
          sort_merged_arrays: true
      "^profile::(.*)::(.*)::(.*)_list$":
        merge:
          strategy: deep
          knockout_prefix: "--"
          sort_merged_arrays: true

site/profile/common4.yaml

    ---
    lookup_options:
      "^profile::(.*)::(.*)_hash$":
        merge:
          strategy: deep
          knockout_prefix: "--"
          sort_merge_arrays: true
      "^profile::(.*)::(.*)::(.*)_hash$":
        merge:
          strategy: deep
          knockout_prefix: "--"
          sort_merge_arrays: true
      "^profile::(.*)::(.*)_list$":
        merge:
          strategy: deep
          knockout_prefix: "--"
          sort_merge_arrays: true
      "^profile::(.*)::(.*)::(.*)_list$":
        merge:
          strategy: deep
          knockout_prefix: "--"
          sort_merge_arrays: true

All this is already part of a PR for [PSICK](https://github.com/example42/psick).

We are interested to learn about any other - less ugly - solution.

We wish successful unit and integration tests on your control-repositories.

Martin Alfke
