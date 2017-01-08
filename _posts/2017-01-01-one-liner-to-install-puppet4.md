---
layout: blog
title: Tip of the Week [1] - One-liner to install Puppet 4
---

New year, new challenges. At example42 we continuously develop Puppet solutions but we seldomly take the occasion to talk about them.

We've decided, starting today, to publish every week a blog post with tips and infos about Puppet, DevOps, Automation and what we do with it.

Since the 31st of December 2016 Puppet 3 has reached its End Of Life, so we think it's a good occasion to begin the new year and our journey with how to install or upgrade Puppet 4.

If you want it on Linux you can follow the [official documentation](https://docs.puppet.com/puppet/latest/install_linux.html) or you can just run this command:

    wget -O - https://raw.githubusercontent.com/example42/control-repo/production/bin/puppet_install.sh | sudo bash

Or, if you are lazy:

    wget -O - https://bit.ly/installpuppet | sudo bash

The script automatically detects the underlying OS, **removes existing Puppet installations and repos**, installs the relevant, official, repositories for Puppet 4 and then installs the puppet-agent package.

It currently supports installation on Linux (RedHat and derivatives, Fedora, Suse, Debian, Ubuntu) and MacOS/Darwin. Check online reference for [installing Puppet on Windows](https://docs.puppet.com/puppet/latest/install_windows.html).

It runs totally unattended, so it can be used during automated provisioning of servers on public or private clouds.

If you don't like the idea of running as root scripts from the Internet, even worse via an url shortener, you are right and you already know what do do: download the script, analyze it, place it in a safe location and run it from there.

Or just fire the above one-liner and forget: it will work in the same way ;-)

Alessandro Franceschi
