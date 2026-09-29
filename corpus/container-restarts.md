---
id: container-restarts
version: 1
title: Container restart investigation
---
# Container restart investigation

## Restart checks
Inspect the previous container logs and the last termination reason. OOMKilled means the memory limit was exceeded; compare peak memory with the configured limit. Exit code 137 alone is not proof of an application bug.

Check whether the liveness probe fails before startup completes. Northstar worker initialization can take 45 seconds; use the startup probe with a 60-second allowance. Do not increase the liveness frequency during an incident.

A synthetic event is worker-7 OOMKilled limit=512Mi peak=540Mi. Preserve that event and the previous logs. Roll back a new release if memory growth begins with that release. Confirm restart counts stop increasing before closing the incident.

## Verification and handover
This document applies to the fictional Northstar staging and production services. Begin by recording the environment, service name, release revision and incident timestamp. Check the service dashboard over the same time window as the reported symptom. Compare an affected replica with a healthy replica when one is available. A single isolated log line is a clue and does not establish the cause of the incident.

Use a read-only investigation first. Any proposed service change needs the owning on-call and the normal change procedure. This runbook describes checks and approval paths; it does not authorize the assistant to execute commands or change infrastructure. Preserve observations before restarting a process because restarts can remove transient evidence.

After the owner applies a correction, repeat the original synthetic request and watch the relevant service counters for ten minutes. Record whether the original symptom disappeared, whether another symptom appeared, and what evidence supports recovery. If the check fails, keep the incident open and hand over the recorded observations to the next responder. The scribe should add the exact source document ID and version to the incident record.
