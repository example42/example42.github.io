---
layout: blog
title: Puppetize Digital - example42 talk about GIT workflows
---

[Puppetize Digital](https://digital.puppetize.com/series/Puppetize-Agenda/schedule) is coming! November 19th!

example42 is super excited that we are again delivering a talk to a Puppet conference.

This year [Martin Alfke](https://digital.puppetize.com/series/d90513c03829/show_speaker_details) is talking about GIT workflows.

The talk was prerecorded as Martin recovers from a dental surgery and will be broadcasted on November 19th at 1:30 PM (GMT) and at 2:30 PM (AEDT).

* Table of content
{:toc}

# Puppet and GIT

Working on Puppet always is fun. But working with GIT is hard for many people who are new to GIT.

## Single long living branch - simple GIT

Within this talk I will show why a single long living branch (production) makes sense for most installations.

I will show how you bring changes into your environment by using feature branches.

## Staging branches

But how do you deal when you have separated networks?

e.g. people are not allowed to do changes in production network. Changes must de done in the development network.

In this case you need GIT servers in each network zone. How do you now stage your code from development to production network?

## GIT flow

What happens if you are in a more ITIL based environment.

In this case it might be required to have several long living branches like production, testing, development.

How do you now bring individual changes into production and how to backport hotfixes into development.

This is the situation where you want to consider following the [GIT Flow](https://nvie.com/posts/a-successful-git-branching-model/) concept.

## Summary

I will explain when and how to make use of which concept and what are the main differences and challenges.

- Puppet Control-Repo
- Simple GIT
- Staging Branches
- GIT Flow

Happy puppetizing and git-ting,

Martin

