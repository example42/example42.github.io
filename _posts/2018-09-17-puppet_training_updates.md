---
layout: blog
title: Tip of the Week 90 - Update of official Puppet Training courses
---

example42 trainers conducts the official Puppet Training courses since 2011.
Since then Puppet has adopted best practices multiple times. These adoptions also had an impact on the official training courses material.

{:toc}

## The old courses

In the early days everybody was using a Linux based virtual machine on every attendee laptop.
The last major update was done in 2016, when the course material switched to Puppet 4 and people used a Docker container to run their course exercises.
Containers were provided by the trainer.
Course management was built around a self developed tooling where attendees were able to create their account (which was then used in [Gitea](https://gitea.io/en-us/), Puppet Enterprise Console and to instantiate the containers).

The training was fully focusing on Linux distributions and Windows was explained but not actively done. All attendees were asked to have knowledge in vim.

Many attendees complained about to few active doings and to deep introduction into Puppet instead of providing a good starting point for building their infrastructure.

## The new courses

With the newest content change, Puppet renamed the Puppet Fundamentals Training to "Getting Started with Puppet".

### Initialising Puppet in your infrastructure

The new course setup is different. We start using [bolt](https://puppet.com/docs/bolt/0.x/bolt.html) (the Puppet open source ad-hoc task utility) to install Puppet agent on non-managed systems within a cloud based setup. We still have a course management, but git server was switched from gitea to [GitLab](https://about.gitlab.com/).

### Step-by-step declaration of your infrastructure

The whole training content is now built around a [control repository](https://puppet.com/docs/pe/2018.1/control_repo.html). Instead of coding everything by ourselves, we immediately introduce the Puppet Modules and the Roles and Profile pattern.

In the base course we will not go too deep into the panning of a good [hiera](https://puppet.com/docs/puppet/5.4/hiera_intro.html) setup (this is done in an advanced course), but we will use an existing hiera configuration to separate data from code.

### On-Premise and off-premise usage of Puppet

As the course is now cloud based, we will have hands-on exercises for managing Windows systems and different Linux distributions on AWS.
This opens the course also for Windows administrators.

### Your code, your environment

People can now choose the IDE they prefer. Depending on existing knowledge it is now possible to either use VIM or Visual Studio Code.

## Training Availability

The new courses are available from Puppet starting at [Puppetize Live](https://puppet.com/puppetizelive) in October 2018.

example42 will switch to the new training courses after we have verified the setup, see our [list of upcoming training courses](https://www.example42.com/#training).

Martin Alfke
