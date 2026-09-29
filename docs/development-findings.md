# Early development findings (run still active)

These are inspected examples, not final aggregate results. The running report is development-20260929T062619Z.pending.json at backend source revision ca7857d. The complete raw report will be saved only after all 120 outputs finish.

| Case / keyword | Observed issue | Why it matters |
|---|---|---|
| dev-a-18 | Correct HTTP 429 fact cited P1 authentication checks instead of P2 rate-limit checks | Membership validation is weaker than semantic support |
| dev-a-06 | Correct HTTP 503 facts cited P1/P2; actual source was P3 | A correct answer can still have unusable supporting citations |
| dev-a-16 | Boilerplate filled the first three candidates; confidence gate abstained | Recall@5 and answerable coverage measure different bottlenecks |
| dev-x-01 | Relevant authentication evidence existed but the generator abstained on a mixed adversarial question | Safe refusal can sacrifice the legitimate supported request |
| dev-a-12 | Source-supported statement about isolated logs did not answer the requested restart check | Supported-claim rate alone cannot establish usefulness/correctness |
| dev-a-02 | Useful supported checks omitted explicit termination-reason investigation | Partial correctness needs a rubric rather than binary keyword scoring |

Annotations are recorded by the implementing assistant as model-assisted semantic inspection. They are not independent human ground truth. No held-out outputs have been used to alter the prompt or threshold. Keep the raw outputs for review and disagreement.
