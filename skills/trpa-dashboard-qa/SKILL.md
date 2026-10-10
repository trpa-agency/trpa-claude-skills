---
name: trpa-dashboard-qa
description: Pre-deploy QA checklist for TRPA dashboards and web tools — laketahoeinfo.org, climate.laketahoeinfo.org, monitoring.laketahoeinfo.org, eip.laketahoeinfo.org, parcels.laketahoeinfo.org, transportation.laketahoeinfo.org, stormwater.laketahoeinfo.org, clarity.laketahoeinfo.org, thresholds.laketahoeinfo.org, gis.trpa.org, and any internal TRPA web app. Use this skill before deploying or shipping a dashboard, web map, indicator page, or any browser-based TRPA tool. Trigger on phrases like "ready to deploy", "ready to ship", "QA the dashboard", "review before publishing", "pre-deploy check", "dashboard checklist", "going live", or any context where Mason is about to push a TRPA web tool to production. Pair with `trpa-dashboard-stack` and the relevant brand skill.
---

# TRPA Dashboard QA

A pre-deploy checklist for TRPA browser-based tools. Run this before pushing any dashboard, indicator page, web map, or interactive report to a production URL on the `*.laketahoeinfo.org` or `*.trpa.org` ecosystem.

The goal is to catch the embarrassing-but-fixable stuff (broken links, busted mobile layout, unreadable contrast, stale data) before a stakeholder sees it.

---

## When to use this skill

- Before deploying a new dashboard page
- Before pushing a significant change to an existing dashboard
- After a data refresh that touched the page
- When a stakeholder is about to demo the tool to leadership

If you're just iterating locally and not deploying, skip this — overhead is real. Run the full checklist when it actually matters.

---

## The Checklist

Work through each section in order. For each item, mark **Pass / Fail / N/A** and note the issue if Fail.

### 1. Branding and Visual Polish

- [ ] **Correct brand applied.** TRPA Blue (`#0072CE`) for general agency tools, EIP color palette for EIP / Forest Health / AIS / Stormwater work, Tahoe Living palette for housing. See the relevant brand skill.
- [ ] **Logo present and correct variant.** Use white logo on dark backgrounds, color logo on light backgrounds. Top-left of header is the default placement.
- [ ] **Font is Open Sans** (the web equivalent of Calibri). No Times New Roman, no system-default sans-serif fallback unless intentional.
- [ ] **Chart color sequence matches brand defaults.** No random Plotly defaults bleeding through.
- [ ] **No placeholder text or lorem ipsum** anywhere visible.
- [ ] **Page title and meta description set** in `<head>` — these show up in browser tabs and search results.
- [ ] **Favicon set.** Use TRPA favicon for general tools.

### 2. Content Accuracy

- [ ] **All numbers verified against the source data.** Spot-check at least three values against the upstream CSV / SDE table / REST endpoint.
- [ ] **Date stamps are current.** "Last updated" matches the actual data refresh date, not a hardcoded value from the prototype.
- [ ] **Units labeled on every metric.** Acres, percent, count, etc. — never assumed.
- [ ] **Source citations present** under every chart and table. Format: "Source: [program/agency], [year]."
- [ ] **Acronyms defined at first use.** Even EIP, BMPs, SEZ, VMT, TAU, CFA — define them.
- [ ] **TRPA Style Guide rules applied.** Oxford comma, "50 percent" in prose, dates abbreviated with specific days (Jan. 1, 2026), gender-neutral language.

### 3. Accessibility (WCAG 2.1 AA target)

- [ ] **Color contrast ≥ 4.5:1** for body text against background, ≥ 3:1 for large text and UI components. Check with [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/).
- [ ] **Charts not color-only.** Patterns, labels, or annotations carry the meaning for color-blind users.
- [ ] **All interactive elements keyboard-reachable.** Tab through the page. Focus indicators visible.
- [ ] **Alt text on every meaningful image.** Decorative images use `alt=""`.
- [ ] **Headings in proper hierarchy.** One `<h1>`, then `<h2>` → `<h3>`, no skipping levels.
- [ ] **Form inputs labeled.** Use `<label for="...">` or `aria-label`.
- [ ] **Maps have a non-map alternative** for screen readers — a data table or summary text covering the same information.
- [ ] **Color contrast on charts** — TRPA Blue (`#0072CE`) on white passes 4.5:1; navy (`#003B71`) is even better. Avoid placing Olive (`#B5A64C`) or Ice (`#B4CBE8`) on white for text — they fail.

If `accessibility-review` skill is installed, use it for a deeper audit on stakes-y deployments.

### 4. Responsive Layout

- [ ] **Test at mobile width (375px).** Charts reflow, no horizontal scroll, text readable without zoom.
- [ ] **Test at tablet width (768px).** Layout makes sense, no stranded white space.
- [ ] **Test at desktop (1280px and 1920px).** No content stranded in a narrow column when wide screens are available.
- [ ] **Touch targets ≥ 44×44px** for buttons, links, and tab triggers on mobile.

Browser DevTools' device-emulation pane is enough for a sanity check. For real-world testing, hit the staging URL on a phone.

### 5. Cross-Browser

Test in:

- [ ] **Chrome** (latest)
- [ ] **Edge** (latest — many TRPA staff and Governing Board members use Edge)
- [ ] **Safari** (latest — for Mac and iOS users)
- [ ] **Firefox** (latest)

The most common issue: ArcGIS Maps SDK or Plotly behaving differently in Safari. Test maps and charts specifically.

### 6. Performance

- [ ] **First Contentful Paint < 2 seconds** on a typical broadband connection.
- [ ] **Total page weight < 2 MB** unless there's a documented reason (e.g., the page hosts a large dataset).
- [ ] **No unused libraries loaded.** If you're not using AG Grid on this page, don't import it.
- [ ] **Images optimized.** PNGs compressed, large photos served as WebP or compressed JPEG.
- [ ] **Map tiles cached** — don't re-fetch on every interaction.
- [ ] **Lighthouse Performance score ≥ 80** as a sanity check.

### 7. Data Freshness and Pipeline

- [ ] **Underlying data refresh ran successfully.** Check the pipeline log.
- [ ] **No stale "TODO: refresh before launch"** placeholders in the code or copy.
- [ ] **REST/API endpoints return expected payload shape.** Open DevTools → Network → reload — confirm responses look right.
- [ ] **Fallback behavior tested.** What does the page do if the API is down? Should not crash silently.

### 8. Links and Navigation

- [ ] **All links work.** Use a link checker (e.g., `linkchecker` CLI) or click each manually.
- [ ] **External links open in a new tab** with `target="_blank" rel="noopener noreferrer"`.
- [ ] **Internal nav (header, footer) consistent** with the rest of the `*.laketahoeinfo.org` ecosystem.
- [ ] **404 page customized** if this is a standalone site.

### 9. Pre-Push Sanity

- [ ] **No console errors or warnings** in DevTools on page load.
- [ ] **No hardcoded local paths** (`file:///`, `localhost`, `C:\Users\...`) in the source.
- [ ] **No exposed secrets** (API keys, tokens, credentials) in JS/HTML.
- [ ] **Git status clean.** Committed, pushed, ready to deploy.
- [ ] **Stakeholder review done** if the change is consequential. Don't ship untested changes to leadership-facing tools.

---

## Quick mode (for minor changes)

For small tweaks (copy edits, color tweaks, single-data-point fix), running the full checklist is overkill. Run this short version instead:

1. Branding looks right.
2. Numbers verified against source.
3. No console errors.
4. Mobile layout still works.
5. The specific change tested in the deploy environment.

If anything fails the short version, run the full checklist.

---

## Output Format

When invoked, produce a checklist report (Markdown) with:

```
# Dashboard QA Report — <dashboard name>
**Date:** <today>
**Reviewer:** Mason Bindl
**Target URL:** <staging or prod URL>

## Summary
- Pass: <count>
- Fail: <count>
- N/A: <count>

## Failures (must fix before deploy)
- [section] [item]: <description and fix>

## Warnings (recommend fix, not blocking)
- ...

## Notes
- ...
```

---

## Pairs with

- **`trpa-dashboard-stack`** — defines the tech stack the dashboards are built in.
- **`trpa-brand` / `trpa-eip-brand` / `tahoe-living-brand`** — for the brand verification step.
- **`accessibility-review`** — deeper a11y audit when needed.
