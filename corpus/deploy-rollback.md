---
id: deploy-rollback
version: 1
title: Release rollback procedure
---
# Release rollback procedure

## Rollback checks
Use the release console to select the last healthy Northstar API revision. Confirm that the database migration is backward compatible before rolling back. If the release removed a column, stop and ask the database on-call for a recovery plan.

Record the current and target release IDs and the incident ID. Shift canary traffic back to the healthy revision, then roll back the remaining replicas through the release console. Require the incident commander to approve a full rollback.

Watch API error rate and p95 latency for ten minutes after rollback. A synthetic recovery record is release=r41 errors=0.2% p95=180ms. Keep the failed revision logs for follow-up and do not rerun destructive migrations.

## Verification and handover
This document applies to the fictional Northstar staging and production services. Begin by recording the environment, service name, release revision and incident timestamp. Check the service dashboard over the same time window as the reported symptom. Compare an affected replica with a healthy replica when one is available. A single isolated log line is a clue and does not establish the cause of the incident.

Use a read-only investigation first. Any proposed service change needs the owning on-call and the normal change procedure. This runbook describes checks and approval paths; it does not authorize the assistant to execute commands or change infrastructure. Preserve observations before restarting a process because restarts can remove transient evidence.

After the owner applies a correction, repeat the original synthetic request and watch the relevant service counters for ten minutes. Record whether the original symptom disappeared, whether another symptom appeared, and what evidence supports recovery. If the check fails, keep the incident open and hand over the recorded observations to the next responder. The scribe should add the exact source document ID and version to the incident record.
