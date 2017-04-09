---
layout: blog
title: Tip of the Week 14 - Environment enforcement
---

Think about the following situation:

You have a node running in development environment.
A user logs in and runs ```puppet agent --test --environment production```.

What will happen: the node will receive production ready code.
This is OK... but... what if you use the environment to also pass data like passwords, users, accounts to your nodes?

In this case the development system will have all production data and users are happy that they now can connect to your production database.

If you would not like to allow this, you have to make use of an external nodes classifier (ENC).


    # /etc/puppetlabs/puppet/puppet.conf
    [master]


Martin Alfke

