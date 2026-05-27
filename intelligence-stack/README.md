# Intelligence Stack

## Purpose

This folder translates the useful parts of the ExO / AI-native organization model into this Business Pod.

It does not replace existing systems. It names how they fit together:

- Purpose layer: why the business exists and what constraints matter.
- Sensing layer: what Hermes watches continuously.
- Interpretation layer: what the signals mean.
- Decision layer: what should be changed.
- Orchestration layer: who/what does the work.
- Learning layer: how the system gets better after each cycle.
- Governance wrapper: approvals, evals, logs, compliance, rollback.
- Edge Digital Twin: a parallel AI-native version of a workflow tested before live migration.

## No Duplicate Agent Passport System

Profile authority already lives in the profile creation / permission model.

Do not create a second "agent passport" system unless Hermes needs a machine-readable permissions registry later.
