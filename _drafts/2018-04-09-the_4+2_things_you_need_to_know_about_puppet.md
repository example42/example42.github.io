---
layout: blog
title: Tip of the Week 67 - The 5 things you need to know when starting with Puppet
---

Let's say you know nothing or few about Puppet.

Or maybe you know and have started to use it, but still don't know well all its components or have not a clear understanding of the whole picture.

There are various things to know to get a clear understanding on how to work with Puppet and automate your systems infrastructure in a smart and sustainable way.

The amount of things to know, is definitively not limited, and may look overwhelming at the very beginning, but once the basic principles are grasped, everything becomes clearer, and you are able to undestand how easily you can represent and manage your infrastructure with data managing more and more complex scenarios.

The basic things to know about Puppet are:

## Terms, and components

- puppet command
- Essential components and terminology
- Components of a Puppet infrastructure
  - Puppet master
  - Puppet CA (by default on the master)
  - PuppetDB
  - Web Frontends (Puppet Enterprise, Foreman, Puppetboard, Puppet explorer...)

## Modules

- Modules structure and conventions
- Forge and GitHub

## Classification

Classification is how we decide what class to include in our nodes, in order to manage via Puppet any configuration  on our nodes.

Basically for each Puppet managed node we have to define a list of classes to use, each class comes from modules, either public (so we don't have to write it)

- ENC Foreman / Puppet Enterprise
- In manifests
- On Hiera

## Hiera

- Class parameters via Hiera
- hiera.yaml configuration
- Hierarchies


## The Control Repo

- Structure
- manifests directory
- Puppetfile
- Hiera data


Alessandro Franceschi
