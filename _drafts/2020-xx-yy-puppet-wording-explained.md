---
layout: blog
title: Puppet Tip XYZ - Puppet Wording explained
---

When reading emails from Puppet mailinglist or when takling to people I sometimes hear wrong wording regarding Puppet and its essential concepts.
This mostly leads to misunderstanding und it takes longer to identify the real issue someone has.

This posting gives you an overview on Puppet topics and the correct words to use.

* Table of content
{:toc}

# Puppet infrastructure components

## Single Master

A standalone single master is called `master`. It runs all Puppet components like

- PuppetCA
- Puppet Compiler
- PuppetDB
- PostgreSQL
- Puppet Console (PE only)
- Puppet Orchestrator (PE only)

## Master and Compilers

In case of many systems or in case of network separation you want to install dedicated compilers.
Either behind a load balancer or as single instance with direct Agent access.

The central System is still called `master`. The additional systems are called `compiler`. A compiler runs the following componentes:

- Puppet Compiler
- PuppetDB

## PuppetDB and PostgreSQL

PuppetDB is not a database! PuppetDB delivers a HTTP(S) REST API which translates API calls into SQL.

At the moment PuppetDB can only work with a PostgreSQL database.

# Puppet Code components

## Manifests, Classes and Defined Types

Any file which has Puppet DSL code inside is called a `manifest`.

Depending what is inside the manifest you will have

- a `class definition`,
- a `defined type` or
- a Puppet `function`

## Parameters and variables

Within Puppet code one can make use of `variables`. There are special variables which are defined in a class or defined type header.

These special variables are calloed `parameters`.

Parameters can be specified upon declaration and will mostly be used with Hier aand automatic data binding.

Variables are inside the code body and can not be changed.

Happy puppetizing,

Martin

