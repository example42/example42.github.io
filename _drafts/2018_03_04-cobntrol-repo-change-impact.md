---
layout: blog
title: Tip of the Week 62 - Control Repo change impact
---

A Puppet control-repo is typically the place where most of the Puppetteer development activitiers are done.

This is especially true if we keep our Hieradata and local profiles in the control-repo git repository, rather than maintaining them in separated git repos.

It often happens, especially to who doesn't know well the underlying logic and structure, to wonder what might be the impact of a change on the control repo on the managed infrastructure.

Here we try to summarize the possible impacts on changes on different files, underlying that our mileage may vary and ultimately depends on how we structure our control-repo files and Hiera's hierarchies.

We define 4 risks levels:

  - [safe] Changes done here are totally safe in terms of impact on running servers
  - [limited] Changes here impact a limited number of servers or not critical elements
  - [warning] Changes may impact several servers and should be considered with care
  - [danger] Changes may have a very large impact. Be sure to be aware of what we are doing

Let's review what level of risk may be associated to changes on different file. Needless to say that they refer to actual changes in Puppet code and data, if we are just adding a comment we can be confident that we change won't have any effect (unless we change a configuration file on a system which may trigger a service reload).

  - [safe] ```README.md```, ```docs/```, ```LICENSE``` or any other documentation or general information file. Changes done here won't have any impact on our servers

  - [danger] ```hiera.yaml``` is the Hiera configuration file for the environment, changes here (for in the hierarchy or the used backends) may affect several systems in more or less unpredictable ways. We should edit it only if we know what we are doing and we should be especially careful when we refactor the lookuop hierarchy.

  - [danger] ```data/common.yaml```, ```data/defaults.yaml``` contain Hiera data which is used for all the nodes (when not overridden in more specific layers of the hierarchy), so any change here may impact several servers. Be aware.

  - [warning] ```data/role/```, ```data/zone/```, ```data/env/``` contains Hiera data which is used for a more or less large group of nodes. The actual directory names depends on how is our hierarhy. It's recommended here to test at least one node belonging to the affected group, before promoting the change.

  - [limited] ```data/nodes/``` contains Hiera data for specific nodes (again, the actual path may change according to the hierarchy, but there always should be one level matching each node certname. Here we can place nodes specific settings, which are easy to test (directly on the involved node) and have a limited impact (only the node having the name of the file we change).

  - [danger] ```manifests/``` files here impact all the nodes. Handle with care.

  - [warning] ```Puppetfile``` contains the list of the modules to add to the control-repo. If we add a new module we won't have any effect on nodes until we actually start to use its classes or defines. If we remove a module we'll break Puppet runs in all the nodes that eventually use it. When we add or remove modules, we may see on our nodes files changing at the first Puppet run: these are due the contents of module's plugins being synced to the clients (pluginsync feature) they are normal and won't affect our servers operations. If we change versions of the used modules, especially major versions, if module follow Semantic Versioning, we might impact exiting nodes.

  - [warning] ```.gitlab-ci.yml```, ```Jenkinsfile```, ```.travis.yml``` define, according to the used tool, how is the CI pipeline to test our code, chaning these files may break our CI (and that's something that should always have the highest priority for fixing).

  - [warning] ```site/profile/*``` here may stay local profiles, templates, files, facts, resource types, data types. Changes to ```profile/manifests``` here may impact several or even all nodes. Changes to ```profile/files``` or ```profile/templates``` may actually change the contents of configuration files on our managed systems.

Don't be too much worried about the above dangers and warnings, though, it's normal in the life of Puppet admin to edit such files, just be aware of the potential impact area of our change and, always, do changes we are aware of and, when we are not fully sure of what we are doing, test our changes in noop mode before actually enforcing them.

Alessandro Franceschi
