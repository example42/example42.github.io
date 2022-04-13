---
layout: blog
title: Puppet is acquired and example42 goes back to the roots
---

On April 11th, 2022 Puppet's CEO Yvonne Wassenaar [announced](https://puppet.com/blog/an-open-letter-from-the-ceo-of-puppet){:target="_blank"} the acquisition from Perforce.

Interesting and, for me, unexpected news. Only time will tell us how much this is going to impact Puppet's product and the nature of its community.

### Do we still need Puppet?

In these times where serverless, containers, and cloud based services are trending tech friends ask me (given my barely concealed addiction for it) what's the future and the role of a tool like Puppet?

It was born to solve problems of the past, when people who had to manage their own servers, rather than relying on some cloud service, an hosted Kubernetes cluster or a bunch of "serverless" functions.

My answer is often on these lines:

What's the **average lifetime of the systems** you have to manage? (if you have systems to manage)

If it's more than few weeks, and the number of systems is more than a dozen, you NEED a tool like Puppet.

That's it. Plain and simple.

In a modern IT shop, especially when its scale is not minimal, you have to manage everything as code: versionable, reproducible, repeatable.

What kind of code do you need to (re)build your infrastructure?

Whatever the Yaml, HCL, Json files that allow you to describe and configure your IT world with whatever tool, you need something to put under version control. You need something that allows you to reproduce and possibly automate your setups and the configurations. Manual operations, eventually based on an hardly documented checklist of point and click operations or commands, are barely acceptable.

To some degree, the essential disaster recovery of a modern IT shop is a git repository from where you can rebuild everything.

So, back to the key question: what's the lifetime of the systems you have to manage?

I mean, **all** systems, not only the servers which provide your company's internal or public services (be they on-premise physical and virtual or cloud instances).

If you don't have own servers to deal with, do you have to install, configure and manage your client desktops?

How do you configure the development stations from where you manage your cloud services?

How do you ensure that security settings and selected programs are installed on the employees' laptop?

If anywhere in your company, there's a Linux, a Windows, or a MacOS system that lives more than a few weeks, then you need a configuration management tool.

And among the various ones around, trust my biased opinion, Puppet is still the most complete, advanced, and scalable one.

It's also one of the hardest to learn, but for this you can rely on old sysadmins like me and the plenty of documentation around.


### Getting personal

I started to use Puppet around June 2008.

I had just started to work in the national Bank of Italy, as freelance System Administrator, when a colleague came back from an IT conference with exciting infos on this new tool which could help us configuring the hundreds of servers we had to manage.

We were already doing some kind of configuration management, using a somehow genial but cumbersome method based on configuration rpm packages.

I remember my initial reluctance in replacing the existing approach, which I just had started to master, with this new tool.

The typical sysadmin resistance to what's new and may disrupt his/her dream of stable and untouchable systems and established habits.

We started with version 0.21, if my memories don't fail me, and as soon as I began to understand its principles, I could not prevent myself from loving it.

A year later I was already [publishing](https://github.com/example42/control-repo-archive/commit/9490bbd7123a5bfe72fe11d26023b5b45f0a3b49){:target="_blank"} my first set of Puppet modules (yes, that's embarrassing code now), following the steps of David Schmitt's modules collection, with the ambition of doing modules with a standard naming structure, multi OS support and integrated monitoring, auditing, documentation and firewalling.

At the times I called this bunch of Puppet code "Lab42 Puppet Infrastructure". The Forge was still far from being even an idea.


### The first PuppetCamp

In 2009 I also attended the first PuppetCamp ever, held in San Francisco. It has been a blast. I thought to be a Puppet expert, I found out I had so many things to learn and fields to explore. It has been by far the most useful and enlightening IT conference I've ever been at.

I've vivid and wonderful memories of that event, from the visit at Google's headquarters, thanks to Nigel Kersten, who was working there at the times:

![Google First rack](/img/posts/google.jpg){:height="50%" width="50%"}

To the tours around San Francisco with new friends and Puppet legends like Ohad Levy (he presented The Foreman there), Brice Figureau (the wizard behind exported resources, puppet device and a lot of other community code) and Dan Bode (he has been one of the first employees hired by Luke right before the event):

![San Francisco](/img/posts/sf.jpg){:height="50%" width="50%"}

Since those times I had this obsession about modules standards which never really faded, here's me suggesting a round table about the topic:

![PuppetCamp](/img/posts/puppetcamp.jpg)


### example42 modules

Since that first event I attended almost every major Puppet conference, actually all the times I've been in USA has been for a Puppet event.

I owe to Luke Kanies and Puppet a good half of my IT career: since those first years I never stopped to work with Puppet, writing modules, delivering training and consulting all over the world, either for direct customers or as Puppet Partner.

I passed 10 years traveling almost every week, taking an airplane to flight to destinations in Europe, and occasionally Middle East and even Australia and Singapore.

The Lab42 Puppet infrastructure was renamed to example42, under this name over the years I developed various Puppet related projects:

- [Puppi](https://github.com/example42/puppi){:target="_blank"} a module which integrates with the first generation of example42 Puppet modules (featuring standard naming, saner MultiOS support and decommissioning of resources) to provide the ability to test from the command line what a module was managing and provide defines and commands to manage applications deployments
- The example42 "NextGen" modules set,  introduced in 2012, with the [params_lookup](https://github.com/example42/puppi/commit/12f2211a565495a6491e33388b1d893e43a3138b){:target="_blank"} function which somehow anticipates the concept of classes' automatic parameters lookup
- [Tiny Puppet](https://github.com/example42/puppet-tp){:target="_blank"}, a single module you can use to install and configure virtually every application on every OS. I like to consider it the most underrated Puppet module ever, but, again, I'm definitively biased here.
- A full featured control-repo (when the control-repo concept was introduced) which was then renamed to [PSICK](https://github.com/example42/psick){:target="_blank"} (Puppet Systems Infrastructure Construction Kit, any reference to SEUCK is not casual)
- The [psick module](https://github.com/example42/puppet-psick){:target="_blank"} a collection of reusable profiles and defines for common uses.

In many of these projects I break many official best practice rules and recommendations.

I can explain.

I've my reasons for many of such controversial choices and I'd do most of them again.

I developed most of example42 code by myself, but I don't forget and I am grateful for the PRs and fixes from other contributors.

It was nice at the times to learn about people and companies using my modules, and funny to see persons surprised to learn that example42 was just a person and not an organization with various developers.


### example42 GmbH

Actually, in 2015, example42 from a one man band became a company: example42 GmbH registered in Berlin, in collaboration with Martin Alfke.

We were both experienced Puppet freelance consultants and we decided to join forces. I wanted to preserve the example42 name, since it was known, for the good or the bad, in Puppet world, Martin had no objections to that.

My developments in Puppet code were reduced to simple maintenance activities on the existing projects, sacrificed on the altar of profit with the excuse of lack of time. 

Our business has grown well over the years, we worked with some of the biggest Puppet customers in Europe but even if our relationship was fine, the company has always had a dual nature, with the two of us working somehow in parallel without mutual interferences but also without a real common goal and direction.

Last year we decided to close the example42 GmbH company, and follow our own paths, as can read from [last blog post](https://blog.example42.com/2021/12/20/example42-gmbh-closes-business-on-31st-of-december-2021/){:target="_blank"}.


### And now?

So here we come to 2022, with the long tail of the pandemic and the terrible war news.

As for many other out there, I lived the last 2 years in a sort of suspended state, completely changing my habits (from one travel a week to endless hours in front of my home computers) and reconsidering priorities and life goals.

The example42 name and online assets came back to my full control, now I deliver all my Puppet related activities via my company in Italy, Lab42 Srl, keeping the example42 brand.

I brought to the extreme the flexibility I always grant to the customers I work with, some of the [services](https://example42.com/services/){:target="_blank"} I offer are really unique for the ways you can access, activate and use them: do you have a problem or something to do with Puppet? Send me a message, let's setup a conference call with shared screen and I can explain, guide, troubleshoot and work with you on your own Puppet setup.

Trust me, in most of the cases I can solve, or show how to solve, Puppet problems in a few minutes.

I like my work, I don't have working hours or days: I can pass full mid-week days playing video games or watching videos and nights or Sundays working on Puppet code or doing conference calls with people on other continents.

I'm not writing a lot of public code lately, and I'm not happy of that. I also would like to write some updated documentation and hints on Puppet (in the past I wrote a [book on Puppet](https://www.amazon.com/Extending-Puppet-Alessandro-Franceschi-ebook/dp/B00LA414JG){:target="_blank"} which was well received, but now it's definitely obsolete and there's so much to talk about newer Puppet topics and patterns).

Still it has been 3 months I'm not doing anything of the above, working only a fraction of my available time, without regrets.

Suspended, I said. Reconsidering the meaning of Life, the Universe and Everything.

I guess you can related.

The news about the acquisition has left me with mixed thoughts: I don't know if this will mean the end of Puppet as we know it or the beginning of a new shining era. Maybe both.

At least it has achieved one thing for me: it has enticed me to write this new blog post, the first one after closing the German company.

Given the times, it might be a beginning, or just another false start.

Alessandro Franceschi
