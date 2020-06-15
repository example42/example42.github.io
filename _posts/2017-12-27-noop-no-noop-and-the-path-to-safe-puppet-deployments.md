---
layout: blog
title: Tip of the Week 52 - Puppet noop, no-noop and the path to safe Puppet deployments
tags: bestpractices
---

We have already talked in this blog, about [server side noop mode](https://www.example42.com/2017/03/06/server-side-noop-mode/) in the past, now we come back to the topic to expose how we currently prefer to use noop mode, and how to enforce no-noop mode on specific classes.

Puppet **noop mode** mode allows us to review the changes that Puppet would do on the system without actually applying them.

This is particularly useful when managing critical servers, as it allows to push to production Puppet code and data in a more controlled, safe and manageable way.

There are various ways we can enforce noop mode when using this control repo: let's review them.

### Setting noop from the client

In any Puppet installation it's possible to run Puppet in noop mode specifying the ```--noop``` option in the command line:

    puppet agent -t --noop

This applies only for that specific Puppet run, so if there's a Puppet agent service running in the background, that service will run Puppet in normal mode.

The noop setting can be configured and made persistent also in ```puppet.conf```:

    [agent]
    noop = true

If you use the [PSICK module](https://github.com/example42/puppet-psick) you can configure it on Puppet Enterprise clients as follows:

    # We want to manage noop mode on clients:
    psick::puppet::pe_agent::manage_noop: true

    # We want to set noop to true
    psick::puppet::pe_agent::noop_mode: true

    # We enforce no-noop mode on the pe_agent class to be
    # able to revert our noop settings. Details in no-noop section.
    psick::puppet::pe_agent::no_noop: true

Note that this is the common and official approach to manage noop mode and is controlled and managed from the client, not on the server.

### Setting noop server-side

In the [PSICK control-repo](https://github.com/example42/psick) we use the **trlinkin-noop** module which provides a function called ```noop()``` which adds the noop metaparameter to each resource.

We use this function in ```manifests/site.pp```:

    $noop_mode = lookup('noop_mode', Boolean, 'first', false)
    if $noop_mode == true {
      noop()
    }

This code sets the ```noop_mode``` variable via a Hiera lookup for the key ```noop_mode```. If it's not found on Hiera, then the default value is false.

If the ```noop_mode``` variable is true then noop metaparameter is added to all the resources of the catalog.

It's recommended to limit the usage of noop_mode key on Hiera only when necessary, for example when a massive or invasive code change has to be promoted to production and we want a safe net where we can selectively remove noop_mode to control the propagation of change.

For example when pushing to production particularly critical changes it's possible to force noop mode for all the servers adding in ```hieradata/common.yaml```:

    noop_mode: true

To test the actual changes we could override this in a Hiera yaml (something like ```hieradata/env/test.yaml``` to give you an idea) which configures a subset of our servers:

    noop_mode: false

Note that this is not the typical way to manage noop mode in Puppet and when using the Puppet Enterprise console you will see nodes where noop is applied with this approach undef the "Nodes run in enforcement" group (and not in noop mode) in the dashboard. Still, checking report you will be able to notice that actually no resource is really applied and you should see eventual changes in the noop column.

Final result is the same (no resources are really applied) but they are shown differently on PE console.

#### Important caveat with server-side noop mode

There's a small but rather important thing to consider when using the noop() function: since it works by adding the noop metaparameter to a resource, and can override a normal puppet run without noop set client-side, it can have unpredictable effects when you are working with **exported resources** which, when missing, alter the configuration of the node which collects them.

Let's see an example:

- You run puppet in normal mode on a node which exports a concat resource used by a load balancer. When server side noop mode is used , this concat resource is exported with noop = true
- When you run puppet on the load balancer which collects the concat resources previously exported (with noop set server side), Puppet will rebuild the target configuration without the concat fragment where noop is true.

This doesn't happen when you run Puppet with noop mode client side-

How to avoid such situations?
- Identify the cases where missing exported resources can actually change some configurations (rather than just not managing for a single Puppet run a resource previously configured). This basically happens whenever you export concat fragments and where you export files in directories which are completely managed and where files not explicitly managed by Puppet are purged.
- In the above cases, be sure to have a normal real Puppet run on the exporting nodes before doing a Puppet run in the collecting ones.


### Enforcing no-noop mode

In some cases we might need to enforce the applications of the resources of some classes in every case, whatever is the noop mode.

Some of the profiles used in the PSICK module have the no_noop parameter: if set to true all the resources of the class are enforced and are applied whatever are the noop settings (either client or server side). By default no_noop is set to false and nothing changes in terms of noop management.

This allows us to have some server where Puppet runs in noop mode but have still some resources always applied.

In order to set no_noop mode for a class, use hiera data like:

    psick::dns::resolver::no_noop: true
    psick::hostname::no_noop: true
    psick::hosts::file::no_noop: true
    psick::puppet::gems::no_noop: true
    psick::puppet::pe_agent::no_noop: true # This is required to be able to change the noop setting client side

In case the no_noop parameter is not present in a profile, it's quite easy to add it:

    class my_class (
      [...]
      Boolean $no_noop            = false,
    ) {

      if $no_noop {
        info('Forced no-noop mode.')
        noop(false)
      }
      [...]
    }

### Puppet code deployment and application workflows

Enabling noop mode on some clients, the most important ones, or the whole production ones, allows us to implement some sophisticated and safe workflows for the testing and the deployment of the Puppet code and data that manage our nodes.

Some basic principles have to be considered in order to design them in the most effective way:

  - Server side noop mode if set to true, overrides any client setting
  - Setting a class no_noop parameter to true overrides any noop setting either client or server side
  - We can manage via Hiera both server and client settings, giving us full flexibility on where to set it, still we should limit as much as possible the places where we configure it, and possibly, to avoid unnecessary confusion, not use, on regular basis, both server and client settings at the same time (exceptions below).
  - Client settings are effective after the Puppet run that sets them. Server side settings are immediately effective.
  - Always consider that classes with no_noop set to true are always applied, if you make changes to them consider the possibility to set no_noop temporarily to false, before propagating such changes everywhere.

The following approach is recommended when noop mode is used or desired:

  - Set noop mode client side on the nodes where we want it (all production nodes or particularly critical ones)
  - Use server side noop mode only when deploying big or potentially dangerous code/data changes, keep it undefined in normal conditions
  - Have a CI pipeline which triggers Puppet runs on canary nodes, also in production, enforcing one-shot no-noop runs
  - In the CI pipeline trigger noop Puppet runs on the other production nodes and verify the result
  - Do not accumulate too many changes on noop nodes: run Puppet in no-noop mode on production servers as soon as possible (eventually do that in maintenance windows if you are particularly prudent).

To trigger real no-noop Puppet runs and apply changes on nodes normally running in noop mode different approaches can be used:

  - At the end of the CI pipeline if everything is OK trigger (manually or automatically) a no-noop Puppet run on nodes normally in noop mode
  - Actual execution of a no-noop run can be done via a Puppet task like ```psick::puppet_agent``` (it has a parameter for forcing it) or any other tool that can remotely execute ```puppet agent -t --no-noop``` on a node.
  - Via PE-Console, in the Run Puppet section, manage manually the remote execution of a no-noop Puppet run by clicking on the "Override noop = true configuration".

Remember that in both these last two cases, if noop is set server side Puppet keeps on skipping changes on the managed node, that's why we suggest to use server side noop mode only to add a safe net when deploying massive, critical or potentially dangerous code and data changes.
In normal operations is probably better to use client side noop mode that can be more easily overridden.

Alessandro Franceschi
