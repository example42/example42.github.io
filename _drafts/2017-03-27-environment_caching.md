---
layout: blog
title: Tip of the Week 13 - Environment caches
---

Usually a Puppet Server as a monolithic installation can handle up to 4000 nodes. In larger environments one can easily scale this by adding compile servers placed behind a load balancer.

But prior you throw additional hardware on your load issue, Puppet server allows you for some scaling.
One of the ways to prevent scaling issues is to make use of Puppet environment cache.

When activating the environment cache, the Puppet master process compiles catalogs for a node once only and keeps the generated catalog in memory.
This also has an impact on available RAM on the Puppet master as all catalogs are kept in RAM - either for a specific timeout or permanently.

The environment cache can either be set globally or per environment. Global setting must be done in puppet.conf file:

    # /etc/puppetlabs/puppet/puppet.conf
    [master]
    # environment_timeout = 180 # default 3 minutes
    environment_timeout = 100

The environment_timeout option can have one of the following values:

 - 0 - never cache catalogs
 - unlimited - always use catalog cache
 - <number> - duration to keep a catalog in cache

Mostly one does not like to set environment_timout as a global setting.
In production environment . where changes are less often - you want to have an environment cache, whereas in development environment - where you push changes very often - you want to disable the cache.

Environment specific cache settings can be put in environment.conf file and has the same look and options according to the global setting in puppet.conf.

Now let's set environment in the production environment:

    # /etc/puppetlabs/code/environments/production/environment.conf
    environment_timeout = unlimited

But how can I let Puppet know that new code is available so the compiler uses the new code instead of the cached catalog?

Puppet server provides an [environment API](https://docs.puppet.com/puppetserver/latest/admin-api/v1/environment-cache.html) where you can delete specific environments. Usually you want to run this API call on r10k postrun.
This also solves another side effect: race-condition when updating an environment while the compiler is in progress of generating a catalog for a node.

Martin Alfke

