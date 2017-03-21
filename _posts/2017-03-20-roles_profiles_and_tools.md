---
layout: blog
title: Tip of the Week 12 - Roles, profiles and tools
---

Roles and profiles is an established pattern that for years has helped Puppet architects in the organization of their code base.

A role, and only a role, is typically assigned to a node, describing its business functionality (blog webserver, api backend, relay mail server...) and includes one or more profiles.

A profile is basically a wrapper class which may use a component module (like the ones for apache or mysql or whatever we find on the Modules Forge) and adds site specific resources: the things we need to configure servers in the way we want.

Over the years I found myself using slight variations on this pattern, according to use cases and context.

For example I find more flexible the possibility to define the profiles to use in nodes, not in "static" role classes, but via Hiera.

I consider absolutely necessary to have in my hiera's hierarchy a layer that represents the role of the machine, and since this is already there I can use it as layer of reference where to include profiles.

The Puppet code needed to define in Hiera the profiles to use is quite straightforward:

    hiera_include('profiles', [])

The hiera_include function looks for an array and includes as classes all the elements of the array.

Starting from Puppet 4.9 Hiera functions in Puppet DSL are deprecated, so the above code can be written with:

    $profiles = lookup({
      name          => 'profiles',
      merge         => 'unique',
      default_value => [],
      value_type    => Array[String],
    })
    $profiles.each | $p | {
      contain $p
    }

This alternative may look more complex but it's actually much more powerful. Check [this](https://www.devco.net/archives/2016/03/13/the-puppet-4-lookup-function.php) blog post for R.I.Pienaar for more details.

For a smarter alternative of the above, you can simply have something like:

      lookup('profiles', Array[String], 'unique').contain

One of the benefit in defining what profiles to include via Hiera is that we have much more flexibility on where to include them.

We can set them at the role's hierarchy level but we can also set them at other levels, for example managing per node exceptions.

So, in my latest control-repos I don't have a role module where I define my role classes, as everything is managed via Hiera, but I have another kind of site module: **tools**.

The tools module is usually coupled with the profile one and basically contains defines which are used by the profile classes.

The basic idea is that tools contains local facts, functions, data types, defines, types and providers which are not provided by a dedicated module and which serve us for our own purposes, be they very specific or somehow common.

An example of a tools module is in example42's [PSICK](https://github.com/example42/psick), a rather complete control-repo, here, since we make a large use of Tiny Puppet which saves us from the need of importing several external modules, we place various defined for common (and not so common) purposes.

Some of them should actually stay in dedicated modules, along with the relevant profiles classes, but our control-repo is somehow opinionated and has its own rules ;-)

Alessandro Franceschi
