---
id: image-pull
version: 1
title: Container image pull failures
---
# Container image pull failures

## Image checks
For ImagePullBackOff, inspect the pod events for the exact registry error. A not-found error usually indicates a missing image tag or incorrect repository path. Verify the release manifest points to an immutable digest in the Northstar registry.

For unauthorized errors, check the image pull secret reference and its namespace. Do not display the secret value. Ask the registry owner to rotate expired credentials through the approved secret workflow. Avoid changing the application image to latest.

A synthetic event is FailedPull image=registry.northstar.invalid/api:r42 reason=manifest_unknown. Record the digest expected by the release and the registry owner response. Retry the rollout only after the registry contains the verified artifact.

## Verification and handover
This document applies to the fictional Northstar staging and production services. Begin by recording the environment, service name, release revision and incident timestamp. Check the service dashboard over the same time window as the reported symptom. Compare an affected replica with a healthy replica when one is available. A single isolated log line is a clue and does not establish the cause of the incident.

Use a read-only investigation first. Any proposed service change needs the owning on-call and the normal change procedure. This runbook describes checks and approval paths; it does not authorize the assistant to execute commands or change infrastructure. Preserve observations before restarting a process because restarts can remove transient evidence.

After the owner applies a correction, repeat the original synthetic request and watch the relevant service counters for ten minutes. Record whether the original symptom disappeared, whether another symptom appeared, and what evidence supports recovery. If the check fails, keep the incident open and hand over the recorded observations to the next responder. The scribe should add the exact source document ID and version to the incident record.
