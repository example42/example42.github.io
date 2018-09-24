---
layout: blog
title: Tip of the Week 91 - The FIVE things you need to know when starting with Puppet
---

Let's say you know nothing about Puppet.
Or maybe you already know something about it and have started to use it, but still don't have a firm grasp on its components or a clear understanding of the whole picture.

Eventually someone has started to introduce it in your company and you have to deal with it.

You might belong to one or more of these category of Puppet users:
- **End user**, dealing only with (Hiera) Data based on given instructions
- **Power user** comfortable with using public or internal modules and eventually write custom classes (such as profiles)
- **Modules developer**, writing modules and profiles intended for local or public use
- **Admin**, who maintains the Puppet server infrastructure
- **Architect**, who designs the data structure, the code organisation, the classification approach

Bad news is that more you belong to the latter categories, more things you need to know, and their amount is not negligible.

Good news is that you don't need to know everything, in order to successfully use Puppet.

Here is a list, with useful links, of the things to know, according to who you are and what you want to be, in Puppet terms.


## Terms, command and components

Basic knowledge of Puppet ecosystem is essential for architects, admins and developers, and useful, even if not strictly necessary, for end users:

- Puppet [terminology](https://docs.puppet.com/references/glossary.html)
- [Components](https://puppet.com/products/platform/core-components) of an infrastructure
  - Server side:
    - [Puppet Server](https://puppet.com/docs/puppetserver)
    - Puppet CA (by default on the master)
    - [PuppetDB](https://puppet.com/docs/puppetdb)
    - Web Frontends (Puppet Enterprise, Foreman, Puppetboard, Puppet explorer...)
    - [Hiera](https://puppet.com/docs/hiera)
  - Client side:
    - [Puppet](https://puppet.com/docs/puppet/) agent
    - [Facter](https://puppet.com/docs/facter)
- The puppet [commands](https://puppet.com/docs/puppet/latest/services_commands.html)
- Help from:
  - [Official documentation page](https://puppet.com/docs)
  - The [Community](https://puppet.com/community)
  - [Support](https://puppet.com/support)

## Modules

If you are an end user, you might even know nothing about Puppet modules and blindly add the data you are told to manage, still for everybody else using, understanding and integrating modules structure is part of the job, so these concepts are given for granted:

- Modules [structure](https://puppet.com/docs/puppet/latest/modules_fundamentals.html) and conventions
- [Forge](https://forge.puppet.com) and GitHub
- [stdlib](https://forge.puppet.com/puppetlabs/stdlib) and other common modules
- [Conventions](https://puppet.com/docs/puppet/latest/cheatsheet_module.html) for templates and files
- [Automatic class parameter lookup](https://puppet.com/docs/puppet/latest/hiera_automatic.html#looking-up-data-with-hiera) on Hiera data
- The `[puppet module](https://puppet.com/docs/puppet/latest/modules_installing.html)` command

## Classification

Classification is how we decide what class, from any module, to include in our nodes, in order to manage the desired resources.

Basically for each Puppet managed node we have to define a list of classes to use, each class comes from modules, either public (so we don't have to write it) or written by a developer.

End users, if allowed to define what applications to install on a node, deal with the classification approach decided by architects.

[Classication](https://www.example42.com/2018/08/20/puppet-classification/) can be done in different ways using different, not necessarily alternative, tools:

- [External Node Classifiers ENC](https://puppet.com/docs/puppet/latest/nodes_external.html):
  - Custom ENC script getting data from any source
  - Classification in Puppet Enterprise console
  - Classification in The Foreman
- In the main `manifests` dir:
  - [Node](https://puppet.com/docs/puppet/latest/lang_node_definitions.html) statement
  - Facts driven class inclusion
- In modules:
  - Roles module
  - Other modules or classes which include and group other classes
- On Hiera
  - Looking up a key (like `classes` or `profiles` with an array of classes to include
  - Classification via example42's [psick module](https://github.com/example42/puppet-psick#classification) [Shameless plug]


## The Control Repo

A modern Puppet setup is based on a control-repo. If you are an architect, you designed it, otherwise you might need to work on it (if hieradata is included in the control-repo) or use it while locallh testing any development.

In any case it's important to know about it.

- Layout:
  - manifests directory, where Puppet code starts to be evaluated
  - Puppetfile, with list of external modules to use and
  - hiera.yaml with definition of hierarchy levels and backend for data lookup
  - Eventually the hieradata|data dir if backend is file based (json,yaml...) (Can stay in an external module)
  - site directory with local modules (such as profiles) (Can stay in an external module)

- Change management:
  - development environment (with pdk)
  - testing (syntax, unit, integration tests)
  - deployment (r10k or alike, with control-repo branches matching Puppet environments)

## Puppet DSL

Strictly speaking knowledge of Puppet language is not necessary for Puppet end users which may configure their data via Hiera.

Still a basic understanding of Puppet abstraction and idempotency principles and the basics of the language is enough to understand better the used modules and eventually write custom ones.

- The Resource Abstraction Layer:
  - Types and providers
  - Everything can be a Puppet resource (via the relevant module)
  - the command `puppet resource`

- Resources, classes and modules
- Type systems
- Facts
  - Native
  - Custom facts in ruby
  - External facts (in any language)
  - Trusted facts via ```csr_attributes.yaml``` file


## ...

Enough?

Enough for now :-)


Alessandro Franceschi
