---
layout: blog
title: Puppet Tip XYZ - Puppet Terminology explained
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

## Master and Replica

When using Puppet ENterprise one has the option to have an active/passive Cluster which replicates the PostgreSQL Database between two nodes.
The active Puppet Server is called `master` or `primary`.
The passive Puppet Server is called `replica`.

## PuppetDB and PostgreSQL

PuppetDB is not a database! PuppetDB delivers a HTTP(S) REST API which translates API calls into SQL.

At the moment PuppetDB can only work with a PostgreSQL database.

# Puppet Code components

## Manifests, Classes, Defined Types, Pupept Functions and Node Classification

Any file which has Puppet DSL code inside is called a `manifest`.

Depending what is inside the manifest you will have

- a `class definition`,
- a `defined type` or
- a Puppet `function` or
- `node classificatoins`

## Parameters and variables

Within Puppet code one can make use of `variables`. There are special variables which are defined in a class or defined type header.

These special variables are called `parameters`.

Parameters can be specified upon declaration and will mostly be used with Hier aand automatic data binding.

Variables are inside the code body and can not be changed.

# Custom Facts, Functions, Types, Provider

Whenever you her the term `custom` within Puppet, you can be absolutely sure that this is now Ruby code!

## Custom Facts

Puppet allows one to extend Facter by developing custom facts.
The filename is irrelevant, but you should ensure that filenames are unique.

We recommend to use the fact name as part of the filename.
Additionally we recommend to prefix self developed custom facts with company or departement short name.

## Custom Functions

Puppet allows to extend Puppet compiler functionality by having custom functions.
Different to custom facts, the file name of the custom function must use the function name!

## Custom Types

Any time when the existing types are not really usable for you (e.g. you have a self developed application which must be configured using cli commands instead of config files) you can choose to develop your own set of types/providers.

The type describes the Puppet DSL:
- the type name
- which properties can be changed or set
- which parameters are possible

### Properties vs. Parameters

Properties is anything you can read or set.
COnsider the user reosurce type: uid and shell are properties.

Parameters let you choose how something is done. It is not possible to identify if a parameter was used to create a resource.
Consider the user resource type and the managehome parameter. After the user is created it is impossible to verify if the homedirectory was created as a directory by itself or if it was created when adding the user.

## Custom Providers

If you have developed a type, you want to be sure that the type can be managed on a system.
This is where you need the provider for.
The provider knows about commands, location of files, possible command options and parameters.

The provider can optionally also check for all exusting resources of a specifc type. That is what we need the self.prefetch and self.instance ruby classes for.


Happy puppetizing,

Martin

