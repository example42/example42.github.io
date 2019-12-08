---
layout: blog
title: Puppet Tip 110 - Request for Tiny Data - Part 4
---

Part Four of the Four parts blog serie on our Request for Tiny Data.

Previously we have:

- Part 1 - Introduced Tiny Puppet and where it can be used
- Part 2 - Described how to write Tiny Data
- Part 3 - Show how to manage extra repositories and how to define an app upstream repo

### Tiny Puppet defaults

Did we mention that Tiny Puppet is smart enough to do something also when it has no Tiny data for an application?

In this case it simply tries to declare a resource like:

    packake { 'unknown_app':
      ensure => present,
    }

Automatically adding the right package provider,, like **chocolatey** on Windows and **homebrew** on MacOS.

So, even if there's no tidy data for opera, something like this works on any OS:

    tp::install { 'opera': }

When there's no tiny data anyway the `tp::conf` define can't be used.

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
