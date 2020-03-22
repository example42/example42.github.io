---
layout: blog
title: Puppet Tip ___XXX___ - Puppet Control-Repo Workflow
---

When starting with Puppet you usually first create your Puppet GIT control-repository.
It is up to you, whether you just copy and adopt our [Open Source Control-Repository](https://github.com/example42/psick) or if you prefer to start with an empty repository.

In both cases you want to carefully consider your workflow on how to get changes into your code base.

The most simple option is to only use the `production` environment branch and add all changes via feature branches and merge requests.

When working in an ITIL based change management environment this simple approach does not adopt to change management requirements which ony allows code changes being tested on dedicated systems prior being deployed to production systems.
This is where one should consider adopting the [GIT Flow](https://nvie.com/posts/a-successful-git-branching-model/) concept. 

This blog post explains the *simple* and the *git flow* based change workflow for a Puppet control-repository.

* Table of content
{:toc}

## Simple workflow

Within the simple workflow you are working with a single long living branch which we usually call `production`.
We prefer to set this branch to "protected" to prevent any direct changes. All changes must be delivered using feature branches which will be merged into `production` branch.

This is similar to many upstream development procedures of most Puppet library module code.

Pro:
easy to learn

Con:
changes on Puppet code affect all systems at once

An example:

    prod    prod
      |     |
      feature

You will statr by creating your own feature branch:

    git checkout -b <feature_branch>

At customers we usually recommend to build the name of the branch based upon useer or team name. e.g. `git checkout -b alfke_new_db_role`.

Additionally we recommend to work with rebase on feature branches instead of merge. Rebasing will take care that your feature branch changes are placed after any other productoin changes.

If you see changes on production branch you need to rebase: `git rebase origin/production`

Any feature branch should result in a merge request. Every merge request should consist of a single commit only. Best option is to use `git commit --amend` on any additional change or to squash all commits once your feature is ready to get deployed.

## GIT Flow

But how to proceed, if you want to have Puppet code available for each of your infrastructure stages?
In this case you have to create several long living branches like `development`, `testing` and then `production`. You can use any string lower case letters and numbers and underscore as environment name. Maybe you prefer other naming like `dev`, `qa`, `int`, `pre_prod`, `prod`.

But using multiple branches makes it harder to deploy single changes independently. What will happen upon merge if you have two changes within development branch and only the second one may be deploed to the next branch?

One must reconsider on how you look at your branches within your GIT repositorie: *Instead of just seeing one single code base within a GIT repository you should see several loosly coupled streams of code placed into branches on a single GIT repository*.

Each of these code stream branches can be developed and improved indepdendently and all development must be done in a stream feature/change branch.
All workflows must be tracked within a ticket. Within this change ticket you follow work and deployment be placing them into subtasks for each stream branch.


    dev         dev
      |         |
      dev_feature
      
          qa        qa
           |        |
           qa_feature
           
                 prod          prod
                    |          |
                    prod_feature

This might look like duplicate work, as you need to apply the same change in multiple places.
But on the other hand, this deployment and staging methods allows you to also deploy hotfixes in production and backporting them to development.

Multiple branches have several additional requirements:

- Rebase and Squashing is a hard must for each merge.
- Cherry-Picking is the way to get a change from one feature branch to another.
- All long living branches must be protected. Changes may only be added via merge requests. No exceptions allowed.
- Normal code staging is done by merging into dev and cherrypicking the change into a merge request to the other branches.
- Hotfixes in testing are developed on testing feature branch, forwarded via cherry-pick to production feature branch and backported (also cherry-pick) into development feature branch.
- Hotfixes on production branch are developed on production feature branch and are backported via development feature branch and testing feature branch (both cherry-pick).

Pro:
adopts agile and waterfall concepts

Con:
needs more GIT knowledge

## Recommendations

When to use which solution?
What are characteristics which will make you consider using GIT Flow. What are the requirements?

Deploy fast and often? Single plattform, no stages? -> Use simple
Deployment may stuck for weeks in a specific stage? Deployments are rare and slowly? ITIL based change management and change approval process? -> Use GIT Flow

Switching to GIT Flow allows more flexible handling of complex change approval requirements but needs more understanding on GIT squash, rebase and cherry-pick and how to deal with merge conflicts.

Martin Alfke

