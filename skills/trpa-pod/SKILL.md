---
name: trpa-pod
description: TRPA department pod playbook for bringing AI tooling to one department at a time with a forward deployed engineer, an implementation and project manager, and a QA engineer. Use when planning or running a department engagement, writing a pod intake, scoping a beta for a department, deciding whether a problem becomes an app, a skill, a pipeline, or a document workflow, or when a beta hits its graduate-or-archive date. Trigger on department pod, pod intake, forward deployed, department engagement, beta app for a department, or solving a problem for Legal, Finance, Science and Data, Long Range and Transportation Planning, the Environmental Improvement Program, Permitting and Compliance, Reporting and Accountability, or Communications at TRPA.
---

# TRPA Department Pods

A pod brings AI tooling to one TRPA department at a time: sit with the department, find the problem worth solving, build a beta, and either graduate it or kill it. The working folders, the intake template, and the app scaffold live in the `trpa-agency/tools` repo. This skill is the process, so any machine runs an engagement the same way.

## Where things live

- `tools/pods/README.md`: the playbook, source of truth. This skill summarizes it; when they disagree, the repo wins and this skill gets updated.
- `tools/pods/_intake-template.md`: copy per engagement into the department folder as `intake-YYYY-MM-DD.md`.
- `tools/pods/<department>/`: one folder per department with status, work in flight, and intake docs.
- `tools/qa/_template/`: the single-file HTML starter for beta apps, with its own README.

The tools repo is public. Engagement notes record roles and workflows, never individual staff, and never sensitive records.

## The departments

Legal, Finance, Science and Data, Long Range and Transportation Planning, Environmental Improvement Program, Permitting and Compliance, Reporting and Accountability, and Communications. Science and Data staffs the pod. Folder slugs match `tools/pods/`.

## The three roles

- **Forward deployed engineer.** Sits with the department, watches the workflow, writes the intake, builds the prototype. Discovery is the job. Do not accept the tool the department asks for at face value; find the step where the hours go.
- **Implementation and project manager.** Owns the scope document, the beta schedule, and check-ins with the department lead. Holds the engagement to one problem.
- **QA engineer.** Runs `trpa-dashboard-qa` on apps, verifies numbers against source data for everything, and signs off before anyone outside the pod sees the work.

One or two people plus Claude cover all three roles. Keep the roles distinct even when one person wears them, because each one has a different definition of done.

## Lifecycle

1. **Intake.** Fill the intake template during the sit-down. The data access section is mandatory and comes first: SDE is not reachable from a browser, maps.trpa.org CORS fails on the office network, LT Info tabular data comes from internalapi.laketahoeinfo.org, and anything behind a login cannot live in a public static app.
2. **Scope.** One problem, one container. An app in `qa/` is one option, not the default. The other containers are a Claude skill in this marketplace, a data pipeline in its own repo, or a document workflow. Legal and Finance problems usually land outside the public repo.
3. **Build.** Apps: stamp `qa/_template/` into `qa/<category>/`, register in `apps.json` with beta true, follow `trpa-dashboard-stack` and the right brand skill. Skills: build here with skill-creator.
4. **QA.** Full `trpa-dashboard-qa` pass for apps. Numbers spot-checked against source for everything.
5. **Beta.** Four weeks with the department on real work, start date written in the intake doc.
6. **Graduate or archive.** At the decision date the department commits a named owner and the tool is promoted, or it is archived and removed from `apps.json`. The decision and reason go in the intake doc. No zombie betas.

## Rules

- One engagement per department at a time.
- The intake doc is the record: decisions, dates, and the final call live there.
- Success is measurable before the build starts: hours saved, errors removed, a step eliminated.
- A problem that needs data a static page cannot reach gets a different container, decided at intake, not discovered after the prototype.

## Pairs with

- `trpa-dashboard-stack` and a brand skill for the build
- `trpa-dashboard-qa` for the QA role
- `trpa-data-services` for where the data lives and how to reach it
