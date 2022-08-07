---
layout: blog
title: HashiConf Europe 2022 - Vibes from a perfect conference
---

IT conferences are main attractions in our jobs with machines, the occasions to meet again remote friends you've known for years, know people with whom you have something in common and stay updated on vendors' products.

After the last two years I guess many of us are looking forward to attend some good in presence conference, hence my decision to plan a road trip, from Italy to Amsterdam, take the occasion to meet business partners, old friends and, first time for me, jump into an HashiCorp conference.


### How tp always matters

I didn't came to the party without anything, I took the occasion to demonstrate how easily you can install any other Hashcorp application (as actually, every other application) with Tiny Puppet:
"Example42's coolest and most underrated module ever".
My opinion.

Quick recap, if you have Puppet installed, even without any agent runner, you can install on your local OS (RedHat/Debian/Suse/MacOs/Windows...) the Tiny Puppet module with:

    puppet module install example42/tp

Then you can setup Tiny Puppet (practically creating the local tp cli command) with:

    puppet tp setup

Now you have the tp cli command which can be used for different tasks.

You can install literally every application, so also the HashiCorp tools, with:

    tp install terraform
    tp install vault
    tp install packer
    tp install vagrant
    tp install consul
    tp install nomad ...

You can test if the above apps are correctly installed with:

    tp test

You can tail continuously all the system logs of the ones of a specific app with (CTRL+C to exit):

    tp log
    tp log consul

You can collect live info on the system and single apps with: 

    tp info
    tp info packer

This is possible on every common OS, you don't have to remember names or paths. Tiny Puppet, and Puppet under the hoods, takes care of everything (as long as there's tinydata for a specific application).

That's only the surface of what you can do with Tiny Puppet, which is not only a cli command but also a Puppet module you can use in your profiles to manage quickly and in a cross OS compliant way the applications you need to configure.

It also provides tasks, that perform the above actions remotely. A tp::test task run globally gives you instant health stats pf all your apps on all your systems, for example.


### Vibes of a conference

Enough about tp, let's dwell into HashiCrop Europe 2022, held in Amsterdam, in the same lovely location of earlier editions.

Here we found an almost unique combination of different factors:

- An Open Source based company with a cool lineup of products
- A great conference location, near a gorgeous park and not far from center
- Perfect weather, sunny but not hot.
- Intriguing ambiance and background music
- Perfect organization and plenty of food and beverages
- That Amsterdam special feeling 

I guess words don't make much sense or add a lot, so I hope the following videos can given an idea of the general location and environment.

This is the main room at the beginning of the conference:

<iframe width="560" height="315" src="https://www.youtube.com/embed/3zchzz96t1Q" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

A walk around during Day 2 Keynote, spaces organisation was good, with this main room used only for keynote all the resting, demo, food areas.

<iframe width="560" height="315" src="https://www.youtube.com/embed/BZbQh0rIVuk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


<iframe width="560" height="315" src="https://www.youtube.com/embed/CpbTVZRjgTQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Hope that these videos, better than many words, can give you an idea of how HashiConf Europe 2022 has been, which I guess is better than nothing.


Alessandro Franceschi
