---
layout: blog
title: Tip of the Week 10 - Server side noop mode
---

Puppet has a well known command option that allow us to make dry runs, with clients fetching the catalog from the Master and showing what it would have changed if it were applied for real.

From the command line on the client this can be done with a command like:

    puppet agent -t --noop

There are situations, anyway , where it would be preferable to activate nood directly from the server, forcing noop mode on one or more clients or sets of resources.

This is possible thanks to the [trlinkin-noop](https://github.com/trlinkin/trlinkin-noop) module, which provides a function, called ```noop()``` which automatically add the noop argument to every resource in the current and the child scopes.

A use case we've found quite useful in many occasion is the possibility to manage and force the noop mode directly in Hiera.

To do this for all the resorces, it's enough to add in the top scope, in one of the main manifests, for example ```manifests/site.pp``` a few lines of code like these:

    $noop_mode = hiera('noop_mode', false)
    if $noop_mode == true {
      noop()
    }

Basically we look for a hiera key called ```noop_mode``` if this is set to true, then noop is enabled in the given Hiera context (for a specific node, an environment or all the nodes) with an entry (in yaml format) like:

    ---
      noop_mode: true

What are the use cases for such an approach? Various.

For example when you have to deploy large or potentially dangerous Puppet code refactorings and you can't fully test their effect until you deploy to production.

In these cases being able to rollout your changeset with noop mode enabled (for all or the most important nodes) allows you to test and review the real consequences on your servers with more safety and confidence.

In some situations you may prefer to have production servers only running in safe noop mode, and trigger real changes only upon request.

This can be done via Hiera, as seen before, but also eventually setting a top scope parameter on an ENC like PE console or The Foreman) and using it as trigger for the ```noop()``` function in your ```site.pp```.

In some situations you might want to enforce real mode whatever is the noop setting. This can be done by calling the noop function with the false parameter:

    if $enforce == true {
      noop(false)
    }

If this is done in a class with a parameter called $enforce, for example, you can let users decide if to ignore or not any noop option. 


Alessandro Franceschi

