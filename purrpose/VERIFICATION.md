# First increment verification

24 October 2026 · Windows · local working tree based on `5a8a208`, with uncommitted changes. No external requests or inference calls.

Executed from repository root:

```text
python -m unittest purrpose.test_core -v
python -m purrpose --output ../outputs/purrpose/core-increment
git diff --check
```

The actual Python executable was the locally bundled Codex Python 3.12.14 runtime; the commands above use `python` for portability. Record your interpreter/version when reproducing.

**18 tests passed.** Covered behaviors:

- Sufficient evidence skips dispute resolution; ambiguous evidence changes the plan and uses a new source; exhaustion preserves an unknown remainder without a human ticket.
- Included versus separate grants; zero remainder is not misconduct; negative/string/bool/null amounts rejected.
- Wrong-case medical material rejected; date-only funding age valid at seven days and rejected beyond/future dates.
- Synthetic incomplete risk profile and active hold block qualification.
- Task/source/repair caps; cancellation; stale return rejection; unsupported citations; contradictory update without an explicit supersession basis rejected.
- Repeating a completed review does not repeat work; non-synthetic input rejected; report text escaped.

CLI results actually observed:

| Scenario | Disposition | Remaining minor CAD units | Repair rounds |
|---|---|---|---|
| complete | completed | 100000 | 0 |
| repair | completed | 100000 | 1 |
| exhausted | pending_evidence | null | 1 |

These tests cover selected behaviors related to A01/A03/A04/A06/A08/A11 and resource safeguards, not the complete acceptance rows. In particular, A08 restoration authority is only protected by leaving fixture holds active; no human restoration workflow exists yet. A full acceptance pass requires its complete setup and observed outputs. Concurrency, H-MEM persistence, live inference, live data, real donation-channel checks, region-profile validation, historical cutoffs and a complete operator queue were not tested or implemented here.

The report was also opened with headless Chrome: three scenario sections present, no page errors and no horizontal overflow at a 390-pixel viewport. The desktop screenshot was visually inspected. This browser check is separate from the 18 core tests.

The generated report records actual program decisions over synthetic sources. No claim of real-world case verification or model autonomy is made. No API-key files are included. Nothing was pushed or deployed.
