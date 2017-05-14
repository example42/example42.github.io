---
layout: blog
title: Tip of the Week 20 - Self contained nodes classifications
---

Every Puppeteer quite soon in his career has to cope with nodes classification.

The inevitable, necessary and useful task of defining which classes to include in which nodes.

In Puppet we can do this with various alternatives, which can often coexist.

Some of them are based on data or code we have in our control-repo:

  - Using the node statement in our ```manifests``` directory files. For each node, eventually matched by RegExps, we can include classes grouped as needed.
   
  - Including, conditionally, classes in the main ```manifests``` directory based on top scope variables which may come from facts, variables from an ENC, be defined in the same main manifests.

  - Defining in Hiera the classes to include for each node, according the local hierarchy. If using local files, data may be in the ```hieradata``` or ```data``` directories of our control repo.

Others rely on external data sources:

  - Using an External Node Classifier (ENC) such as the console of Puppet Enterprise or The Foreman, or any other which, queried with the node certname, returns a yaml as described [in a previous tip](2017-04-10-environment-enforcement.md).

  - Using LDAP, querying an external LDAP server for the classes to include in a node (Puppet schema is provided)

  - Using Hiera to classify nodes with an external datastore backend.

We define **self contained** a control repo which has all the code and the data needed and necessary to manage our infrastructure: Hiera data, Puppet code in manifests and local modules, list of external modules in Puppetfile and eventually provisioning scripts for different environments such as Vagrant, AWS, Docker.

My current own personal preference on how to classify nodes is, more or less, in [PSICK](https://github.com/example42/psick), example42's opinionated, customizable, control repo which by default includes in ```manifests/site.pp``` a ```profile::pre``` and ```profile::base``` class, which are just class containers for other classes to manage, respectively, the resources we want to apply before all the others (package repos, network configs...) and the ones which we want to apply to all our nodes (the common baselines of configurations).

On PSICK is possible to customize, via Hiera, the actual classes to include for each component managed in prerequisites and baselines.

Hiera is used also to define the classes (profiles) to add for each node according to how different they are.

This approach is equivalent to the roles and profiles pattern but instead of defining and declaring role classes, the list of profiles to include is retrieved via Hiera, using the modern equivante to the good old ```hiera_include```:

    lookup('profiles', Array[String], 'unique', [] ).contain

Probably it's easier to give a look at the [```site.pp```](http://github.com/example42/psick/blob/production/manifests/site.pp) to get an idea.

This approach makes it easy to test similar environments during development, testing and CI. It's also entirely data driven: we can configure the whole infrastructure in Hiera Yaml files, both the classes to include in each node and how they are parametrized.

Worth underlining is that all this still relies on some kind of external data source: the facts or the variables derived from the node name. I currently tend to use **trusted facts** to set such variables during systems provisioning.

Also, it's important to understand that such an approach may, and in some cases has, to adapt to local needs and software, such as installations based on Puppet Enterprise or The Foreman where we can use a web interface to classify nodes.

What information has to stay on Hiera, and what on the ENC, depends on single cases, as long as it's clear, and logic, what is responsible for what, the two worlds can exist.

In PE based setups, for example I still prefer to define classification as Hiera Yaml data, and use PE Node manager just to manage the Puppet infrastructure itself (as done by itself), and eventually to create custom local groups, where may be defined top scope variables used in the control repo code and data.

As usual, your mileage may vary.

Alessandro Franceschi
