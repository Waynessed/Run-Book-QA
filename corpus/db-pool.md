---
id: db-pool
version: 2
title: Database connection exhaustion
---
# Database connection exhaustion

## Pool checks
Check active and idle connections in pg_stat_activity and compare them with max_connections. Northstar API uses a pool maximum of 6 connections per replica. Multiply the pool maximum by the replica count and reserve 20 database connections for operations.

Look for idle-in-transaction sessions and missing connection release paths. Record query age, application name and transaction state. Do not terminate all database sessions; ask the database on-call to review a specific stuck session.

A synthetic alert is pool_wait_ms=5000 api_replicas=12 pool_max=10 db_max=100. This configuration exceeds the connection budget. Reduce application pool demand through an approved release and check that wait time falls. Increasing max_connections requires a separate capacity review.

## Verification and handover
This document applies to the fictional Northstar staging and production services. Begin by recording the environment, service name, release revision and incident timestamp. Check the service dashboard over the same time window as the reported symptom. Compare an affected replica with a healthy replica when one is available. A single isolated log line is a clue and does not establish the cause of the incident.

Use a read-only investigation first. Any proposed service change needs the owning on-call and the normal change procedure. This runbook describes checks and approval paths; it does not authorize the assistant to execute commands or change infrastructure. Preserve observations before restarting a process because restarts can remove transient evidence.

After the owner applies a correction, repeat the original synthetic request and watch the relevant service counters for ten minutes. Record whether the original symptom disappeared, whether another symptom appeared, and what evidence supports recovery. If the check fails, keep the incident open and hand over the recorded observations to the next responder. The scribe should add the exact source document ID and version to the incident record.
