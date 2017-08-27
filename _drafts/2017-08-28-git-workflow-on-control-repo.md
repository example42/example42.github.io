---
layout: blog
title: Tip of the Week 35 - GIT workflow for Puppet control-repositories
---

Modern best practices for management of Puppet Code suggest to make use of a control-repository.
Within a control-repository one manages the whole Puppet Code in a centralized pattern but istill allowing flexibility and code staging:
- upstream modules are referenced in Puppetfile
- Profiles and Roles are managed directly inside the repository
- Hiera configuration and data are also part of the control-repository

Usually it is recommended to rename master branch to production. Older versions of Puppet might behave irratical when using a puppet.conf section name (master, main, agent) as an environment name.
Most people use an additional branch for development and staging purpose.

This will result in the following branches:
- production
- integration
- development

New features are usually developed inside a feature branch.

Up to here everything is fine. But....

How to proceed if you are developing several features with multiple developers in parallel?

Time point 0: Developer A creates a feature branch based on production
Time point 1: Developer B creates a feature branch based on production
Time point 2: Developer B finished his work and merges his feature branch into development and integration
Time point 3: Developer A merges his feature into development and integration
Time point 4: Developer A has finished his tests and wants to merge his feature into production

BANG!

Developer A can not merge integration branch into production as integration branch has an additional feature not yet ready for production.
Usually people start cherry-picking their features which normally requires to squash all commits into a single commit.

Let's rethink our branches.
Why do you need development and integration as long living branches?

Why not have production branch only and short living feature branches?
OK, you want to test on a dedicated infradtructure which uses a fix Puppet environment name.
OK, you must wait for your ITIL release manager to approve the change in production.
This brings you to two branches: integration and production.

The production branch is the default branch for all of your systems.
Differences in infrastrucure stages are configured by having a hiera hierarchy for your stages.

Integration branch is the branch where you separate your feature deployments. Every feature which is not yet fully developed may not be merged into integration branch.
This will lead to the following concept:

- production is your default branch
- integration is your feature isolation branch
- integration may differ one code commit from production only

Happy hacking on your control repo!

Martin Alfke

