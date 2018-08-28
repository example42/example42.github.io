---
layout: blog
title: Tip of the Week 87 - Puppet Library Module synchronization
---

Don't reinvent the wheel, use existing Puppet Modules to declare your infrastructure.
But how to keep them in sync with upstream?
How to proceed in case of urgent fixes required?
This weeks **Tip of the week** deals with upstream developed modules, how to store them in your local infrastructure, how to synchronize them and how to add urgent patches, without loosing upstream connectivity.

### Storing upstream modules

Using upstream modules in your control-repository is easy. You just add the wanted modules to your Puppetfile:

    mod 'example42/tp', :latest
    mod 'example42/tinydata', :latest
    mod 'puppetlabs/concat', '3.0.0' # postgresql requires concat < 3.0.0
    mod 'puppetlabs/stdlib', :latest
    mod 'puppetlabs/vcsrepo', :latest
    mod 'puppetlabs/firewall', :latest
    mod 'puppetlabs/aws', :latest
    mod 'jdowning/rbenv', :latest
    mod 'trlinkin/noop', :latest
    mod 'puppetlabs/catalog_preview', :latest
    mod 'puppet/archive', :latest
    mod 'puppetlabs/inifile', :latest

Now your heart of your infrastructure automation must access the internet and fetches modules from puppet forge.
How to proceed if you want to keep modules locally?

In general there are two options:

- use a private, local forge
- store modules in local git

#### Local forge

Running a local forge server is easy. You can use [unibet/forge_server](https://forge.puppet.com/unibet/forge_server). Other solutions are [Pulp](https://pulpproject.org/) or commercial artifacts systems like [JFrog Artifactory](https://jfrog.com/artifactory/) or [Sonatype Nexus](https://www.sonatype.com/nexus-repository-sonatype)

Major difference between unibet forge server and the other mentioned solutions is, that forge server does not act as proxy to the real forge server.
You just place the modules as tar.gz files into the forge server directory.

#### Local GIT

But how to proceed if you don't want to run a commercial artifacts platform or a forge server?
How can you easily and superfast fix issues in existing code?

In this case you want to place the upstream modules in your local git server.

Some enterprise Git solutions allow you to specify an upstream source when creating a new module. Some implementations will even sync periodically from upstream to your local Git repository.

You definitley want a regular sync from upstream to your local working copy.
Within your Puppetfile you refer to the synchronized upstream module by specifying the desired tag:

    mod 'puppetlabs/concat',
      :git => '<user>@<gitserver>:<path>/puppetlabs-concat.git',
      :ref => '3.0.0' # postgresql requires concat < 3.0.0

### Module synchronization

How do you get synchronization when using git?
First you create the repositories on your local Git server and clone them locally:

    git clone <your localgit url>/<path>/<repo>.git
    
    git clone git@gitserver/puppet7puppetlabs-concat.git

Now you switch into the empty directory and add a new remote:

    git remote add github https://github.com/puppetlabs/puppetlabs-concat.git

From the newly created remote with the name "github" we fetch all onjects and non-objects like taks and branches:

    git fetch --all
    git pull github master

Now we have identical code base compared to upstream. We now push all objects and non-objects to our local Git server:

    git push origin master --tags

Every time when you want to upgrade, you run the last three commands on each of your synchronized Git repositories.
Wait! Manual work, when we do automation? This does not feel good.

### Multiple module synchronization

When managing many repositories it becomes error prone and time consuming when doing this in a manual pattern.
Luckily there is help around:

- [repo](https://android.googlesource.com/tools/repo)
- [vcstool](https://github.com/dirk-thomas/vcstool)
- [rosinstall](https://github.com/vcstools/rosinstall)
- [python-vcs-repo-mgr](https://github.com/xolox/python-vcs-repo-mgr)
- [go-vcs](https://github.com/Masterminds/vcs)

The most simple one - from my point of view - is [myrepos](https://myrepos.branchable.com/) a Perl script from Joey Hess.

Within a configuration file we provide the list of modules which we want to manage additionally we provide commands which we want to execute. In the lib section we specify commands with parameters:

    # ~/git/.mrconfig
    [DEFAULT]

    checkout = git clone ssh://<user>@<git server>/<path>/$(basename $MR_REPO).git
    pull = git pull --rebase
    fetch = git fetch --all
    master = if [ $(git branch | grep master) ]; then git checkout master; git reset --hard ;git pull --rebase; fi
    prod = if [ $(git branch | grep production) ]; then git checkout production ;git reset --hard ;git pull --rebase; fi
    
    clean = rm -fr vendor .bundle spec/fixtures/modules
    
    remote_update = git checkout master; git fetch --all --prune; git pull github master; git push origin master --tags
    lib =
        remote () {
          git remote -v | grep $1 || git remote add github $1 || echo 'remote already added'
        }

    # Our control repository
    [puppet-control-repo]
    
    ## Upstream modules
    [puppetlabs-concat]
    remote = remote https://github.com/puppetlabs/puppetlabs-concat.git
    
    [puppetlabs-stdlib]
    remote = remote https://github.com/puppetlabs/puppetlabs-stdlib

    [puppetlabs-inifile]
    remote = remote https://github.com/puppetlabs/puppetlabs-inifile
    # ...

Now you can get your whole repository synced to your local machine with just one command: `mr checkout`.
When you return to work, you want to ensure that your local code is up to date. Run: `mr master` and `mr prod`.
To add the remote you run: `mr remote`. Nice side effect: everybody has the same remote set! No more checking which puppet-foo module you had taken initially.

To update the local Git server you run `mr remote_update`.

Best option is to have this process running via cron using an application user to push updates.

### Local patching and remote PR

But how to proceed if you encounter issues with released versions of a module?
Usually you want to create an issue on upstream location (github) and wait for someone to fix it.
Maybe you are even able to provide a PR for the issue.
Buth then you have to wait until upstream creates a new release.

In the menatime you can do the following to your local Git copy of the upstream module:

- create a local branch
- add changes to the branch, commit and push them locally
- within your puppetfile, switch to the branch name or the commit id

When upstream fixes the issue you just update your local module working copy and switch back to release tags.

Happy hacking,
Martin Alfke