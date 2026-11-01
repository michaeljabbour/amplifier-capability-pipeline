---
name: pipeline
description: "Turn a project\u2019s actual build and release needs into a reviewable pipeline across CI platforms. Use when asked to create, audit, repair or migrate a build/test/release pipeline."
---

# Pipeline

Scout the actual manifests, lockfiles, tests, release process and existing CI before choosing jobs. Record supported commands, runtime versions, artifact consumers and secrets by name only. Do not add deployment because a build pipeline was requested.

Design: read references/apr-schema.md and references/project-profile.md. Write an Abstract Pipeline Representation (APR) before platform syntax when migrating or targeting several platforms. Capture stage/job dependencies, timeouts, triggers, artifacts, environments and required secret names. Use scripts/apr.py APR.json to check the JSON subset of APR 1.0 for reference errors, cycles, missing timeouts and undeclared secrets. It does not validate arbitrary YAML or prove the pipeline can run.

Generate: read only the selected platform reference directory: references/platforms/github-actions, gitlab-ci or azure-devops. Render APR into native config, inspect permissions, untrusted pull-request paths, action/image pinning and the deployment approval boundary. Use the platform's actual validator or runner when available. Explain any unchecked native feature.

Audit: compare the APR and live config for drift; preserve platform idioms when they are deliberate. Test changes in a disposable branch or local runner before changing production triggers. A generated file, a syntax pass, a green run and an accepted deployment are distinct results. Installing this skill does not authorize publishing, provisioning secrets or releasing software.

The original scout/architect/auditor/platform-generator agents and automation recipes remain optional Amplifier adapters. They carry the original platform-specific mechanisms; the portable method and schema work in an ordinary coding agent.

## Optional coaching checkpoint

Read [the local coaching guide](references/coaching-session.v1.md) only when the person asks for practice or optional session bookkeeping. Keep direct artifact production available; agree a small budget, preserve the baseline and stop on goal, user exit or no meaningful gain.
