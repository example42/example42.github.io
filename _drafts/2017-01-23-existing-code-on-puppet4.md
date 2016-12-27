---
layout: blog
title: Tip of the Week [4] - Existing code and Puppet 4
---

Starting with Puppet 4 on greenfield is easy.

But how to upgrade from Puppet 3 to Puppet 4 with an existing codebase?

To be honest: it depends.

When you have a really old code base (e.g. you started using Puppet 2.6 or older) and you never adopted to new best practices you might reconcider a full rewrite from scratch. Don't mess you new Puppet 4 infrastructure with old practices Puppet code.

When you have constantly adopted to best practices and removed deprecations from your Puppet code base you are in the comfortable situation to use tools which help ypu ensuring that your code is working on Pupprt 4, too.

First you want to ensure that you are running the latest Puppet 3 Master version (3.8.x) and that your Agents are upgraded to the same version, too.

There are several ways to identify whether your code works in the same way on Puppet 4:
  - check identical catalogs with Puppet 3 and 4
  - test by enabling the Puppet 4 parser on a Puppet 3 Master
  - integration testing with different Puppet versions

Checking identical catalogs needs an additional module installed onto the master. You can choose between [zack/catalog_diff](https://github.com/acidprime/puppet-catalog-diff) or [github/octocatalog_diff](https://github.com/github/octocatalog-diff).


Martin Alfke
