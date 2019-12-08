---
layout: blog
title: Puppet Tip 110 - Request for Tiny Data - Part 4 - Defaults and final call
---

Post **four** of **four** about our Request for Tiny Data!

Previously we have:

- Part 1 - Introduced Tiny Puppet and where it can be used
- Part 2 - Described how to write Tiny Data
- Part 3 - Shown how to manage extra repositories and how to define an app upstream repo

Now let's add a few other info and raise the final call!

### Tiny Puppet defaults

Did we mention that Tiny Puppet is smart enough to do something also when it has no Tiny data for an application?

In this case it simply tries to declare a resource like:

    package { 'unknown_app':
      ensure => present,
    }

Automatically adding the right package provider, like **chocolatey** on Windows and **homebrew** on MacOS.

So, even if there's no tidy data for, example, **opera**, something like this would work for Linux, Windows and MacOS:

    tp::install { 'opera': }

When there's no tiny data anyway the `tp::conf` define can't be used.

### tp command line

One of the free side benefits of using Tiny Puppet is that optionally you can install the **tp shell command** (powershell version still not available) to interact with the apps you manage, and have at disposal commands as the following.

To just test that everything is fine:

    tp test

To test a specific app (can be used in shell sessions, CI, monitoring, puppet tasks, motd... )

    tp test gitlab-ce

To `tail -f` all the known logs of the apps managed with tp:

    tp logs

To limit to the logs of an application

    tp logs nginx

To quickly install an application caring of repositories

    tp install elasticsearch

To actually list the applications for which is available tiny data (based on latest version of [the module on the forge](https://forge.puppet.com/example42/tinydata){:target="_blank"}):

    tp list

## Request for Tiny Data!

So, here is our renovated **call for tiny data**.

We have tinydata for *some* applications:

    ls -la data/ | wc -l
      179

the common ones or what we needed or found interesting.

Still there's more.

A lot of wonderful applications that would be great to be able to install on a shell command:

    tp install wonderapp

or manage with a Puppet define:

    tp::install { 'wonderapp': }

On any Linux, and maybe Mac and Windows.

With the quick choice of using the default OS packages, the app upstream repo or any other repo might be configured.

    tp::install { 'wonderapp': 
      upstream_repo => true|false,
    }

We know we can add new data very easily, and relatively quickly.

We don't know what application interests you.

Please engage with, in effort order:

- **Let us know**, in any way (tweet, comment, mail, voice) **what app** you would like to quickly manage via tp
- **Open a [ticket on Github](https://github.com/example42/tinydata/issues){:target="_blank"}** for a **new app** support. Possibly provide context and relevant information
- **Open a [ticket](https://github.com/example42/tinydata/issues){:target="_blank"}** for **incorrect, incomplete or not updated** existing tiny data
- **Do directly the work** with updated tinydata and submit a **[Pull Request](https://github.com/example42/tinydata/pulls){:target="_blank"}**

Our goal is to `tp install everything` on any OS.

Now **let's define everything** together.
