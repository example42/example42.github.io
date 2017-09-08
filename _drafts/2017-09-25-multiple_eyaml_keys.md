---
layout: blog
title: Tip of the Week 39 - Secure data anagement with multiple eyaml keys
---

With improved security implementations it is often required that SSl keys must be seaprate among different infrastructure stages.
This means that we have to deal with multiple eyaml keys for production stage, integration stage, ci stage and development stage.

Nobody may have the private production key. Everybody should have access to the productoin public key (which is used for encryption).
All other keys can be made available to everybody.

First let's set some top scope variable by analyzing facts:

    # Set top scope variables
    # eyaml key selection based on existance of an external fact:
    #  'eyaml_private_base_path'
    # when fact is set, then we run on spec tests keys
    # otherwise we use production keys
    if has_key($::facts, 'eyaml_private_base_path') {
      $eyaml_selector = 'development'
    } else {
      $eyaml_private_base_path = '/etc/puppetlabs/puppet/eyaml'
      $eyaml_selector = 'production'
    }

Now let's adopt our hiera yaml:

    ---
    version: 5
    defaults:
      datadir: data

    hierarchy:
      - name: "Data"
        lookup_key: eyaml_lookup_key
        paths:
          - "hosts/%{::trusted.certname}.yaml"
          - "hosts/%{::trusted.certname}_secrets_%{::eyaml_selector}.yaml"
          - "role/%{::role}/%{::env}.yaml"
          - "role/%{::role}/%{::env}_secrets_%{::eyaml_selector}.yaml"
          - "role/%{::role}.yaml"
          - "role/%{::role}_secrets_%{::eyaml_selector}.yaml"
          - "zone/%{::zone}.yaml"
          - "zone/%{::zone}_secrets_%{::eyaml_selector}.yaml"
          - "common_secrets_%{::eyaml_selector}.yaml"
          - common.yaml
        options:
          pkcs7_private_key: "%{::eyaml_private_base_path}/private_key.pkcs7_%{::eyaml_selector}.pem"
          pkcs7_public_key: "eyaml/keys/public_key.pkcs7_%{::eyaml_selector}.pem"



Martin Alfke
