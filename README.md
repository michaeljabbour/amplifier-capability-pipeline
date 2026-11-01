# Pipeline

Build the pipeline your project actually needs.

Watch the [72-second film](https://michaeljabbour.github.io/amplifier-capability-pipeline/#film): a template that ships a release nobody asked for, and how the skill builds only the pipeline you need. The example in it is fictional.

For developers creating, repairing or moving CI. Pipeline starts with your real commands and artifact consumers, makes job dependencies reviewable and then generates configuration for the selected platform.

[Explore the site](https://michaeljabbour.github.io/amplifier-capability-pipeline/)

## What you get

- **Start with working commands.** Read manifests, lockfiles and existing tests before adding a job.
- **See dependencies before syntax.** Use the optional abstract representation to review stages, artifacts, timeouts and secret names across platforms.
- **Keep release boundaries explicit.** Separate a build, a green CI run and an approved deployment so generation does not silently publish anything.

## Start here

```sh
git clone https://github.com/michaeljabbour/amplifier-capability-pipeline.git
cd amplifier-capability-pipeline
python3 scripts/capability.py install --dest ~/.agents/skills
```

This installs the portable method and its packaged references into your agent skill folder. If your host uses another folder, pass that path to `--dest`. Start a new session or use your host’s skill refresh so it can discover the installed skill. Optional native tools are installed separately.

Try this first task:

> Use Pipeline to inspect a fictional Python project and propose a test-and-wheel pipeline for GitHub Actions. Name the real commands and artifact consumer. Include timeouts and minimal permissions. Do not add deployment, secrets or publishing.

## What you need

- Python 3.11 or later for the portable install helper.
- Install the portable skill and stdlib APR checker without a model key.
- Platform references are loaded as needed; the actual CI service and runner remain separate.
- Keep secret values out of the design; name only the required secrets.

## Evidence and limits

The packaged APR checker exercises structural reference and cycle failures. Generated configuration still needs native validation, a real run and separate deployment acceptance.

The worked examples on the site are fictional. They illustrate the output and decisions; they are not user results or measured benefit. See [consolidation and runtime boundaries](docs/CONSOLIDATION.md) for retained interfaces and acceptance scope.

---

## Retained source guide

### amplifier-bundle-cicd

An Amplifier application bundle that designs, generates, audits, and maintains CI/CD pipelines for applications.

## What It Does

Point this bundle at any project and it will:

1. **Detect** your tech stack — languages, frameworks, build tools, test runners, Docker, existing CI configs
2. **Design** a pipeline — choosing stages, jobs, triggers, caching, security scanning, and deployment gating
3. **Generate** native CI/CD configs — GitHub Actions (deep support), GitLab CI, Azure DevOps
4. **Document** the pipeline — what it does, why each stage exists, how to customize
5. **Manage secrets** — configure them when safe, guide you when not
6. **Revisit** later — audit, optimize, migrate, or update as your project evolves

## Four Entry Points

| You say... | The bundle does... |
|---|---|
| "Set up CI/CD for this project" | **Greenfield** — detects your project, designs a pipeline, generates configs |
| "Migrate from Jenkins to GitHub Actions" | **Migration** — analyzes your current pipeline, maps to new platform |
| "My pipeline is slow" | **Optimization** — audits your pipeline, identifies bottlenecks, proposes fixes |
| "Review my pipeline" | **Audit** — analyzes and scores your pipeline against best practices |

## Architecture

The bundle separates **pipeline design** from **platform rendering** using an Abstract Pipeline Representation (APR):

```
Your Project --> Pipeline Scout --> Project Profile
                                        |
                                Pipeline Architect --> APR (platform-agnostic)
                                                        |
                                                Platform Generator --> Native CI/CD Config
```

This means:
- One pipeline design serves multiple platforms
- Migration is just re-rendering an APR to a different platform
- Auditing compares APR intent vs. actual config (drift detection)

## Platforms

| Platform | Support Level |
|---|---|
| GitHub Actions | Deep — full idioms, optimization, validation |
| GitLab CI | Solid — correct configs with platform idioms |
| Azure DevOps | Solid — correct configs with platform idioms |

## Quick Start

```
# Interactive — guided pipeline design
/cicd-explore

# Autonomous — end-to-end, hands-off
"Set up CI/CD for this project, go autonomous"

# Audit only
"Audit my pipeline"
```

## Bundle Structure

```
amplifier-bundle-cicd/
  bundle.md                  -- Thin router (entry point)
  context/
    instructions.md          -- Routing logic and agent reference
    philosophy.md            -- Design principles
    schemas/
      project-profile.md    -- What Pipeline Scout produces
      apr-schema.md          -- Abstract Pipeline Representation
    stages/                  -- Composable stage primitives
    platforms/               -- Platform-specific rendering context
  agents/                    -- Specialized agents
  behaviors/core/            -- Shared context all agents inherit
  modes/                     -- Workflow phase modes
  recipes/                   -- Workflow recipes
```

## License

MIT

## Repository migration

This repository was renamed from `amplifier-skill-pipeline` to `amplifier-capability-pipeline`. Existing installed method names, bundle aliases and native interfaces stay the same. See the [migration guide](https://michaeljabbour.github.io/migration/) and [repository map](https://michaeljabbour.github.io/migration/mapping.json) for source URL updates.

## Optional coaching

For an explicitly requested practice or review checkpoint, use [the local coaching guide](skills/pipeline/references/coaching-session.v1.md). It includes a fictional first task, a baseline, a bounded budget, stop rules and human-reviewed keep/revert. No learner trace is saved by default, and software checks do not establish human learning or outside-user usefulness.
