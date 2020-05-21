---
layout: blog
title: Puppet Tip 117 - Managing extra repositories with Tiny Puppet 
---

I've written recently a [post about Tiny Puppet](https://www.example42.com/2020/04/20/five-years-of-tiny-puppet/){:target="_blank"}, which is a recommended reading if you want to understand some of its internals.

Now, here, I want to talk about how you can use it to manage interesting and juicy extra packages repositories with it.

* Table of content
{:toc}

## Managing packages repositories with Tiny Puppet

I suppose everybody who works with RedHat Linux or derivatives is well aware of EPEL, a collection of packages, totally compatible with the default set of packages, shipped with RedHat Enterprise Linux (and derivatives like CentOS, Oracle Linux and Scientific Linux).

Now on Puppet Forge there are [various modules](https://forge.puppet.com/modules?q=epel){:target="_blank"} you can use to install the Epel repository, but why adding another module to your Puppetfile (with eventual dependencies), when you can install EPEL using Tiny Puppet simply by adding in your profiles:

    tp::install { 'epel': }

And why limiting ourselves to EPEL, when with the single Tiny Puppet module and its [TinyData](https://github.com/example42/tinydata){:target="_blank"} companion you can add several other repos?

What Repos? Let see them, note that Tiny Puppet installs them using the best approach possible, which in most of the cases means installing the relevant **release package** which takes care of configuring yum repo files, GPG keys and whatever is needed to add the repository to the system, but when a release package is not available the yum or apt configuration files, and eventual GPG keys are directly managed.

This is transparent to the user and it all depends on the available Tiny Data.

## RedHat based repositories

As of writing we currently support on Tiny Puppet, for RedHat and derivatives versions 6, 7 and 8 (where supported) the following additional repositories:

- [Epel](https://fedoraproject.org/wiki/EPEL){:target="_blank"}. The Big Brother of them all. The most used and supported, with more than 5000 extra packages a yum install away. As we have seen, to install it, as we anticipated, just add in a class used by your node the following Puppet code:

        tp::install { 'epel': }

  alternatively, if you have the class tp included in your nodes, you can install it via Hiera:

        tp::install_hash:
          epel:
            ensure: present

  finally, if you prefer to use Tiny Puppet from the command line (install it with: `puppet module install example42-tp ; puppet tp setup`), as root, on your favorite shell, you can simply type:

        tp install epel

The above options are available for all the other repos (and applications) that Tiny Puppet can install, so we will not repeat them in the examples below.

- [RPM Fusion](https://rpmfusion.org/){:target="_blank"}, is another *historic* repo of extra packages, result of the merger of older repos (Dribble, Freshrpms and Livna, for who remembers them ;-) it provides both free and non free (like Nvidia drivers) packages for RedHat (and derivatives) 6, 7 and 8 and keeps compatibility with EPEL:

        tp::install { 'rpmfusion-free': }
        tp::install { 'rpmfusion-nonfree': }

Note, in the [git commit](https://github.com/example42/tinydata/commit/fd5ebc15b4735d30cc11438d6e8bf02017d7b0d9){:target="_blank"} where RPM Fusion Tiny Data has been added, how we manage the needed dnf or subscription-manager commands on RedHat 8.

- [IUS](https://ius.io/){:target="_blank"}, which stays for *Inline with Upstream Stable*, provides updated packages of common applications, packages in a way to be compatible with RedHat native rpms. As of writing supports RedHat (and derivatives) 6 and 7:

        tp::install { 'ius': }

The relevant [commit](https://github.com/example42/tinydata/commit/5f14cd7e5dea56d98e2e8df446d26adc5a4b7aea){:target="_blank"} shows how easily a new repo like this one could be added.

- [Remi Repository](https://rpms.remirepo.net/){:target="_blank"}, a repo which adds to EPEL's packages several (more than 2000) other packages, particularly oriented to different versions of PHP, for RedHat (and derivatives) 6, 7 and 8:

        tp::install { 'remi': }

Also here, [one commit](https://github.com/example42/tinydata/commit/3d7ed6acd50a71423ab6467bafd9658508326723){:target="_blank"}, one repo support added (and no extra module needed ;-)

- [ELRepo](http://elrepo.org/tiki/){:target="_blank"} focuses on hardware related packages for enterprise usage it supports RedHat (and derivatives) 6, 7 and 8:

        tp::install { 'elrepo': }

Another [simple commit](https://github.com/example42/tinydata/commit/95004e77cac0fff82eba14fd0da5fd58012d4a18){:target="_blank"}.

- [Nux DexTop](http://li.nux.ro/repos.html){:target="_blank"} provides multimedia and desktop oriented packages for RedHat (and derivatives) 6 and 7:

        tp::install { 'nux': }

Introduced in a [too quick commit](https://github.com/example42/tinydata/commit/0cc1f6d04825636b4e82d6f0b6963630c907abd2){:target="_blank"} based on another repo, then [corrected](https://github.com/example42/tinydata/commit/5571dc311d82e0c170c29dd9d11146134ee4627c){:target="_blank"}.

- [Ulyaoth](https://community.ulyaoth.com/resources/categories/repository.1/){:target="_blank"}, a repo with different versions of Tomcat and Solr packages for RedHat (and derivatives) 7 and 8:

        tp::install { 'ulyaoth': }

Here just one release package is enough for all RedHat versions, as you can see in [this commit](https://github.com/example42/tinydata/commit/a29c59ed4789f855aa6ee4a416f557ba8c210055){:target="_blank"}.


## Ubuntu / Debian based repositories

At the moment there are no extra Debian or Ubuntu repositories added to Tiny Data as we couldn't find any interesting enough one which is not already added (or easy to activate) to the standard distros, or that is not related to a specific application (in such cases the repo is added to the application's Tiny Data).

In any case, if you have any interesting extra repo to suggest here, please let us know: adding it will be easy and quick.


## Adding custom repositories

Since Internet is a bad and dangerous place, many companies prefer to have internal repositories where packages are both mirrored from upstream sources and locally packaged.

Tiny Puppet can help here, and allow to handle any custom repository, either by using custom tinydata as in the above examples or by specifying directly the expected params when using the `tp::repo` define, which is declared inside  `tp::install` if repo related Tiny Data is present.

Let's see some examples. If you have a local release package, with all the configurations of your repos and gpg keys, you can install it with something like:

    tp::repo { 'my_repo':
      repo_package_url => 'https://my.internal/my_repo-release.rpm',
    }

If you have to configure a Yum Repository with these parameters (not all of them are needed):

    tp::repo { 'my_repo':
      repo_url         => "https://my.internal/yum/repos/my_repo-el-${::os['distro']['release']['full']}-\$basearch",
      key_url          => 'https://my.internal/my_repo-GPG-KEY',
      key              => '54A6 47F9 048D 5688 D7DA  2ABE 6A03 0B21 BA07 F4FB',
      yum_priority     => '5',
      repo_description => "My Internal Repo",
      yum_gpgcheck     => true,
    }

For a Zypper repo for SuSE:

    tp::repo { 'my_repo':
      zypper_repofile_url => 'https://my.internal/zypper/repos/my_repo.repo',
      repo_name           => 'my_repo',
    }

If you use an Apt repository you can have parameters as follows:

    tp::repo { 'my_repo':
      repo_url         => 'https://my.internal/apt/repos/my_repo/',
      key_url          => 'https://my.internal/my_repo-GPG-KEY',
      key              => '54A6 47F9 048D 5688 D7DA  2ABE 6A03 0B21 BA07 F4FB',
      apt_release      => $::os['distro']['codename'],
      aptrepo_title    => "My Internal Repo",
      apt_repos        => 'main',
      aptrepo_title    => 'my_repo', # Default is $title
    }

It might be a bit overkill to use `tp::repo` to manage internal repositories, but consider it as a side effect of Tiny Puppet, considering that all this comes, as usual, with just *one module that installs everything*.


Alessandro Franceschi
