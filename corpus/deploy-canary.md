---
id: deploy-canary
version: 1
title: Canary release gates
---
# Canary release gates

## Canary gates
Keep the Northstar API canary at 5 percent of traffic for ten minutes. Expand only if its error rate stays below 1 percent and p95 latency stays within 20 percent of the healthy release.

If either canary gate fails, return traffic to the healthy release and ask the release owner to review the new revision. Keep current and target revision IDs in the change record.

## Verification and handover
Before starting, record the fictional environment, service name, release revision and incident timestamp. Match the dashboard window to the reported symptom and compare an affected instance with a healthy instance when possible. Preserve the diagnostic observation before a restart or rollout removes it. Use synthetic identifiers in the incident record and exclude customer payloads, real credentials and private keys.

This runbook gives an investigation and an approval path. It does not authorize an assistant to execute commands, modify infrastructure or make a production change. The owning on-call must approve a correction through the normal change workflow. When observations contradict the expected pattern, keep the incident open and ask the owner for further evidence.

After an approved correction, repeat the same synthetic check and observe the service for ten minutes. Record the before and after measurements, the change revision and whether any new symptom appeared. Ask the next responder to verify the recovery observation independently. If recovery cannot be established, hand over the outstanding question and the exact document ID and version. Add verified follow-up guidance only after the service owner reviews it.
