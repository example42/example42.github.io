---
layout: blog
title: Puppet Tip 117 - Managing extra repositories Tiny Puppet 
---

I've written recently a post about Tiny Puppet, which is a recommended reading if you want to understand some of its internals.

Now, here, I want to talk about how you can use it to manage interesting and juicy extra packages repositories with it.

I suppose everybody who works with RedHat Linux or derivatives is well aware of EPEL, a collection of packages, totally compatible with the default set of packages, shipped with RedHat Enterprise Linux (and derivatives like CentOS, Oracle Linux and Scientific Linux).

Now on Puppet Forge there are [various modules](https://forge.puppet.com/modules?q=epel) you can use to install the Epel repository, but why adding another module to your Puppetfile (with eventual dependencies), when you can EPEL using Tiny Puppet simply by adding in your profiles:

    tp::install { 'epel': }

And why limiting ourselves to EPEL, when with the single Tiny Puppet module and its TinyData companion you can add several other repos?

What Repos? Let see them, note that Tiny Puppet installs them using the best approach possible, which in most of the cases means installing the relevant **release package** which takes care of configuring yum repo files, GPG keys and whatever is needed to add the repository to the system.

## RedHat based repositories

As of writing we currently support on Tiny Puppet, for RedHat and derivatives versions 6, 7 and 8 (where supported) the following additional repositories:

- [Epel](https://fedoraproject.org/wiki/EPEL). The Big Brother of them all. The most used and supported, with more than 5000 extra packages a yum install away. As we have seen, to install it, as we anticipated, just add in a class used by your node the following Puppet code:

        tp::install { 'epel': }

alternatively, if you have the class tp included in your nodes, you can install it via Hiera:

        tp::install_hash:
          epel:
            ensure: present

finally, if you prefer to use Tiny Puppet from the command line (install it with: `puppet module install example42-tp ; puppet tp setup`), as root, on your favourite shell, you can simply type:

        tp install epel

The above options are available for all the other repos (and applications) that Tiny Puppet can install

- [RPM Fusion](https://rpmfusion.org/), is another *historic* repo of extra packages, result of the merger of older repos (Dribble, Freshrpms and Livna, for who remembers them ;-) it provides both free and non free (like Nvidia drivers) packages for RedHat (and derivatives) 6, 7 and 8 and keeps compatibility with EPEL:

        tp::install { 'rpmfusion-free': }
        tp::install { 'rpmfusion-nonfree': }

- [IUS](https://ius.io/), which stays for *Inline with Upstream Stable*, provides updated packages of common applications, packages in a way to be compatible with RedHat native rpms. As of writing supports RedHat (and derivatives) 6 and 7:

        tp::install { 'ius': }

- [Remi Repository](https://rpms.remirepo.net/), a repo which adds to EPEL's packages several (more than 2000) other packages, particularly oriented to different versions of PHP, for RedHat (and derivatives) 6, 7 and 8:

        tp::install { 'remi': }

- [ELRepo](http://elrepo.org/tiki/) focuses on hardware related packages for enterprise usage it supports RedHat (and derivatives) 6, 7 and 8:

        tp::install { 'elrepo': }

- [Nux DexTop](http://li.nux.ro/repos.html) provides multimedia and desktop oriented packages for RedHat (and derivatives) 6 and 7:

        tp::install { 'nux': }

- [Ulyaoth](https://community.ulyaoth.com/resources/categories/repository.1/), a repo with different versions of Tomcat and Solr packages for RedHat (and derivatives) 7 and 8:

        tp::install { 'ulyaoth': }

That's it, managing repositories (via the `tp::repo` define) is just a side effect of Tiny Puppet, and all this comes, as usual, with just *one module that installs everything*.


Alessandro Franceschi
