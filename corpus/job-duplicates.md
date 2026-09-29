---
id: job-duplicates
version: 1
title: Duplicate scheduled jobs
---
# Duplicate scheduled jobs

## Duplicate job checks
Check the scheduler lease owner and the idempotency key on each duplicate Northstar job. The scheduler lease duration is 90 seconds; two active lease owners indicate a lease coordination fault.

Consumers must store the job idempotency key before applying a side effect. Replaying a job without a recorded key risks duplicate work; ask the job owner to reconcile the synthetic job IDs.

## Verification and handover
Before starting, record the fictional environment, service name, release revision and incident timestamp. Match the dashboard window to the reported symptom and compare an affected instance with a healthy instance when possible. Preserve the diagnostic observation before a restart or rollout removes it. Use synthetic identifiers in the incident record and exclude customer payloads, real credentials and private keys.

This runbook gives an investigation and an approval path. It does not authorize an assistant to execute commands, modify infrastructure or make a production change. The owning on-call must approve a correction through the normal change workflow. When observations contradict the expected pattern, keep the incident open and ask the owner for further evidence.

After an approved correction, repeat the same synthetic check and observe the service for ten minutes. Record the before and after measurements, the change revision and whether any new symptom appeared. Ask the next responder to verify the recovery observation independently. If recovery cannot be established, hand over the outstanding question and the exact document ID and version. Add verified follow-up guidance only after the service owner reviews it.
