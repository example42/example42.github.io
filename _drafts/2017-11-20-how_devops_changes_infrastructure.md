---
layout: blog
title: Tip of the Week 47 - DevOps - why and how?
---

# How DevOps started

In the past times system administrators mostly managed their infrastructure in a manual pattern: provisioning systems using USB sticks (if you were already lucky to have larger infrastructures you might have used a provisioning system like [FAI](https://fai-project.org/) or [Cobbler]((http://cobbler.github.io/)). Afterwards people logged into the system using SSH and configured them according to some documentation or tickets.

When developers changed from waterfall to agile methods, we as system administrators were facing new issues: we needed to build systems faster as developers were pushing out code faster.

That was the point where DevOps started. We learned that communication and collaboration with developers gave us insight on upcoming developmnent. As a nice side effect we were able to prevent having the need for hard to maintain systems already during development phase. We learned about developer methods and adopted them to our needs (e.g. using a version control system). On the other hand developers got an understanding of system engineers needs and frustrations.

This collaboration of developer sand system engineering is since then called `DevOps`.

But what does DevOps do? How does it work? What else did it change?

# What is DevOps?

Some companies still try to seel their 'DevOps products'. You can find evidence especially at enterprise level as one can see at the landing pages from [IBM](https://www.ibm.com/ibm/devops/us/en/products/) or [CA](https://www.ca.com/us/why-ca/devops.html). Others have understood that there are [no DevOps products](https://techbeacon.com/no-there-no-such-thing-devops-product) like the [Atlassian description of DevOps](https://www.atlassian.com/devops).

There already is a description on what DevOps is since 2010 when [Daemon Edwards](http://devopsdictionary.com/wiki/Damon_Edwards) and [John Willis](http://devopsdictionary.com/index.php?title=John_Willis&action=edit&redlink=1) gave a talk at DevOpsDays Mountain View. They describe DevOps using the [CAMS](http://devopsdictionary.com/wiki/CAMS)  acronym. These are:

- Culture
- Automation
- Measurement
- Sharing

Another summary of terms would be:
- People
- Processes
- Platforms and
- Participation

Automation and Measurement are the parts which you can easily make available to you and your teams by searching for products.
For [Configuration Management](https://en.wikipedia.org/wiki/Configuration_management) we can choose between tools like [Puppet](https://puppet.com/), [Chef](https://www.chef.io/chef/) or [Ansible](https://www.ansible.com/). All mentioned tools are aimed at teams managing IT infrastructures like servers, routers, storages and mostly use a declarative system description.

When it comes to metrics, we must first analyze which are the important information. Here we see different needs for different departments. IT Ops wants to see whether server usage is within normal limits, Product Owners want to see customer process and Management wants PKI to initial bonus payments.
When collaborating with the application developers it is easy to also fetch application specific data into a central metrics collection system like [Elasticsearch[(https://en.wikipedia.org/wiki/Elasticsearch) (formerly known as the ELK stack - Elastic, Logstash, Kibana) from [Elastic](https://www.elastic.co/webinars/introduction-elk-stack) or [Prometheus](https://prometheus.io/).

But how to implement 'Culture' and 'Sharing'? This is not something which you can just shop and 'buy' as this is people and not products or processes.

The most important task is to tear down any barrier which exists between developers and operations. Usually we see that these two departments are part of different C-Level stakeholders, especially at large companies: Development usually is located within Product, whereas Operation is handled within Technology. You will always fight battles between the CPO (Chief Product Officer) and the CTO (Chief Technology Officer). Both have different goals: the CPO wants new features and products to be available for customers as soon as possible, whereas the CTO sees a desire for stable platforms.
In this case the whole DevOps approach must be fully supported by the whole C-Level team.

The next barriers which build up are mid-level managers. Usually these are former technology people (either from development or operations) which have been given a team or even department lead. As team lead they are responsible to C-Level management for performance and results. Now these people have to adopt to a new role as team coach or leader. Their new main responsibility will be to remove any kind of issue their team has, they have to coach their staff to learn new technologies. This will take some time, as they first have to gain knowledge on how to fullfil the new role.

The above mentioned case is quite simple to solve for C-Level management: just get the right people and support them directly while your mod management is on training courses. Make the technicians a team which is directly under your control. If you haven't talked directly to your employees for a while you might want to change that now.

Ensure that you have smart people. Not the ones which are the loudest. Listen to the silent ones. Everybody in your team is your favorite player. Onlyworking as a team will bring you success in implementing DevOps.


# We don't need DevOps?

In the past few years we have seen plenty of tools and terms coming up within the DevOps area.
The one with the most momentum is [Docker](https://www.docker.com/). Docker allows you to easily build systems running as [Containers](https://en.wikipedia.org/wiki/LXC) but on multiple architectures and operating systems.

Some people even say that when using Docker there is no need to an IT operations team. An idea, which I don't share:
- who is responsible (technical experienced) contact to your Continer Plattform supplier?
- who is able to understand a decent way to manage containers and get important data from it?
- who will define and verify whether your container is created as a secure system?

Another term which is used often nowadays is [Serverless](https://en.wikipedia.org/wiki/Serverless_computing) which describes a way to run systems in cloud architecture. But serverless does not mean that you run a plattform without operations. It is just a wording saying that you run your platform on other company computers.
Even when using any kind of cloud you will have the need to manage (operate) your cloud access and configuration.

Both still require to have people with good knowledge on network, storage and application management around. The only difference is that we just don't have hardware in our own datacenter. The need for operations and therefor for collaboration between developers and system administrators is still there. So is the DevOps idea.


# The future of DevOps

As we are mostly within different customers, we see different stages of DevOps implementation. Some companies are already deep into DevOps whereas others are starting or evaluating DevOps principles.

Customers who do DevOps for quite some time already found, that they should not limit DevOps to developers and operation. They start to adopt the principles and ideas also to other departments, mostly loosely coupled to technology.
Within the past months several other implementations of DevOps already came up:
- SecOps - Collaboratoin of IT Security and Operations ans Development
- NetDev - Collaboration and automation between network engineers and other departments
- BizOps - Shared responsibility between product management or other business units and other teams

Even though that these re-use the DevOps naming conventions these enablements are not just a 1-1 correlation. The best term describing what we see as the future of DevOps might be something like: **SecNetDevBizOps**


Martin Alfke

