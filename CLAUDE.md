# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About This Site

Jekyll site for [example42.com](https://example42.com) — home of Example42's Puppet/DevOps consulting services and the **Abnormal DevOps Iterations (ADI)** podcast. Deployed via GitHub Pages.

Media production assets (audio, video, transcripts, cover images) live in the sibling OneDrive workspace: `~/Library/CloudStorage/OneDrive-Personal/ADI/`

## Local Development

```bash
# Via Docker (recommended — no local Ruby/Jekyll install needed)
bash bin/docker_jekyll.sh
# Serves at http://127.0.0.1:4001 with live reload

# Or with local Ruby/Bundler
bundle exec jekyll serve --config _config.yml,_config_dev.yml
# Serves at http://127.0.0.1:4000
```

## Site Architecture

| Path | Purpose |
|------|---------|
| `_episodes/` | ADI podcast episode pages (001.md, 002.md…) |
| `_posts/` | Blog posts |
| `_presentations/` | Tutorial/presentation pages |
| `_layouts/` | Page layouts (Jekyll) |
| `_includes/` | Reusable HTML partials |
| `_config.yml` | Production config |
| `_config_dev.yml` | Dev override — sets `url: http://127.0.0.1:4000` |
| `AbnormalDevOpsIterations/img/` | Resized episode cover images |

## Episode Pages (`_episodes/NNN.md`)

Files are zero-padded: `001.md`, `022.md`. The layout `adi_humanintelligence` renders via `_layouts/adi_humanintelligence.html` → `_includes/adi_detail.html`.

### Required Frontmatter

```yaml
---
number: '22'                        # string, matches the episode number
layout: 'adi_humanintelligence'     # always this value
title: 'Episode title'
date: 'YYYYMMDD'                    # e.g. 20250305
host: Alessandro Franceschi
youtube: 'YouTubeVideoID'
guest:                              # list (or bare string for single guest)
  - Guest Name
tags:
  - Tag1
  - Tag2
summary: "One-sentence summary, ~200 chars max, no names"
quotes:
  - "Quote 1, ≤140 chars"
  - "Quote 2"
  - "Quote 3"
  - "Quote 4"
---
Episode body text here.
```

`guest` can be a bare string (`guest: Name`) or a YAML list. The template iterates over it with ` for g in page.guest `.

### Adding a New Episode

1. Create `_episodes/NNN.md` with full frontmatter above
2. Add cover image: run `bin/resize_pics.sh` to copy + resize from `ADI/Covers/ADI N.png` → `AbnormalDevOpsIterations/img/N.png`
3. The episode URL will be `/AbnormalDevOpsIterations/NNN/`

## Tooling Scripts

| Script | What it does |
|--------|-------------|
| `bin/docker_jekyll.sh` | Serve site locally via Docker on port 4001 |
| `bin/resize_pics.sh` | Resize ADI cover images and copy to site img dir |
| `bin/get_quotes.py` | Generate `summary` + `quotes` frontmatter from a transcript file using OpenAI |

### `get_quotes.py` usage
```bash
export OPENAI_API_KEY=...
python3 bin/get_quotes.py /path/to/transcript.txt
# Outputs YAML — paste into episode frontmatter
```
