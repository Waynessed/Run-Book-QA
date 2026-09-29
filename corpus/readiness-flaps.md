---
id: readiness-flaps
version: 1
title: Readiness probe flapping
---
# Readiness probe flapping

## Probe checks
For flapping Northstar readiness probes, inspect /ready latency and dependency health in the same window. The probe timeout is two seconds and failureThreshold is three.

Check whether an overloaded database causes probe timeouts. Keep readiness separate from liveness; an unhealthy dependency should remove traffic eligibility without repeatedly killing a healthy process.

## Verification and handover
Before starting, record the fictional environment, service name, release revision and incident timestamp. Match the dashboard window to the reported symptom and compare an affected instance with a healthy instance when possible. Preserve the diagnostic observation before a restart or rollout removes it. Use synthetic identifiers in the incident record and exclude customer payloads, real credentials and private keys.

This runbook gives an investigation and an approval path. It does not authorize an assistant to execute commands, modify infrastructure or make a production change. The owning on-call must approve a correction through the normal change workflow. When observations contradict the expected pattern, keep the incident open and ask the owner for further evidence.

After an approved correction, repeat the same synthetic check and observe the service for ten minutes. Record the before and after measurements, the change revision and whether any new symptom appeared. Ask the next responder to verify the recovery observation independently. If recovery cannot be established, hand over the outstanding question and the exact document ID and version. Add verified follow-up guidance only after the service owner reviews it.
