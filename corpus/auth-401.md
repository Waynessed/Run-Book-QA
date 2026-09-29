---
id: auth-401
version: 1
title: API authentication after deployment
---
# API authentication after deployment

## Authentication checks
Check that the deployed Northstar API has AUTH_ISSUER=https://identity.northstar.invalid and AUTH_AUDIENCE=northstar-api. A mismatched issuer or audience causes 401 responses after deployment. Compare the active release configuration with the last healthy release. Never paste bearer tokens into an incident ticket.

Confirm that the gateway forwards the Authorization header. Compare token expiry with the API clock; Northstar permits 30 seconds of clock skew. If only new pods fail, check the mounted identity configuration and restart only after correcting it.

A synthetic log example is auth_failed reason=audience_mismatch release=r42. Record the reason, release and pod name without recording the token. Do not disable authentication to restore service. Escalate to the identity on-call if the issuer endpoint is unavailable.

## Verification and handover
This document applies to the fictional Northstar staging and production services. Begin by recording the environment, service name, release revision and incident timestamp. Check the service dashboard over the same time window as the reported symptom. Compare an affected replica with a healthy replica when one is available. A single isolated log line is a clue and does not establish the cause of the incident.

Use a read-only investigation first. Any proposed service change needs the owning on-call and the normal change procedure. This runbook describes checks and approval paths; it does not authorize the assistant to execute commands or change infrastructure. Preserve observations before restarting a process because restarts can remove transient evidence.

After the owner applies a correction, repeat the original synthetic request and watch the relevant service counters for ten minutes. Record whether the original symptom disappeared, whether another symptom appeared, and what evidence supports recovery. If the check fails, keep the incident open and hand over the recorded observations to the next responder. The scribe should add the exact source document ID and version to the incident record.
