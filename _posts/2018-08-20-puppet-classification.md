---
layout: blog
title: Tip of the Week 86 - Puppet classification
---

One of the most important tasks we face when working with Puppet is **Classification**: the action of assigning classes to nodes, each class containing the resources we want to be applied to a system.

Classes are included in modules and may have parameters: setting parameter values to classes for different nodes is the other crucial Puppet activity, which is commonly done via Hiera.

Once we have defined what classes are included in what node and how they are parametrised, we have basically done most of our Puppet work.

Puppet nodes classification can be done in several different ways, let's review them.

### Node statement

This is the original and still usable, even if not too much popular in these days, method.

We can use the **[node](https://puppet.com/docs/puppet/5.5/lang_node_definitions.html)** statement in `manifests/site.pp` and other manifests in the main `manifests` directory of our control repo. With this approach, we identify each node by its certname and declare all the resources and classes we want for it, as shown in the following code:

     node 'web01.example.com' {
       include ::general
       include ::apache
     }

We can also use regular expressions, to group together different nodes, for example, all the nodes with name beginning with "web" can be grouped as follows:

    node /^web/ {
      include ::general
      include ::apache
    }

In the past it was possible to use inheritance to manage nodes and groups of nodes, but this no more supported as it could lead to scoping issues with variables, when used incorrectly.


### External Node Classifier

On an [External Node Classifier](https://puppet.com/docs/puppet/5.5/nodes_external.html) (ENC), we can define the classes (and parameters) that each node should have in a totally separated tool, which can be on a system other than the puppet server.

To configure Puppet to use an ENC, it's enough, on the puppet server to add lines like these to `puppet.conf`:

    [master]
      node_terminus = exec
      external_nodes = /usr/local/bin/enc

When configured to use an ENC with the `node_terminus = exec` option, Puppet runs the command specified via `external_nodes` and it passes as argument the client's certname.

The executed command can do anything with any language (query a web API, a Database, check file contents) and has to return a YAML output for the given certname with contents as follows:

    ---
      environment: production
      classes:
        - general:
        - apache:
      parameters:
        role: 'web'

Here are defined the classes to include for that node, the global parameters, which will be usable as top scope variables in Puppet code and the Puppet environment to use.

[The Foreman](https://www.theforeman.org), the Web Console of [Puppet Enterprise](https://puppet.com/products/puppet-enterprise), [Puppet Dashboard](https://github.com/sodabrew/puppet-dashboard) and other less popular products can all work as external nodes classifiers: here the selection of what classes have to be included in what nodes, or group of nodes, is done via the relevant Web interface.

Note however that an ENC can be of any kind, and doesn't involve the presence of a Web interface where to configure data for clients.

A ridiculously simple ENC script can be one that just makes a `cat` of a Yaml file with contents as the one shown before. Look [here](https://github.com/example42/psick/blob/production/bin/enc_cat.sh) for such an example, which uses files in [this directory](https://github.com/example42/psick/tree/production/bin/enc_cat).

### LDAP

Since the early days Puppet has the possibility to integrate with [LDAP](https://puppet.com/docs/puppet/5.5/nodes_ldap.html) and retrieve the lists of classes to from a LDAP have a hierarchical structure where a node can inherit the classes (referenced with the `puppetClass` attribute) set in a parent node (`parentNode`).

LDAP based classification is not common and is usually not even mentioned, but it's a viable alternative, especially where there is a robust LDAP infrastructure which users can access and manage with any kind of graphical user interface.

Configuration requires some settings on the Puppet server `puppet.conf` as follows:

    [master]
    node_terminus = ldap
    ldapserver = ldap.example.com
    ldapbase = ou=Hosts
    ldapuser = cn=admin,ou=users,dc=example,dc=com
    ldappassword = ldapuser_password

also we need to add Puppet's [schema](http://github.com/puppetlabs/puppet/blob/master/ext/ldap/puppet.schema) to the LDAP server and be sure to have, in our `manifests/site.pp` a default node statement like:

    node default {}

### hiera

We can specify the list of classes to include on a node via Hiera.

Originally there was the `hiera_include` function, typically added in `manifests/site.pp` as follows:

    hiera_include('classes').

This function looks for the 'classes' key in Hiera (could be any name), which is expected to contain an array of classes to merge across hiera's hierarchies and include in the relevant node.

The hiera_include, as all the other hiera_* functions, is not replaced by `lookup`, so the above line can be replaced by:

    lookup('classes',Array,'unique',[]).include

Which is a fancy and condensed way of writing:

    $classes = lookup('classes',Array,'unique',[])
    $classes.each | $class | {
      include $class
    }

Then, we define in our hierarchy under the key named classes, what to include for each node. For example, with a YAML backend, our case would be represented with the following lines of code:

    --- classes:
     - general
     - apache

### Nodeless Classification

In our main manifest `manifests/site.pp` we have the code that the Puppet master alwayes parses first when compiling a catalog. Here we can place anything: declarations of resources we want on ALL the nodes, nodes statements (as in the example before), resources defaults, definition of top scope variables and so any valid Puppet code.

Here we can also include classes without the need to use the node statement.

If we write here, outside any conditional logic, something like:

    include general

The `general` class (which, by convention, is expected to be defined in the file `manifests/init.pp` of a module called `general`) is included on all the nodes.

Here we can also include classes according to whatever logic we want, eventually using variables in the class names. So, for example if we have a fact (or a parameter set via an ENC) called `$role` we can implement the roles and profiles pattern just by adding something like:

    include "role::${::role}"

and have in a module called `role` different classes named according to the `$role` variable values we may have.


### PSICK module Classification

In example42 we like to explore new way of doing things with Puppet and refine our ideal approach to managing infrastructures with it.

The [psick module](https://github.com/example42/puppet-psick) has an unique approach to nodes classification based on Hiera data, featuring:

- Usage of hashes instead of arrays to more easily allow overrides and exceptions to the list of classes to include in each nodes

- Different Hiera keys to manage classes to include on different OS (so that you don't need to add OS specific layers in your environment's hiera.yaml)

- Different phases of Puppet application: an optional `firstrun` mode, where are defined what classes to include in the very first Puppet run, and three other phases, `pre`, `base` and `profiles` , classes defined for them are applied in that order (so typically in `pre` we include classes like proxy and repo settings which are a prerequisited for the others, in `base` the common classes we want on all the nodes (even if we can override them via Hiera) and in `profiles` the typical profile classes, as in the roles and profiles pattern).

In order to use Psick classification we need to add the `psick` class to our nodes (this is safe, by default, without relevant Hiera data in the `psick::` namespace, the class does nothing), so we can just write in our `manifests/site.pp`:

    include psick

Then we can use the psick module (which also provides a lot of profiles for common use cases) by setting Hiera data as follows, having different keys for Linux phases:

    psick::pre::linux_classes:
      puppet: ::puppet
      dns: psick::dns::resolver
      repo: psick::repo

    psick::base::linux_classes:
      sudo: psick::sudo
      time: psick::time
      ssh: psick::openssh::tp
      mail: psick::postfix::tp

    psick::profiles::linux_classes:
      webserver: apache

and Windows ones:

    psick::enable_firstrun: true
    psick::firstrun::windows_classes:
      hostname: psick::hostname
      aws_sdk: psick::aws::sdk    

    psick::pre::windows_classes:
      hosts: psick::hosts::resource

    psick::base::windows_classes:
      features: psick::windows::features
      registry: psick::windows::registry
      services: psick::windows::services
      time: psick::time
      users: psick::users::ad

    psick::profiles::windows_classes:
      webserver: iis

For each element of the above hashes, the element's key name is used as a tag to allow override via Hiera, and the value is the class name to include (in the above example most of these class names are profiles defined in the same psick module, but can be classes from any module with any name).

So for example, given the above data in `common.yaml` we can override to a specific node the name of the class to use to manage ssh with a node specific Hiera yaml file with a content like:

    psick::base::linux_classes:
      ssh: profile::ssh::bastion

On the relevant node the class used to configure ssh (note that we used the `ssh` key, but this could be called in any way, not necessarily referring to the actual function) will a custom class called `profile::ssh::bastion` from our local profile module instead of the common one from psick module `psick::openssh::tp`.

We can even decide to NOT manage ssh at all on a node (or group of nodes, according to where on Hiera we make the configuration) with an entry like:

    psick::base::linux_classes:
      ssh: ''

which overrides and nullifies the classes defined in more general Hiera layers.

You can read more about PSICK approach to classification on this [blog post](https://www.example42.com/2018/01/15/classification_and_first_run_mode_with_psick/)


### Roles and profiles

Strictly speaking the Roles and Profiles pattern is not a classification alternative, but a way to organise classes in a flexible and composable way.

In this case we just have to include a role class in a node, and this role class will itself include other classes (typically classes from a module called profile).

Classification of the role class itself can be done in different ways, as the ones mentioned before:

  - Via an **ENC** including the relevant role class for each of our nodes
  - On `manifests/site.pp`, including the role class inside the `node` statements
  - On `manifests/site.pp`, if we have a $role fact, with a single line like `include "role::${::role}"`
  - Even via the `psick` module, where we can reproduce the roles and profiles pattern by defining the profiles to include only on Hiera files defined in a hierarchy level which uses the $role variable (look [here](https://github.com/example42/psick-hieradata/tree/production/data/role) for some samples)


### Conclusion

Puppet seems complex. Puppet **is** complex.

Still once you understand a few key concepts everything becomes clearer and the dots start to be connected.

One of this key concepts is classification: how we decide what classes have to be included on what nodes.

We hope that after this reading you have a better and clearer idea on how you can manage classification in Puppet, and what approach better fits your use case. 


Alessandro Franceschi
