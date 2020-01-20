---
layout: blog
title: Puppet Tip ___XXX___ - Puppet Control-Repo Workflow
---

When starting with Puppet you usually first create your Puppet GIT control-repository.
It is up to you, whether you just copy and adopt our [Open Source Control-Repository](https://github.com/example42/psick) or if you prefer to start with an empty repository.

In both cases you want to carefully consider your workflow on how to get changes into your code base.

The most simple option is to only use the `production` environment branch and add all changes via feature branches and merge requests.

When working in an ITIL based change management environment this simple approach does not adopt to change management requirements which allow code changes being tested on dedicated systems prior being deployed to production systems.
This is where one should consider adopting the GIT Flow concept. 

This blog post explains the simple and the git flow based change workflow for a Puppet control-repository.

* Table of content
{:toc}

## Simple workflow

Only production and branch protected.
Changes as feature branches only.
Similar to upstream development of most Puppet library module code.

Pro:
easy to learn

Con:
changes on Puppet code affect all systems at once

An example:

    prod    prod
      |     |
      feature

## GIT Flow

In this case you have to create several long living branches like `development`, `testing` and then `production`. You can use any string lower case letter sa nd numbers and underscore as environment name. Maybe you prefer other naming like `dev`, `qa`, `int`, `pre_prod`, `prod`.

But using multiple branches makes it harder to deploy single changes independently. What will happen upon merge if you have two changes within development branch and only the second one may be deploed to thenext branch?

Multiple branches have several additional requirements.
Rebase and Squashing is a hard must for each merge.
All long living branches must be protected. Changes may only be added via merge requests. No exceptions allowed.
Hotfixes in testing are developed on testing feature branch, forwarded to production feature branch and backported into development feature branch.
Hotfixes on production branch are developed on production feature branch and are backported via development feature branch and testing feature branch.

Pro:
adopts agile and waterfall concepts

Con:
needs more GIT knowledge

## Production isolated from development?

Needs GIT server and Puppet Master in prod and dev.
Puppetfile references an DNS alias!

### Simple workflow

Same as above.
After CI run in dev the deployment to prod Puppet is either automated or a manual CI step.

### GIT Flow workflow

Needs a GIT sync system.
Pull frm dev, push to prod (branches and code)

## Recommendations

When to use which solution?
What are characteristics which will make you consider using GIT Flow. What are the requirements?

Deploy fast and often? Single plattform, no stages? -> Use simple
Deployment may stuck for weeks in a specific stage? Deployments are rare and slowly? ITIL based change management and change approval process? -> Use git flow

Switching to GIT Flow allows more flexible handling of complex change approval requirements but needs more understanding on GIT squash and rebase and how to deal with merge conflicts.

Martin Alfke

