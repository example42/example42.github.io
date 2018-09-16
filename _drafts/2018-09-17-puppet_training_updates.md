---
layout: blog
title: Tip of the Week 90 - Update of official Puppet Training courses
---

example42 trainers conducts the official Puppet Training courses since 2011.
Since then Puppet has adopted best practices multiple times. These adoptions were also added to the official training courses material.

## The old courses

In the early days everybody was using a virtual maschine on every attendee laptop.
The last major update was done in 2016, when the course material switched to Puppet 4 and people used a Docker container to run their course exercises.
Course management was built around a self developed tooling where attendees were able to create their account (which was then used in [Gitea](https://gitea.io/en-us/), Puppet Enterprise Console and the container).

The training was fully focusing on Linux distributions and Windows was explained but not actively done. All attendees were asked to have knowledge in vim.

Many attendees complained about to few active doings and to deep introduction into Puppet instead of providing a good starting point for building their infrastructure.

## The new courses

With content change, Puppet renamed the Puppet Fundamentals Training to "Getting Started with Puppet".

The new course setup is different. We start using [bolt](https://puppet.com/docs/bolt/0.x/bolt.html) (the Puppet open source ad-hoc task utility) to install Puppet agent on non-managed systems within a cloud basedsetup. We still have a course management, but git server was switched from gitea to [GitLab](https://about.gitlab.com/).

The whole training content is now built around a [control repository](https://puppet.com/docs/pe/2018.1/control_repo.html). Instead of coding everything by ourselves, we immediately introduce the Puppet Modules and the Roles and Profile pattern.

In the base course we will not go too deep into the panning of a good [hiera](https://puppet.com/docs/puppet/5.4/hiera_intro.html) setup (this is done in an advanced course), but we will use an existing hiera configuration to separate data from code.

As the course is now cloud based, we will have hands-on execrises for managing windows and people can choose the IDE they prefer, wehther it is VIM or Visual Studio Code.

## Availability

The new courses are available from Puppet starting at [Puppetize Live](https://puppet.com/puppetizelive) in October.
example42 will switch to the new training courses by end of this year, see our [list of upcoming training courses](https://www.example42.com/#training).

Martin Alfke