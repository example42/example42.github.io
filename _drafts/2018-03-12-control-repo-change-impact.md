---
layout: blog
title: Tip of the Week 63 - Puppet Control Repo change impact scenarios
---

A Puppet control-repo is usually the place where most of the Puppetteer activities are done.

This is especially true if we keep our Hieradata and local profiles in the control-repo git repository, rather than maintaining them in separated git repos, as external modules.

We always wonder (well, we should) what might be the impact of a change on the control repo on the managed infrastructure.

This might be an issue espectially for who is learning Puppet, Hiera and the local interactions.

Here we try to summarize the possible impacts on changes on different files, underlying that every mileage may vary and referred paths ultimately depend on how we structure our code and data in the control-repo.

We define 4 risk levels:

- [SAFE] Changes done here are totally safe in terms of impact on running servers (or generally any Puppet managed system)
- [LIMITED] Changes here impact a limited number of servers or not critical elements
- [WARNING] Changes may impact several servers and should be considered with care
- [DANGER] Changes may have a very large impact. Be sure to be aware of what we are doing

Let's review what level of risk may be associated to changes on the different control-repo files.

Needless to say that they refer to actual changes in Puppet code and data, if we are just adding commentef lines we can be confident that we change won't have any effect (unless we change a configuration file on a system which may trigger a service restart).

We assume to have hieradata in the ```data/``` directory and local profiles in ```site/profile/```.

- [SAFE] ```README.md```, ```docs/```, ```LICENSE``` or any other documentation or general information file. Changes done here won't have any impact on our servers

- [DANGER] ```hiera.yaml``` is the Hiera configuration file for the environment, changes here on the hierarchy or the used backends may affect several systems in more or less unpredictable ways. We should edit it only if we know what we are doing. In case of backend changes or big refactors, server side enforced noop mode is highly recommended.

- [DANGER] ```data/common.yaml```, ```data/defaults.yaml``` or any file that contain Hiera data which is used for all the nodes (when not overridden in more specific layers of the hierarchy), so any change here may impact several servers. Be aware.

- [WARNING] ```data/role/$role.yaml```, ```data/zone/$zone.yaml```, ```data/env/$env.yaml``` contains Hiera data which is used for a more or less large group of nodes. The actual path names depends on how is our hierarchy. It's recommended here to test at least one node belonging to the affected group, before promoting the change.

- [LIMITED] ```data/nodes/``` contains Hiera data for specific nodes (again, the actual path may change according to the hierarchy, but there always should be one level matching each node certname. Here we can place nodes specific settings, which are easy to test (directly on the involved node) and have a limited impact (only the node having the name of the file we change).

- [DANGER] ```manifests/site.pp``` or any other manifest here may impact all the nodes. Handle with care.

- [WARNING] ```Puppetfile``` contains the list of the modules to add to the control-repo. If we add a new module we won't have any effect on nodes until we actually start to use its classes or defines. If we remove a module we'll break Puppet runs in all the nodes that eventually use it. When we add or remove modules, we may see on our nodes files changing at the first Puppet run: these are due the contents of module's plugins being synced to the clients (pluginsync feature) they are normal and won't affect our servers operations. When we change versions of the used modules, we might impact exiting nodes. Versions changes for the used modules should always be tested on each managed OS.

- [WARNING] ```.gitlab-ci.yml```, ```Jenkinsfile```, ```.travis.yml``` define, according to the used tool, how is the CI pipeline to test our code, changing these files, or eventual CI commands used in CI on directories like ```bin/``` or ```scripts/``` may break our CI (and that's something that should always have the highest priority for fixing).

- [WARNING] ```site/profile/*``` here may stay local profiles, templates, files, facts, resource types, data types. Changes to our profiles in  ```site/profile/manifests``` impact all the nodes which classifies them. Changes to ```site/profile/files``` or ```site/profile/templates``` may actually change the contents of configuration files on our managed systems.

We shoudl not be too much worried about the above dangers and warnings, though, it's normal in the life of Puppet admin to edit such files.

We have just be aware of the potential impact area of our change and, when we are not fully confident on what we are doing, we should always check our changes in noop mode before actually enforcing them.

Alessandro Franceschi
