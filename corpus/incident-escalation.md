---
id: incident-escalation
version: 1
title: Incident escalation and ownership
---
# Incident escalation and ownership

## Escalation checks
Escalate a customer-facing outage immediately to the Northstar incident commander. For a sustained API error rate above 5 percent over five minutes, declare a severity-two incident. Page the owning service on-call and appoint a scribe.

Record impact, start time, affected services and the latest verified observation. Use the incident channel for updates every fifteen minutes. Route authentication failures to identity, connection exhaustion to database, and failed rollouts to the release on-call.

If the runbooks do not cover the situation, state that the evidence is insufficient and contact the owning on-call. Do not guess a production change. Record the unanswered question so that the owner can add verified guidance after the incident.

## Verification and handover
This document applies to the fictional Northstar staging and production services. Begin by recording the environment, service name, release revision and incident timestamp. Check the service dashboard over the same time window as the reported symptom. Compare an affected replica with a healthy replica when one is available. A single isolated log line is a clue and does not establish the cause of the incident.

Use a read-only investigation first. Any proposed service change needs the owning on-call and the normal change procedure. This runbook describes checks and approval paths; it does not authorize the assistant to execute commands or change infrastructure. Preserve observations before restarting a process because restarts can remove transient evidence.

After the owner applies a correction, repeat the original synthetic request and watch the relevant service counters for ten minutes. Record whether the original symptom disappeared, whether another symptom appeared, and what evidence supports recovery. If the check fails, keep the incident open and hand over the recorded observations to the next responder. The scribe should add the exact source document ID and version to the incident record.
