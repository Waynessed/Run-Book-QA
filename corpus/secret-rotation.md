---
id: secret-rotation
version: 1
title: Application secret rotation
---
# Application secret rotation

## Rotation checks
Rotate the Northstar application secret using the secret manager workflow. Create a new secret version and deploy consumers that can read it before disabling the previous version. Never put secret values in Git, logs or tickets.

Confirm the new version is mounted on every consumer replica. Use secret version identifiers in the rollout checklist and a synthetic authentication check to verify the change. Retain the old version during the approved overlap window of thirty minutes.

After the overlap window, revoke the old secret and verify that clients still authenticate. If any consumer fails, pause revocation and contact the secret owner. Record only version IDs and timestamps in the incident notes.

## Verification and handover
This document applies to the fictional Northstar staging and production services. Begin by recording the environment, service name, release revision and incident timestamp. Check the service dashboard over the same time window as the reported symptom. Compare an affected replica with a healthy replica when one is available. A single isolated log line is a clue and does not establish the cause of the incident.

Use a read-only investigation first. Any proposed service change needs the owning on-call and the normal change procedure. This runbook describes checks and approval paths; it does not authorize the assistant to execute commands or change infrastructure. Preserve observations before restarting a process because restarts can remove transient evidence.

After the owner applies a correction, repeat the original synthetic request and watch the relevant service counters for ten minutes. Record whether the original symptom disappeared, whether another symptom appeared, and what evidence supports recovery. If the check fails, keep the incident open and hand over the recorded observations to the next responder. The scribe should add the exact source document ID and version to the incident record.
