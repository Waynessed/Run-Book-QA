---
id: monitoring-latency
version: 1
title: API latency investigation
---
# API latency investigation

## Latency checks
Compare Northstar API p50, p95 and p99 latency over the same five-minute window. Split latency by route and release revision. A high p95 with stable p50 suggests a subset of slow requests rather than universal failure.

Inspect database query duration, pool wait time and outbound dependency spans. Compare error rate with latency so that fast failures do not look healthy. Use synthetic trace IDs and never include customer request bodies in screenshots.

A synthetic trace is api=900ms db_wait=650ms query=40ms. This points first to connection pool waiting. Follow the database connection exhaustion runbook and validate the explanation against several traces before changing capacity.

## Verification and handover
This document applies to the fictional Northstar staging and production services. Begin by recording the environment, service name, release revision and incident timestamp. Check the service dashboard over the same time window as the reported symptom. Compare an affected replica with a healthy replica when one is available. A single isolated log line is a clue and does not establish the cause of the incident.

Use a read-only investigation first. Any proposed service change needs the owning on-call and the normal change procedure. This runbook describes checks and approval paths; it does not authorize the assistant to execute commands or change infrastructure. Preserve observations before restarting a process because restarts can remove transient evidence.

After the owner applies a correction, repeat the original synthetic request and watch the relevant service counters for ten minutes. Record whether the original symptom disappeared, whether another symptom appeared, and what evidence supports recovery. If the check fails, keep the incident open and hand over the recorded observations to the next responder. The scribe should add the exact source document ID and version to the incident record.
