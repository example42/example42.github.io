---
layout: blog
title: Tip of the Week 48 - LibRAL and a proposal for the new Puppet Resource API
---

Puppet has always run on fast development cycles. Even though only a very few releases required people to refacter their existing Puppet code (e.g. the migration from Puppet 3 to Puppet 4).

Puppet still has lots of upcoming changes and still follows the Open Source idea. All discussion on upcoming development or new features tkae place in the [Puppet Specification](https://github.com/puppetlabs/puppet-specifications) repository.

At the moment there is at least one [PR](https://github.com/puppetlabs/puppet-specifications/pull/93) which deals with idea of a new Puppet Resource API, extending the way how we usually deal with and develop custom types and providers.

Besides this we see more mature ideas made available as new git repositories like [libral](https://github.com/puppetlabs/libral).

This posting will dig into libral and the new proposed Puppet resource API.

# LibRAL

LibRAL is described as "a systems management library that makes it possible to query and modify system resources [...] through a desired-state API".
The aim is to not only query and modify built in resources like files, packages and services, but to also add a new API for managing new kind of resources. It follows Puppet concept of idempotency, only changing a resource when desired state does not match actual state and keep the resource untouched if it is in sync.
Besides this, LibRAL was developed for low performance systems like devices or containers.



# Puppet Resource API

Martin Alfke

