---
layout: blog
title: Puppet consulting, the example42 way
---

If you think that this is a mere low budget marketing self-promoting post, you are right.

Still, if you are interested in Puppet consulting, or, for some really arcane reason, in example42, keep on reading, as I guarantee that everything is written here is true and happened for real.


## example42, an idea, an approach to work

Example42 started in 2008 as an Open Source project, then, in 2005, it became a company based in Berlin, and finally, at the beginning of this year it turned into a brand of Lab42 Srl, my company, based in Italy.

The idea behind example42 is to provide a set of Puppet modules, which are Open Source, and a set of services, which are not. (this sentence, exactly as is, was suggested by one of my editor's AIs, not sure exactly which one but I like it).

I guess from now on you can't tell anymore what is written by a human and what is not.

Let's say that the ramblings and the errors are human made (that's me 🖖), the corrections are from the Machine (that's me 🤖).

But let's go on, believe it or not, this post is about IT professional services, and how example42 delivers them.

Needless to say that they are all about Puppet: development of infrastructure code, consulting, training, fire fighting, technical, architectural, philosophical and moral support.

You can check example42's website for more details, here you can read how they have been implemented in the last months.


## The example42 way

Let me show some examples of real support cases, approached in the example42's way.

### Really Instant Puppet support 

One of the most interesting and satisfactory example of example42's Instant Support has been for an english University: we receive an mail from the website contact form asking for support on a Puppet issue, after some minutes I reply, giving the availability for an Hangouts call. We setup the call in a few minutes and on a shared screen we start to diagnose the problem.

The Puppet server's CA (an old 3.x Open Source server) is expired and clients can't connect anymore (oh those default 5 years which pass so fast!): the problem has emerged 3 days ago and couldn't be solved by the person I have the call with (a consultant who had the bad luck of having to cope with a Puppet setup he has little confidence with).

After having the confirmation that the number of managed nodes is really small (about 15), I suggest to just reinitialize a brand new Puppet CA and re-sign every client. I explain the consequences and the impact of such a brutal approach (the need to connect to each client and cleanup it's certificates), and the fact that that saner alternative to extend Puppet's CA is a bit more complicated in an old setup (and needs further investigations from my side). The customer agrees to follow this procedure.

We backup the leftovers of the old CA, we regenerate a new one, we test and prepare the one liner command to paste and run on each client, and after 30 minutes of call, the problem is solved and clients are happily running using the new CA. I spend the last 30 minutes of the call explaining some basic Puppet concepts, where to look for troubleshooting problems and how the (old) infrastructure may evolve in the future (this last topic is actually of few interest for my interlocutor, given he just found himself in the wrong place at the wrong moment).

Lesson here: sometimes a simple practical solution is more effective than a technically correct but complex one (especially if you don't know it out of the box and Google struggles to help).


Another case of fast and successfully support is for another English company (I love how they are pragmatic when there's to ask support to solve something). We get a request for urgent support on a Puppet issue with agents unable to connect to the server. Timeline is as follows:

- At 12:58 we receive the email request for urgent support
- At 13:17 I reply via email giving availability for a conference call
- At 16:10 I receive an invitation for a Zoom call at 16:30. 
- At 16:30 we have the Zoom call, there are 4 people from the customer and one of them shares his screen with access to the system. I cut most of the introductions as if we already knew each other (how impolite!) and we go straight to the point, asking what's the problem and guiding the person that shares his screen in showing the information of interest. 
- Around 17:15 the problem is solved. Half an hour to gather info on the infrastructure and the issue. Five minutes to fix and test it. We pass the rest of the call talking about Puppet, Universe and Everything.

Now, let's be clear, I'm not always so quick in solving Puppet problems, these are two cases which were particularly lucky (let's call it luck...), but they are good examples of what example42's Instant Support is all about. And, trust me, I really can solve 95% of Puppet related issues in a few minutes.


### Smart Puppet Support

Thanks to the Gods of the Cloud, not all the cases are urgent and we don't always have to deal with Puppet infrastructures on fire.

Most of my synchronous Puppet support is done during calls scheduled on the calendar. This happens usually with customers with which there's an ongoing support contract. 

Sometimes these calls are scheduled in a recurring manner, sometimes they are arranged days or weeks before, in *one* case I sometimes happen to receive the call invitation in the same days it's scheduled, but that's a big customer which I like and, in any case, I know that in the same day a call is expected to be scheduled.

If my calendar is free and I haven't other things to do, I don't have problems in accepting also these last minute calls, if not, I propose a different time and we always manage to get the thing done.

It's not rare, with customers that have an ongoing support contract, to receive emails asking for support for some new Puppet issue or error. When this happens, I connect to the customer infrastructure, check the issue, arrange a call with the customer and I show how I can fix, or have fixed, the problem.

Plain, straight to the point and usually effective. The customer pays for the time spent on it, according to the contract terms.

### Free support

I lied before (actually this misleading AI did).

I wrote that services are not free, but that's not always the case. Via example42's website you can contact me directly via WhatApp, and ask me any Puppet related question. As soon as I can, I reply, if I've an answer I just give it, if the issue requires more investigation I ask for details. Then if the effort to diagnose and solve the problem seems to require more than a few minutes I ask to proceed with one of the paid support services we provide.

In a case I actually happened to spend a few hours, including a shared screen call, to give some advice. It generally happens with individuals from countries where the cost of life is significantly lower than european one, in such cases I really don't feel comfortable at requesting hourly rates which might cost a significant part of an average salary.

So, don't be shy, if you have any Puppet related issue or something to clarify, just contact me via WhatsApp, I'll be happy to help you.

Money talks can happen later, if you want.


## Methodology

What kind of professional services may you expect from an unknown person you contact out of nothing with whom you have to share in a few minutes the burden and complexity of your infrastructure?

How can you trust him (me)? How can you share your infrastructure management with someone who doesn't know anything about it?

How can you share sensitive information with someone you don't know, without a NDA or a contract?

Well, first of all, I can sign all the NDA you want, I can sign a contract, I can sign a blood pact with you, if you want. But I don't think that's necessary. (This one comes from Copilot! 🤖).

I don't have problems in adapting to every procedure you may require, even I prefer to go straight to the point and face the technically challenges of the problem, rather than wasting time in signing papers.

For the rest I guess you have to trust my integrity, experience and knowledge.

I've done Puppet works for companies and entities like Bank of Italy, Vatican City State, Rocket Internet, Foodpanda, Volunia, Bsource / Avaloq, Cineca, Deutsche Telekom, Boeringer Ingelheim, Bundesnotarkammer, Strato, Kuwait Petroleum, University of Bologna, Politecnico di Milano, Infocert, IHS Markit, Cornell University, Porsche, Swisscom, Agility, Willis Tower Watch, Schufa, Banque Central de Luxemburg, Blackrock.

I hope I've left a good impression in all of them.

I've been in IT for more than 25 years, working on operations, networking and security, mostly on Linux and Open Source software. I think I know what I'm doing when I touch configuration files.

I'm also working almost exclusively on Puppet for 15 years and I know how to discover what's the potential effect of a change, how to investigate what's the potential range of impact on the infrastructure of change in a given Puppet class, Hiera key or file template.

But most of all, when there's not an ongoing contract where I'm granted access to the client's systems, we work on a shared screen session, where YOU control what is done, I just give you advice and you decide what to do. I don't have access to your infrastructure, I don't have access to your data, I don't have access to your secrets. I just see your screen.


## Work and life balance

Engagement for example42's Puppet support can be done at any time and day, from every continent.

I never offer a strict SLA or guarantees on intervention times, but in most of the cases the reply and the actual start of the activity is within the day.

You my wonder what hellish life I might be doing, giving this around the clock availability.

My answer is that I don't care about working outside plain working hours or in festive days.

When I work asynchronously, commits in my customer's control-repos might be at midnight or at 6 AM GMT+1, my usual timezone (ehi, I wrote commits, not deployments to production: they are always verified and checked with the customer).

When I work synchronously, typically in conference calls, sometimes onsite, I don't need to have to plan it weeks before. If I can, I can connect and give support as soon as I'm notified of a request.

The main reason all this does not drive me crazy, is that I like my work, I love to develop things with Puppet, and I like to share what I know about it.

The other reason is that I've actually have plenty of free time to do other things, also because, generally to solve a Puppet problem or develop code I take only a fraction of time of a normal DevOps engineer with generic Puppet experience (everyone has his/her skills, my ones are very vertical on Puppet but still quite broad on IT operations, security and networking)



## So long and thanks for all the fish

Are you really reading these last words?

How have you survived this unbearable sequence of embarrassing self promotion boasts?

Well, what to say, if not just Congratulations and Thank You!

You know for what.

Alessandro Franceschi

example42 Founder and Chief Puppet Consultant
