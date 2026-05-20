---
layout: blog
title: Hands in the Swamp
---

This is weird, and I guess a sign of the weird times we live in.

## A pond of beautiful entities

I’m not sure about the first time I heard about [Swamp](https://swamp.club){:target="_blank"}, I guess at last CfgMgmtCamp in February directly from Adam Jacob.

If you know Adam, you know that he is a brilliant guy with crazy ideas, sometimes too ahead of their times (Ok, he also did Chef, when there was already Puppet, messing up things in our placid community, but that's another story).

In the next months I kept on having indirect updates about Swamp from Paul Stack and his posts here on LinkedIn but that remained the classic "apparently cool tool I should check out when I have time".

That time, of course, never arrives, even if I have plenty of it.

This morning was different, I woke up earlier than usual, gave a look at post from Paul, went to the Swamp site and wondered, once again, "What the **** is Swamp anyway"?

Honestly, claims like “[ADAPTIVE WORKFLOWS|DETERMINISTIC AUTOMATION] FOR AI AGENTS” didn't really click anything in me, and it took me some time to understand the inner, and powerful, meanings.

Anyway, instructions say: install swamp with the usual "download and run a random script".

Ok, I’m sadly familiar at performing unprotected sex with the Internet.

Then go to your repo and run `swamp init` and then open your agent tool.

What repo? Your infrastructure management repo? Your own software repo? Any repo?

So I went to my pabawi repo (btw, it’s has been launched right today on [Product Hunt](https://www.producthunt.com/products/pabawi), give it look ) and wondered... now what?

This is software, not infrastructure to run things on.

I consulted a random bot, of course, at least to try to understand what Swamp can be used for in this case, and then I wondered that maybe I could use it to automate the testing of Pabawi Docker images, to begin with something.

## Swamping for a single bad naming choice

So I started to put my hands in the swamp.

Needless to say they quickly became dirty.

Very dirty.

In pure, ignorant, vibe approach, I asked Codex to do something with Swamp to automate the testing of Pabawi docker images.

The AI started to juggle with tokens, searched the swamp.club for existing extensions and generated a workflow to test the local Dockerfile on remote system over ssh.

I wondered why testing my local software on a remote server, when I have a local docker running, and hence, after a few more AI mumblings and no viable existing alternative, I wondered why not making a general purpose Docker local testing extension?

My damn tendency to abstract things to make them reusable.

Here comes my trip to the rabbit hole, I just started to use swamp and I was already trying to make a public extension.

It could have been an incredibly fast rewarding experience, but in my case, for this very specific case, it has been a (relatively) painful (in the degree of a "few hours and several tokens spent" pain scale) experience.

I struggled with conflicts from local development and published versions, issues with unknown model types, AIs already reassuring that everything was fine, while nothing was, moving the extension to a dedicated repo, and doing it in the wrong way, then, again, issues with unknown model types. 

All this via a quick burn of Codex 5 hour session credits, some additional credits bought (clear sign I was hooked in the trap), a shift to Claude code, because I didn’t want to burn too quickly Codex extra credits, and the hit of Claude limits as well, to finalize everything with Antigravity.

After several troubleshooting sessions, where the AI was apparently shooting at its own generated troubles while it should have aimed at my bad naming choices, Claude told me:

    ⏺ ROOT CAUSE — confirmed in swamp's source (extension_loader.ts:1112):

      entry.isFile && entry.name.endsWith(".ts") &&
      !entry.name.endsWith("_test.ts")   // test files are excluded from discovery

      The model file is named docker_image_test.ts — it ends in _test.ts, so swamp's extension loader treats it as a test file and excludes it from discovery entirely. swamp
      extension push uses the manifest's explicit list (so it bundles fine, modelCount: 1), but every consumer scans the directory, skips *_test.ts, and registers 0 models.
      The type string, paths.base, the layout — none of it ever mattered. It was the filename all along.
  
A bad name, a bug in upstream code, promptly reported with the insanely cool `swamp issue` command, some other minor tweaks, 7 releases on day one, and finally an apparently working docker-image-test extension was published.


## Muddy conclusions

The good thing?

In the process I started to learn something about Swamp, just scratching the surface, but my mind started to be enlightened about its endless possibilities.

The bad thing?

The fact that anyone can publish an extension and anyone else can use it out of the box with Swamp and use it for any infrastructure or automation workflow scares me.

Feature request for Adam, Paul and whoever works in the Swamp: if you are not already doing it, do some kind of automated security assessment on what users publish on swamp.club

Lessons learned?

The usual one.
AIs are smart for smart users and dumb with dumb users.

The unnecessary irony?

After all this effort I thought that I probably could have achieved the same "docker build and test" task in much less time with a shell script.

I'm still not sure if this specific Docker test extension makes sense, in Swamp world, but my ancient DevOps spirit keeps on reminding the sacred principles of reusability, abstraction and repeatability and the curious AI fanboy of the current times lights up at the huge powers of gated and modelled AI driven workflows.

Alessandro Franceschi
