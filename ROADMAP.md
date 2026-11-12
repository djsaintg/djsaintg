# 🗺️ Profile Roadmap

This repo is the **coordination hub** for everything that lives across my GitHub presence.
Anything hosted here that other repos reference, any change that ripples across the library,
and any profile-level polish gets planned and tracked in this file.

> *"Code with rhythm. Ship with grace."*

---

## 🎯 How this file works

- **`[x]`** — shipped and live
- **`[ ]`** — planned or in progress
- If a change needs a **central call location** (one file, many repos pointing at it), it gets built here first, then referenced everywhere via `raw.githubusercontent.com/djsaintg/djsaintg/main/...`

---

## 📦 Centralized assets

Files hosted in this repo that other repos link to directly.

| Asset | Path | Referenced by | Status |
|---|---|---|---|
| Animated sponsor button | `sponsor.svg` | Profile · Highland Song · ForgeBound · RS3 · Hogwarts Legacy | ✅ Live |
| Profile avatar (source + 1024px) | `avatar.svg` · `avatar.png` | GitHub profile picture | ✅ Live |
| Stats cards (auto-generated daily) | `stats/overview.svg` · `stats/languages.svg` | Profile README | ✅ Live |

**Adding a new centralized asset:**
1. Create the file in this repo's root
2. Reference it elsewhere via `https://raw.githubusercontent.com/djsaintg/djsaintg/main/<file>`
3. Add a row to the table above

---

## ✅ Shipped

- [x] **Centralized sponsor button** — animated Terminal SVG, single source of truth
- [x] **Library section** in profile README — every repo listed with version, tags & live demo
- [x] **GitHub Pages demos** — Highland Song, RS3, Spiritfarer & Hogwarts Legacy live at `djsaintg.github.io/...`
- [x] **`.nojekyll`** in Highland Song so Pages serves raw files cleanly
- [x] **Library expanded to all six pinned repos**, grouped into Maps · Companions · Mods · Linux Tools
- [x] **ForgeBound unpinned** while it matures; **Objective Tracker** (Hytale mod) takes its Library slot
- [x] **"🎯 Currently" refreshed** to match what's actually on the bench
- [x] **Library caught up (2026-11-11):** ForgeBound back in with its playable demo, Vein Mining, the four Minecraft Fabric mods, and the Mealient fork under Open Source Work; Highland Song and Spiritfarer version lines bumped
- [x] **Self-hosted stats cards:** `.github/workflows/stats.yml` regenerates them daily, replacing the paused github-readme-stats service
- [x] **New avatar:** `> SG▌` terminal monogram with halo and waveform, Tokyo Night palette

## 🔭 Planned

### Profile
- [ ] Keep Library version lines (and the badge counts) in sync when repos ship
- [ ] Re-pick the six pinned repos now that there are 13 (needs the GitHub web UI)
- [ ] Add the next Library entry (under the right category) when the next project lands
- [ ] Consider a contact/social section (Twitter, Discord, email)

### New centralized assets (the `sponsor.svg` pattern)
- [ ] **Profile card SVG** — a compact identity card (name, tagline, waveform) any repo could drop in a footer
- [ ] **Shared tech-stack badge row** — one SVG, every README
- [ ] **Standard support heading** — align `## 💖 Support this Project` across all repos

### Per-repo polish
- [ ] **Social preview images** for all repos (the ForgeBound banner is ready to reuse)
- [ ] **Website field** in each repo's About sidebar → its Pages demo (Spiritfarer & Hogwarts Legacy done)
- [ ] **Author attribution block** in Highland Song & ForgeBound (RS3 already has one)

### Ecosystem
- [ ] Watch own repos for release & issue activity
- [ ] Consider a shared `CONTRIBUTING.md` template for the fan tools

---

## 🔁 Update ritual

Whenever a repo ships a release:
1. Bump its version line in the **Library** section of `README.md`
2. If the release touches a centralized asset, update the asset here and push — every repo picks it up automatically
