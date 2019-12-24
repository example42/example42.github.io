---
layout: blog
title: Puppet Tip 111 - HDM released!
---

Merry christmas to everybody.

We are super excited to announce today the general availability of HDM (Hiera Data Manager) - a webfrontend for vizualising and managing Hiera data.

* Table of content
{:toc}

### HDM

We learned from several customers, that most of them have specifc requirements when it comes to managing application data.

Data must be able to be modified by a person which:
- has no knowledge on Git
- has no knowledge on Puppet
- only runs Windows on Workstation

Therefore we decided to develop HDM.

HDM starts with letting you select a desired environment where you want to check or change data.

![select environment](/img/hdm/02_HDM_env.png)

Next you can select a node. We query PuppetDB to find existing environments, nodes and their facter values:

![select node](/img/hdm/03_HDM_node.png)

Now you can see all hiera keys a node has within the environment hiera data:

![hiera keys](/img/hdm/04_HDM_node_data.png)

When selecting a key we show the hierachies and vizualize whether a hierarchy has data for a key and which one is the default:

![hiera data](/img/hdm/05_HDM_node_data_view.png)

You can now change data on node level.
HDM writes the data back to a file.

#### Requirements

In the actual state, HDM must run on the Puppet Master.
We fetch environments, nodelist and facts from PuppetDB.

HDM needs a file structure where it con store modified data.
This file structure must be added to your `hiera.yaml` configuration file.

#### Upcoming features

Within the next releases we want to:
- add read-only feature
- provide a Puppet module to install, configure and run HDM
- optimize the web view
- have HDM run on a separate machine
- run HDM as a container


### Coming soon: HDM Pro

The Open Source implementation has no login and no access control.
This is a feature we are putting into HDM Pro, our commercial release of HDM.

Another planned HDM Pro features is a git based storage backend with review capabilities.

### Community

We are looking forward to learn about [issues, missing features or any other feedback](https://github.com/example42/hdm/issues/).

Best,
the team of example42.

