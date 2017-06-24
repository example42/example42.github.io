---
layout: blog
title: Tip of the Week 25 - The PSICK Developer Environment Setup - PDES
---

Working on Puppet code with least possible effort requires a properly setup of a suitable workstation environment.
Usually everybody starts playing around with different sets of utilities and tools, learning the hard way about the best usable setup.

This article will guide you to a setup, providing a proper basis for initially working with PSICK, Puppet or Ruby in general.

Puppet Development is based on Ruby.
The first thing we need is a Puppet recommended Ruby version.
As version can change from release to release, therefor we need some flexibility on Ruby versions being available.
Puppet provides a website with information on [Component versions in recent Puppet Enterprise releases](https://docs.puppet.com/pe/latest/overview_version_table.html).
More information regarding ruby development for Puppet is mentioned in the [System Requirements - Section Prerequisites](https://docs.puppet.com/puppet/4.10/system_requirements.html#prerequisites).

The usually preferred method uses Ruby in user space. This allows work without super user privileges.
There are two possible solutions:

 - [rvm](https://rvm.io)
 - [rbenv](https://github.com/rbenv/rbenv)
 
Within this posting we will use rbenv.

# System preparation

As we might need to install ruby from source, several development and application packages are required:

    # RedHat/CentOS:
    yum install -y git gcc make bzip2
    yum install -y openssl-devel readline-devel zlib-devel gcc-c++

    # Debian/Ubuntu:
    apt-get install -y git gcc make bzip2
    apt-get install -y libssl-dev libreadline-dev zlib1g-dev g++

On OS X and macOS Xcode installation is required. Then install the Command Line Tools:

    xcode-select --install

# Installation of rbenv

Installation of rbenv is done as a non-root user

First we clone the rbenv github repository:

    git clone https://github.com/rbenv/rbenv.git ~/.rbenv

Now we can compile shell extensions (this step is optional)

    cd ~/.rbenv && src/configure && make -C src

Now we add the rbenv executable path to our PATH environment variable:

    # RedHat/CentOS/OS X/macOS:
    echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bash_profile

    # Debian/Ubuntu:
    echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc

For the next step we need output from rbenv, which we will add to our shell:

    ~/.rbenv/bin/rbenv init

The output:

    # RedHat/CentOS/OS X/macOS:
    # Load rbenv automatically by appending
    # the following to ~/.bash_profile:

    eval "$(rbenv init -)"

    # Debian/Ubuntu:
    # Load rbenv automatically by appending
    # the following to ~/.bashrc:

    eval "$(rbenv init -)"

Follow the provided information and add the mentioned line to your shell environment.

Next we need to take care on possible ways to install ruby versions. This is not part of rbenv directly but placed into a separate repository which delivers an extension to rbenv: [ruby-build](https://github.com/rbenv/ruby-build)

Just run the following git command will place the code into proper location:

    git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build

Remeber to refresh your shell:

    exec bash

Verify functinality of rbenv:

    rbenv version

This should return the following output:

    system (set by /home/tuxmea/.rbenv/version)

# Install ruby versions

Puppet 4 uses Ruby 2.1.9, Puppet 5 uses Ruby 2.4.1

Install both ruby version by running the following command:

    rbenv install 2.1.9

Verify installation of new ruby version:

    $rbenv versions
      2.1.9

# Install ruby basic extensions

Now we activate the ruby version to install some basic ruby extensions which are required for further development:

    rbenv shell 2.1.9
    gem install bundler wirble pry
    rbenv shell --unset

Bundler is used to install ruby extensions required by some development into another path. This allows you to run development and testing even when there is version mismatch between some application you are working on.

Wirble is an irb (interactive ruby shell) extension which offers syntax highlighting and tab completion.

Pry is a ruby debugger. During development one can set breakpoints where pry will open an irb session within the running application.

Configuration for wirble irb extension is done in ~/.irbrc

    require 'rubygems'
    require 'wirble'
    Wirble.init
    Wirble.colorize

Wirble and pry are not required for Puppet testing, but recommended extensions for development of custom facts, functions, types or providers.

Repeat the steps mentioned above with ruby version 2.4.1 to be prepared for Puppet 5 code testing!

# GIT Prompt

As we are working on a GIT repository, it is highly recommended to have an informative shell prompt delivering information about your actual repository state.

For bash shells one wants to check [git bash prompt](https://github.com/magicmonty/bash-git-prompt), for zsh shells one might consider using [oh my zsh](http://ohmyz.sh/).

For git bash prompt the following steps are required:

    cd ~
    git clone https://github.com/magicmonty/bash-git-prompt.git .bash-git-prompt --depth=1

Now enable the git bash prompt in your shell:
    
    # RedHat/CentOS/OS X/macOS:
    cat <<- EOF >> ~/.bash_profile
    # git bash prompt
    GIT_PROMPT_ONLY_IN_REPO=1
    source ~/.bash-git-prompt/gitprompt.sh
    EOF

    # Debian/Ubuntu:
    cat << EOF >> ~/.bashrc
    # git bash prompt
    GIT_PROMPT_ONLY_IN_REPO=1
    source ~/.bash-git-prompt/gitprompt.sh
    EOF

Don't forget to reinitialize your shell ```exec bash```

# Start working on PSICK

Now clone the PSICK repository:

    git clone https://github.com/example42/psick.git

When changing into the psick directory the default ruby version is selected automatically by using content from .ruby-version file.
Additionally you will se the default branch at the shell prompt:

    [mea@puppet ~]$
    [mea@puppet ~]$ cd psick/
    ✔ ~/psick [production L|✔]


Now it is possible to install all ruby gems required for testing into a separate path:

    bundle install --path vendor

Next you can run tests. Tests are not yet complete but under development.

    # e.g.

    # get puppet version used for testing
    bundle exec puppet --version

    # list all rake tasks
    bundle exec rake -T

    # install modules from Puppetfile
    bundle exec r10k puppetfile install -v

Happy testing, developing and puppetizing.

Martin Alfke

