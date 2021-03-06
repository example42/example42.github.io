---
layout: blog
title: Tip of the Week 39 - Secure data management with multiple eyaml keys
---

With improved security implementations it is often required that keys must be separate among different infrastructure stages.
This means that we have to deal with multiple eyaml keys for production-stage and ci- and development-stage.

Nobody may have the private production key. Everybody should have access to the production public key (which is used for encryption).
All other keys can be made available to everybody.

First let's set some top scope variable by analysing facts:

    # Set top scope variables
    # eyaml key selection based on existence of an external fact:
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
          pkcs7_public_key: "/etc/puppetlabs/code/environments/%{::environment}/eyaml/keys/public_key.pkcs7_%{::eyaml_selector}.pem"


This will lead to a quite complex hierarchy, with the benefit of separating encryptions done with different keys.

All *_secrets_production.yaml files contain secrets encrypted with the production key.
All *_secrets_development.yaml files contain secrets encrypted with the development key.

On the other hand it is easy to find missing encrypted production keys by comparing the hiera data keys in both yaml files.

Martin Alfke
