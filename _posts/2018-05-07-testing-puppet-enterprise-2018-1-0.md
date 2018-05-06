---
layout: blog
title: Tip of the Week 71 - Testing Puppet Enterprise 2018.1
---

A few days ago a new release of Puppet Enterprise (PE), the first of 2018, has been [published](https://puppet.com/blog/see-whats-new-puppet-enterprise-20181).

This is a LTS release which is going to be supported until 2020. The major improvements, compared to the previous release, are in the Tasks and Plans integrations, with improved Role Based Access Control to manage with more granularity what tasks can be run by each user.

One of the most valuable selling points of Puppet Enterprise have been the visualisation options that really give a meaning to the term "infrastructure awareness" (facts, reports, events, catalog graphs... there's really a lot of info to view on PE web interface), these have been coupled by the current management of Puppet Jobs and tasks, giving a single interface from where to control and monitor our infrastructure.

We can make tasks for any "one shot" action we may need to execute on one or more servers: from system upgrades to reboots, from applications deployments to database migrations. Doing tasks for these operations is trivial, we can even reuse our custom scripts, and have a single frontend from where to trigger such tasks, with a robust authorisation scheme, and complete overview of the result of their actions and the status of the infrastructure.

### Trying Puppet Enterprise

Puppet Enterprise can be downloaded and used for up to 10 nodes for free. This is enough to have an idea of how it works and eventually to manage very small shops. You can [download](https://puppet.com/download-puppet-enterprise) the packages for RedHat 6 or 7, SLES 12 or Ubuntu 16.04 from Puppet site (note: these are the only supported OS for the PE server components, the Puppet agent is available for many more OS.

You can also test it on the [Learning VM](https://puppet.com/download-learning-vm) or, if you have your infrastructure on AWS cloud you can also use try [Opsworks for Puppet Enterprise](https://aws.amazon.com/opsworks/puppetenterprise/).

### Testing local code on Puppet Enterprise with PSICK

You can finally test a fully operational Puppet Enterprise infrastructure under Vagrant (based on Virtualbox) using example42's [PSICK control-repo](https://github.com/example42/psick).

A single [commit](https://github.com/example42/psick/commit/9c77782ca5f06ebce8c2b79f7f2cc7b8ef6d4abb#diff-8cb16d894484dcb2c3bc465723063264R38) is what we needed to add support for it in one of the Vagrant environments available.

In order to test a PE infrastructure with PSICK on Vagrant you need:

- Puppet (you can install it with ```bin/puppet_install.sh```)

- The r10k and optionally hiera-eyaml and deep_merge Ruby gems

- Vagrant (you can install it with the needed plugins with ```bin/vagrant_setup.sh```). If you want to install the plugins manually just run:

        vagrant plugin install vagrant-vbguest
        vagrant plugin install vagrant-pe_build
        vagrant plugin install vagrant-hostmanager

- Virtualbox

These are the commands to run to setup locally a full featured control repo based on PSICK:

    git clone https://github.com/example42/psick
    cd psick
    r10k puppetfile install -v


    cd vagrant/environments/pe
    vagrant up puppet.pe.psick.io

This can take some time, if you don't have already locally the used Vagrant box.

There's a known issue, during first time provisioning: you will probably get an error like:

    Stderr from the command:
    bash: line 4: /vagrant/.pe_build/puppet-enterprise-2018.1.0-el-7-x86_64/puppet-enterprise-installer: No such file or directory

Don't worry, it happens only when you provision PE the first time. You just have to:

    vagrant reload puppet.pe.psick.io
    vagrant provision puppet.pe.psick.io

This will proceed with the installation of PE on the local VM, at its end you should be able to access PE web interface by browsing to https://127.0.0.1:1643 and login with user **admin** and password **puppetlabs** (you can ignore your browser warnings about insecure https connection: Puppet CA's self signed certificates are used).

The last command, after having installed Puppet Enterprise (thanks to the vagrant-pe_build plugin) triggers also a normal Puppet run on the node, using directly the contents of the PSICK control repo.

Once the command has ended you have a full configured PE server, which can serve the other nodes present in the same vagrant environment (they are configured in  ```vagrant/environments/pe/config.yaml```). Note that the PE Vm is not thin, by default we allocate 4GB of RAM to it (this can be configured too on the ```config.yaml``` file) and to this you have to add the memory used by each client VM: an host with at least 8, better 16GB, is recommended.

Now you can start other VMs from the same Vagrant environment, they will automatically connect and autosign to the PE server and apply their Puppet code and data:

    vagrant up pe-ubuntu1604.pe.psick.io

You can test directly the effect of the changes on the code and the data of your local PSICK based control repo.

For example edit the hiera file which configures the role **ostest** used by this node (this special role is used to test features on different OS):

    vi modules/hieradata/data/role/ostest.yaml

And set the following key to true:

    psick::base::manage: true

This particular parameter is used to skip the management of the base profiles (useful when we want to test only role specific classes or when building Docker images via Puppet). When set to true all the base classes are going to be effectively applied and several changes are going to occur on the node by running Puppet either via Vagrant:

    vagrant provision

or, even better, triggering Puppet runs on the selected nodes from the PE console, to apply your local changes on the active VMs (check the [PSICK module](https://github.com/example42/puppet-psick) classification features and general docs for more details on how to configure the psick module via Hiera)

When you decide to destroy one of the clients, that one will be automatically removed from PE server (freeing licence slots):

    vagrant destroy pe-ubuntu1604 docker.pe.psick.io

Note that PE based Vagrant environments are present also under ```vagrant/environments/lab``` (here with integration with GitLab for Puppet CI/CD) and ```vagrant/environments/demo```.

The purpose of these different Vagrant environments embedded in PSICK control repo is to let Puppet developers test locally their changes in Puppet code and hieradata in different conditions (with PE server, FOSS server, The Foreman, or in serverless mode using puppet apply) and on different Operating systems.

Have an unforgettable Puppet experience with Puppet Enterprise and PSICK!

Alessandro Franceschi
