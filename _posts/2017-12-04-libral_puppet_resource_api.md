---
layout: blog
title: Tip of the Week 49 - LibRAL and a proposal for the new Puppet Resource API
---

Puppet has always run on fast development cycles. Even though only a very few releases required people to refactor their existing Puppet code (e.g. the migration from Puppet 3 to Puppet 4).

Puppet still has lots of upcoming changes and still follows the Open Source idea. All discussion on upcoming development or new features take place in the [Puppet Specification](https://github.com/puppetlabs/puppet-specifications) repository.

At the moment there is at least one [PR](https://github.com/puppetlabs/puppet-specifications/pull/93) which deals with idea of a new Puppet Resource API, extending the way how we usually deal with and develop custom types and providers.

Besides this we see more mature ideas made available as new git repositories like [libral](https://github.com/puppetlabs/libral).

This posting will dig into libral and the new proposed Puppet resource API.

# LibRAL

LibRAL is described as "a systems management library that makes it possible to query and modify system resources [...] through a desired-state API".
The aim is to not only query and modify built in resources like files, packages and services, but to also add a new API for managing new kind of resources. It follows Puppet concept of idempotency, only changing a resource when desired state does not match actual state and keep the resource untouched if it is in sync.
Besides this, LibRAL was developed for low performance systems like devices or containers.


# Puppet Resource API

The resource API is at a very early state. There is not even a finalised document describing the new API. At the moment this is more a discussion base and Puppet developers are eager to get feedback on the new Resource API.

An interesting way for new resource API can be found within the PR at the [simple_apt.rb](https://github.com/puppetlabs/puppet-specifications/pull/93/files#diff-7dfcf5a8b2b0d5cecfe0a804c5d92eb0) example.
Here David uses a SimpleResource concept which is a generic concept for any new resource type (see line 98 and following in [Module::SimpleResource](https://github.com/puppetlabs/puppet-specifications/pull/93/files#diff-af7afe9cfb6cd905213628f357c0629bR102-R90).

We are looking forward to seeing more examples and ways on how to make use of a new way to develop Puppet types and providers using the new API.
Feel free to comment within the PR or contact the developers via Slack or IRC.

Martin Alfke
