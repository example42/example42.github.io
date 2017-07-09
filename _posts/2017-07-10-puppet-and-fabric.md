---
layout: blog
title: Tip of the Week 27 - Puppet and Fabric
---

[Fabric](http://www.fabfile.org) is a remote execution tool, written in Python, which ease parallel execution and orchestration of commands on different nodes.

Why does it matter with Puppet?

Because it's a good candidate, and not a rare choice, to trigger Puppet runs (and more) from a central location.

In [PSICK](https://github.com/example42/psick), our Puppet control-repo [generator], we use it for several tasks tasks which are related to the whole Puppet code workflow, from development, to testing and deployment.

We can install Fabric, as common with Python software, using **pip**:

    pip install fabric

Once installed we have at disposal the **fab** executable, which reads a file called ```fabfile.py``` to get the list of available Fabric commands.

In PSICK we gathered different fab files for different purposes in a single [directory](https://github.com/example42/psick/tree/production/fabfile) give them a look for an idea of their format. Being written in Python they can have a much more complex and flexible content.

To list the available commands in the local fabfile (or directory) we can type:

    fab -l

Fabric commands can be executed locally on remote nodes. On remote nodes it uses SSH for connection. There are various ways to define the list of remote nodes where to execute a given command, the simplest one is probably to specify them directly in the command line with the ```-H``` argument followed by a comma separated list of nodes or using the ```:host``` argument:

    fab <task>[:host=<hostname>][:option=value]
    fab [-H <hostname>] <task>[:option=value]>

Note that there are other ways to define and group the nodes to work with, for example by using Fabric **roles**, refer to the [official documentation](http://docs.fabfile.org/en/1.13/usage/execution.html#defining-host-lists) for details.

Typically access to the remote node is done using SSH keys, using the local user for remote authentication, if keys are not used a password is prompted.

If local and remote users don't match, or access to a remote node can't be direct and requires a jump host, it's definitively worth adding the relevant nodes in our ```~/.ssh/config``` file, where we define for our nodes, the user to access them, the SSH key to use, eventually a jump host and so on. Syntax for SSH client file is something like:

    Host mon
        ProxyCommand ssh -A -x -W %h:%p bastion.aws.example.com 2> /dev/null
        ForwardAgent yes
        User ec2-user
        Hostname 10.10.2.160
        IdentityFile ~/.ssh/aws.pem

In this way we can connect to this host, with all the correct configurations, with ```ssh mon```, or, when using Fabric, ```fab -H mon```.


### Fabric on PSICK

We mentioned PSICK and its integration with Puppet, the list of available commands is not short:

    al@mule psick [development] $ fab -l
    Available commands:

        aws.apply                  [local] Run puppet apply locally using the specified role (default: aws)
        aws.setup                  [local] Install locally the aws cli environment
        aws.status                 [local] Show AWS resources on one or all regions
        docker.purge               [local] Clean up docker images and containers (CAUTION)
        docker.rocker_build_role   [local] WIP Rockerize a role on all or the specified image OS (data in hieradata/role/$puppetrole.yaml)
        docker.setup               [local] Install locally Docker (needs su privileges)
        docker.status              [local] Show Docker status info
        docker.test_role           [local] Test a role on the specified OS on a Docker image
        docker.tp_build_role       [local] Dockerize a role based on tp on all or the specified Docker (data in hieradata/role/$puppetrole.yaml)
        facter.set_external_facts  [remote] Set the given external facts in /etc/puppetlabs/facter/facts.d
        facter.set_trusted_facts   [remote] Set the given trusted facts in /etc/puppetlabs/puppet/csr_attributes.yaml
        git.checkout_master        [local] Run git checkout master on each on the installed modules
        git.install_hooks          [local] Install Puppet .git/hooks
        git.setup_new_repo         [local] Create a new repo from scratch, based on the current contents of this control-repo
        git.status                 [local] Run git status on this repo and the installed modules
        puppet.agent               [remote] Run puppet agent
        puppet.agent_noop          [remote] Run puppet agent in noop mode
        puppet.apply               [remote] Run puppet apply on the deployed control-repo (uses control-repo in the environments/production dir)
        puppet.apply_noop          [remote] Run puppet apply in noop mode (needs to have this control-repo deployed)
        puppet.check_syntax        [local] Check the syntax of all .pp .erb .yaml files in the contro-repo
        puppet.current_config      [remote] Show currently applied version of our Puppet code
        puppet.deploy_controlrepo  [remote] Deploy this control repo on a node (Puppet has to be already installed)
        puppet.install             [remote] Install Puppet 4 on a node (for Puppet official repos)
        puppet.lint                [local] Run puppet-lint on all site manifests. Eventually fix them
        puppet.module_generate     [local] Generate a Puppet module based on skeleton
        puppet.module_publish      [local] Publish on GitHub and the Forge the local version of a module
        puppet.remote_setup        [remote] Installs on a remote node the packages needed for a puppet apply run on the control-repo
        puppet.setup               [local] Setup the contro-repo, installs r10k and external modules
        puppet.sync_and_apply      [remote] Run puppet apply on a synced copy of the local git repo (syncs and uses control-repo in the environments/fabr...
        tp.clone_data              [local] Add a new app name data directory under modules/tinydata, based on the specified source
        tp.install                 [local] Install locally any tinydata knows app via tp
        tp.remote_test             [remote] WIP Run tp tests on remote node
        vagrant.destroy            [local] Destroy the specified vm
        vagrant.env_status         [local] Run vagrant status on all or the specified environments
        vagrant.halt               [local] Halt all or the specified Vagrant vm
        vagrant.node_test          [local] Run existing and testing Puppet code on a VM
        vagrant.provision          [local] Provision all or the specified vm
        vagrant.reload             [local] Reload all or the specified vm
        vagrant.resume             [local] Resume all or the specified vm
        vagrant.setup              [local] Install locally Vagrant and the needed plugins
        vagrant.status             [local] Show status of all or the specified vm
        vagrant.suspend            [local] Suspend all or the specified vm
        vagrant.up                 [local] Vagrant up the specified vm

Many of these commands are executed locally (and just wrap simple shell commands present in PSICK's ```bin/``` directory), but there are some intended to be used on remote nodes.

For example, to install Puppet on one or more remote nodes we can run:

    fab puppet.install -H host1,host2

To run puppet agent in noop mode on all the known hosts (as defined in fabiles, or in the environment):

    fab puppet.agent_noop

To run puppet agent on a specific node:

    fab puppet.agent -H web01.example.test

To run in apply mode the local code on a remote node (code is rsynced and then compiled on the remote node, eventual eyaml keys and first copied and then removed):.

    fab puppet.sync_and_apply


### Local Puppet activities with PSICK

Local commands are, generally, not ommon in Fabric, as the tools is supposed to be used for remote execution, still in PSICK there are several commands available to support us in our Puppet code workflow.

For example, to install useful git hooks for Puppet development. By default downloaded from (https://github.com/drwahl/puppet-git-hooks)[https://github.com/drwahl/puppet-git-hooks]:

    fab git.install_hooks

To generate a new module based on the format of PSICK's ```skeleton``` directory.

    fab puppet.module_generate

To check the git status of the main control-repo and of each module in ```modules```:

    fab git.status

To check the syntax of all .pp .yaml .epp .erb files in our control-repo:

    fab puppet.check_syntax

To publish the local version of a module in modules/ dir to Forge and GitHub (puppet-blacksmith setup and access to remote git repo required):

    fab puppet.module_publish:<module_name>

To test a role (as defined in ```hieradata/role/$role.yaml```) with Docker on different OS base images:

    fab docker.test_role:<role>,<image>
    fab docker.test_role:log,ubuntu-14.04

Available images are: ubuntu-12.04, ubuntu-14.04, ubuntu-14.06, centos-7, debian-7, debian-8, alpine-3.3.

These are just examples, give a look to the list of available commands for more, and use the ```-d``` argument to show a list of available  arguments:

    al@mule psick [development] $ fab -d docker.test_role
    Displaying detailed information for task 'docker.test_role':

        [local] Test a role on the specified OS on a Docker image
        Arguments: puppetrole='docker_test_role', image='centos-7'

The fabfiles on PSICK are rather basic, but much more can be do, list of nodes can be automatically queried to AWS or PuppetDB, commands can be the result of more or less Python code, which may trigger remote backups, check for systems status, perform database operations, applications deployment and so on.

So, even if not strictly necessary (not even in PSICK), Fabric can be a good companion to Puppet and generally to the whole operations.

It's usage inside a control-repo may give to it a whole new meaning, which goes further than a "simple" central repository for Puppet code and data, and may become the single place from where the whole infrastructure can be provisioned, configured, controlled, and managed.

The limit is our imagination.

Alessandro Franceschi
