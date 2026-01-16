---
layout: blog
title: Announcing Pabawi, a web frontend for classic infrastructures
---

Is there still space in AI and Cloud native days for a new tool to manage classic infrastructures based on physical or virtual servers?

If you handle good old servers, and use Puppet, Bolt or Ansible to configure and manage them, then the answer might be yes, and we may have a nice tool for you.

**Pabawi** is a new, modern, sleek web frontend to inventory your systems, check their configuration management status, and run actions on them.

Needless to sat that it's also Open Source.

Version 0.4.0, just released after a few weeks of AI based coding, has integrations with Bolt, Hiera, PuppetDB and PuppetServer.

Current version is expected to be executed by a Puppet developer or user on her/his localhost, featuring:

- **Multi-Source Inventory**: View and manage nodes from Bolt inventory and PuppetDB
- **Command Execution**: Run ad-hoc commands on remote nodes with whitelist security
- **Task Execution**: Execute Bolt tasks with automatic parameter support
- **Puppet Integration**: Trigger Puppet agent runs with full configuration control
- **Package Management**: Install and manage packages across your infrastructure
- **Execution History**: Track all operations with detailed results and re-execution capability
- **Dynamic Inventory**: Automatically discover nodes from PuppetDB
- **Node Facts**: View comprehensive system information from Puppet agents
- **Puppet Reports**: Browse detailed Puppet run reports with metrics and resource changes
- **Catalog Inspection**: Examine compiled Puppet catalogs and resource relationships
- **Event Tracking**: Monitor individual resource changes and failures over time
- **PQL Queries**: Filter nodes using PuppetDB Query Language
- **Hiera Data Browser**: Explore hierarchical configuration data and key usage analysis
- **Puppet code analysis**: Analyses Puppet code base, reporting class usage, lint issues, outdated modules in Puppetfile


More robust users management and RBAC, and Ansible and other tools integrations are planned for future versions.

Check the [git repository](https://github.com/example42/pabawi.git) for installation instructions and details.

## Screenshots

Here are some screenshots, from a test setup with few nodes. The interface adapts well and is still fast on way larger setups (currently tested with infrastructures up to 350 nodes).

### Nodes Inventory

![Inventory Page](/img/posts/screenshots/inventory.png){:height="50%" width="50%"}

*Node inventory with multi-source support, blazing fast search and filtering options*

### Task Execution

![Task Execution](/img/posts/screenshots/task-execution.png){:height="50%" width="50%"}

*Bolt task execution interface with automatic parameters discovery*

### Executions Tracking

![Executions List](/img/posts/screenshots/executions-list.png){:height="50%" width="50%"}

*Execution history with filtering and detailed execution results with re-run capabilities*

### Node Details

![Node Detail](/img/posts/screenshots/node-detail-page.png){:height="50%" width="50%"}

*Node detail page with access to facts, reports, events, managed resources and other useful info*

### Puppet reports

![Node Detail](/img/posts/screenshots/puppet-reports.png){:height="50%" width="50%"}

*Puppet reports view, with run times and number of affected resources*


## Free installation service (time limited)

Pabawi is easy to integrate in your existing Puppet / Bolt infrastructure and has contextual setup instructions for each integration, but if you want help in trying it in your infrastructure, example42 offers a launch special, time limited, **free installation service**, no strings attached.

In a shared screen call we can setup Pabawi together, either using its container image or via npm.

We want to test and validate it in different conditions, collecting users' feedback and suggestions.

Just contact me on [LinkedIN](https://www.linkedin.com/in/alessandrofranceschi/) for planning a call: half an hour should be enough to set it up and see how it works.

Alessandro Franceschi
