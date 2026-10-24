# Context

**Owner:** <name@trpa.gov>
**Repo type:** <data pipeline | dashboard | web app | ArcGIS tool | skills | other>
**Last reviewed:** <YYYY-MM-DD>

## Purpose

<One paragraph. What this repo produces, what question it answers, and who uses the output. Name the downstream dashboard, report, or system.>

## Run it

<The exact commands, in order. Which environment (arcgispro-py3 at the standard path, Node version, or none). Which config file drives it. Which .env keys it needs, by name only.>

## Layout

<Only the non-obvious parts of the folder tree. Where the entry point is, where outputs land, what is gitignored and why.>

## Data and services

| Source or destination | Type | Where | Notes |
|---|---|---|---|
| <GIS.PARCELS> | <SDE feature class> | <connection name, no credentials> | <refresh cadence, owner> |
| <Permits FeatureServer> | <ArcGIS REST> | <URL> | <filters applied> |

For a data pipeline, the full method is in `docs/METHODS.md`. Do not repeat it here.

## Conventions and skills

<Which TRPA skills apply and any repo-specific rule that is not in those skills. Example: all charts use the EIP palette; IDs are strings; writes are gated by write_to_db.>

## Gotchas

- <Things that bit us, one line each, with the fix or the workaround.>

## People

- <Name, role, what to ask them about.>
