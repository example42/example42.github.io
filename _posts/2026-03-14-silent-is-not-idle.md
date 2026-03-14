---
layout: blog
title: Silent is not idle
---

# Pabawi is Growing Fast: from v0.4 to v0.8 in Two Months

Two months ago I wrote about Pabawi, a web frontend for classic infrastructures. At the time, v0.4.0 had just shipped with Bolt, PuppetDB, PuppetServer and Hiera integrations. It was a working prototype — useful, but rough around the edges.

Today, four releases later, Pabawi is a different animal. This post is a catch-up: what changed, where we're going, and why I think this project matters more than ever.

## What happened in two months

Development moved fast. Here's what each release brought:

**v0.5.0** — Deeper Puppet visibility  
Report filtering, Puppet run history visualization with timeline view, and an enhanced expert mode with frontend logging. If you use PuppetDB seriously, this version made Pabawi genuinely useful for day-to-day operations.

**v0.6.0** — Foundations  
Mostly internal: code consolidation, architecture cleanup, bug fixing. Not glamorous, but necessary. A project that grows this fast needs these stabilization moments.

**v0.7.0** — Ansible joins the party  
This was a big one. Ansible integration landed, meaning Pabawi is no longer a "Puppet tool" — it's a multi-tool. If you run a mixed environment (and most people do), you can now see and act on Ansible-managed nodes from the same interface. Also: class-aware Hiera lookups, which makes the Hiera Data Browser significantly more useful.

**v0.8.0** — RBAC and SSH  
Role-based access control. Multiple users, controlled access, audit trail. This is what takes Pabawi from "personal tool on localhost" to something you can actually deploy for a team. SSH integration also landed, adding direct SSH-based node management and expanding the inventory sources available.


## The bigger picture

When I started Pabawi, the goal was simple: I wanted a modern OSS web UI for Puppet and Bolt. The classic infrastructure space — physical servers, VMs, decades of accumulated systems — is enormous, but it's been left behind by tooling.

Everyone builds for Kubernetes. Everyone builds for cloud-native. But the people managing 200 bare-metal servers running CentOS 7 with Puppet? They get a CLI and a prayer.

Pabawi is trying to fix that. Not by replacing Puppet or Ansible or Bolt — those tools are excellent at what they do. But by giving you a single, modern web interface to work with all of them together.

The vision: one pane of glass for classic infrastructure.


## What's coming

**Proxmox integration** is in active development. If you manage VMs on Proxmox — and a lot of people do — this will let you see and interact with your virtualization layer alongside your configuration management data.

After that, the roadmap extends further:

- **Icinga / CheckMK** — bring monitoring context into the same interface
- **Terraform** — infrastructure provisioning alongside configuration management  
- **EC2 / Azure** — for hybrid environments that span on-prem and cloud
- **Choria, scheduled executions, custom dashboards**

The pattern is consistent: wherever you have servers you care about, Pabawi should be able to see them and help you act on them.


## Try it

Getting started is straightforward. Clone the repo and run the setup script:

```bash
git clone https://github.com/example42/pabawi
cd pabawi
./scripts/setup.sh
```

Or use Docker:

```bash
docker run -d \
  --name pabawi \
  -p 127.0.0.1:3000:3000 \
  -v "$(pwd)/pabawi:/pabawi" \
  --env-file ".env" \
  example42/pabawi:latest
```

Full docs at [github.com/example42/pabawi](https://github.com/example42/pabawi).


## Give it a try — and tell me what you think

If Pabawi looks useful for your infrastructure, the best thing you can do right now is try it and tell me what's missing.

Clone it, run `./scripts/setup.sh`, and connect it to your existing Puppet, Bolt or Ansible setup. It should take less than 30 minutes to have something running. If it doesn't, that's already useful feedback.

👉 [github.com/example42/pabawi](https://github.com/example42/pabawi)

If you find it useful, a GitHub star goes a long way for an open source project. If you find something broken or missing, open an issue — the roadmap is driven by real users.

**Want help setting it up?** I'm still offering a free shared-screen setup session — 30 minutes, no strings attached. We get it running in your environment, connected to your tools. Reach out on [LinkedIn](https://www.linkedin.com/in/alessandrofranceschi/) to schedule a call.


On behalf of Alessandro Franceschi
