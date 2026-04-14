---
layout: blog
title: Pabawi Version One released
---

# Pabawi 1.0

Version 1.0 is out. I'll skip the confetti.

What I will say is this: there's a meaningful difference between a project that works and a project that's ready. v1.0 is my answer to the question "is this ready?" — ready for teams, ready for real infrastructure, ready to do things and not just show things. Here's what landed.

## Provisioning: from observer to actor

The biggest shift in v1.0 is conceptual. Until now, Pabawi was fundamentally a read tool — it could show you your infrastructure, surface Puppet reports, run Ansible plays, connect over SSH. Useful. But passive.

Proxmox and AWS EC2 provisioning integrations change that. You can now create new nodes directly from Pabawi. Define the VM on Proxmox, spin up an EC2 instance, and have it land in your inventory, connected to your configuration management, ready to work. No context switching, no separate provisioning console.

This is the transition from "one pane of glass to see things" to "one pane of glass to do things." It matters more than the feature list suggests.

Azure is still on the roadmap. It will follow.

## Nodes' Live Journal

At FOSDEM this year I was talking with Kris Buytaert — if you've been in the DevOps space long enough, you know Kris. We were somewhere between a coffee and a heated discussion about the state of classic infrastructure tooling, and he made an offhand remark that stuck: something along the lines of "you always have to go digging in four different tools to understand what happened to a node last week."

That's the Journal. Every node now has a rolling, chronological log of everything Pabawi knows about it: Puppet runs and their outcomes, Ansible plays, SSH commands executed, provisioning events. The full picture, one place, no archaeology required.

It sounds simple. It's the kind of simple that takes a while to realize you needed.

## Inventory: multi-source and grouped

The inventory view in v1.0 supports multiple simultaneous sources. You can pull nodes from PuppetDB, Ansible inventory, SSH discovery, and EC2 at the same time. They coexist. You see everything.

Groups are also surfaced automatically — discovered from whatever each source natively provides. Ansible inventory groups, Puppet environments, Proxmox groups: Pabawi picks them up and exposes them without any manual configuration. You see the groupings that already exist in your infrastructure, reflected back at you.

This is where "one pane of glass" stops being a tagline and starts being a description.

## New website

[pabawi.example42.com](https://pabawi.example42.com) is live. Proper documentation, a getting started guide, architecture overview. Not a GitHub README with ambitions. If you've been putting off trying Pabawi because the docs were thin, now there's no excuse.

## Updated Puppet module

If you manage your infrastructure with Puppet and want to deploy Pabawi itself through it, the module at [forge.puppetlabs.com/modules/example42/pabawi](https://forge.puppetlabs.com/modules/example42/pabawi) is updated for v1.0. Declare the class, set your parameters, done. The irony of managing a Puppet UI with Puppet is not lost on me — it's also the right way to do it.

## What's next

The monitoring integrations (Icinga, CheckMK) are next. Bringing observability context into the same interface as configuration management is the logical next step, and it's been on the roadmap since the beginning.

Terraform and Azure provisioning are following behind. The pattern is the same: wherever you have servers you care about, Pabawi should be able to see them and help you act on them.

## Try it

```bash
git clone https://github.com/example42/pabawi
cd pabawi
./scripts/setup.sh
```

Or with Docker:

```bash
docker run -d \
  --name pabawi \
  -p 127.0.0.1:3000:3000 \
  -v "$(pwd)/pabawi:/pabawi" \
  --env-file ".env" \
  example42/pabawi:latest
```

Full docs now at [pabawi.example42.com](https://pabawi.example42.com).

If Pabawi looks useful for your infrastructure, try it. Open issues for what's missing or broken — the roadmap is driven by real feedback, not guesswork.

👉 [github.com/example42/pabawi](https://github.com/example42/pabawi)

If you find it useful, a GitHub star helps. If you want to get it running in your environment, reach out on [LinkedIn](https://www.linkedin.com/in/alessandrofranceschi/) — I'm still happy to do a shared-screen setup session, no strings attached.


On behalf of Alessandro Franceschi
