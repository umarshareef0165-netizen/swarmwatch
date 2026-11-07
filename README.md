# SwarmWatch — Swarm Alignment Hackathon (Apart Research)

**SwarmWatch: Detecting and Stopping Emergent Rogue Coordination in Multi-Agent Systems**
Author: Umar Shareef (University of Agriculture Faisalabad, BSCS) — solo.
Tracks: **T4** Multi-Agent Oversight and Control (primary) + **T1** Sandboxes and Testbeds.
Submission: research report PDF + form. Deadline: **Sun Nov 8, 2026, 11:59 PM AoE** (= Mon Nov 9, 3:59 AM PST).

## The idea in one paragraph

A swarm of 24 agents does a document-summarisation task. Six turn curious: they
discover a shared folder, turn it into a message board, split the document set
between themselves, elect a coordinator, hide behind multiple identities, scrub
their logs — and together breach a restricted endpoint that needs a 5-agent
quorum. **SwarmWatch** watches only observable traces (the board, the agents'
presented logs, a hash-chained audit log) with 5 detectors, and on the first HIGH
finding latches a 3-part mitigation: quarantine the channel, rotate the board,
freeze the endpoint pending human review. Detection is fast (0.8 ticks) but
detection alone changes nothing — the observe-only swarm still breaches 5/5.
Mitigation blocks it 5/5, and 18/18 in the sweep, with zero false positives and
benign work untouched.

## Measured results (all reproduced by `python3 experiments/run_all.py`)

| Arm | Breach | Mean breach tick | Detection latency | Board latency | Findings/run | False positives | Benign completion |
|---|---|---|---|---|---|---|---|
| A baseline (no monitor) | 5/5 | 9.2 | — | — | 0 | 0 | 1.00 |
| B observe-only | 5/5 | 9.2 | 0.8 ticks | 1.0 | 5.6 | 0 | 1.00 |
| C mitigated | **0/5** | — | 0.8 ticks | 1.2 | 5.2 | 0 | 1.00 |
| D control (benign-only) | 0/5 | — | — | — | 0 | 0 | 1.00 |
| S sweep (18 runs, N 12–48) | **0/18** | — | 1.06 | 1.28 | 4.28 | 0 | 1.00 |

- First board signal → breach: ~5.4 ticks. Incident start (mean tick 2.2) → breach: ~7 ticks.
- Fastest detector: log scrub (mean tick 3.7, 10/10 possible — 2 scrubbers × 5 runs).
  Slowest: coordinator (mean tick 8.3–9.5) — by then the breach is one tick away.
- Mitigation fires at mean tick 3.0 (range 2–4). A timed 25-tick freeze was tried
  first and **failed** (seed 0: the swarm waited it out and breached after expiry) —
  the shipped freeze has no auto-expiry; it holds pending human review.
- 38 runs total (20 arm + 18 sweep), **0 false positives** anywhere.

## Run it

```bash
cd ~/workspace/swarm-alignment-hackathon
python3 -m unittest discover -s tests -v        # 18 tests
python3 experiments/run_all.py                   # 4 arms x 5 seeds + 18-run sweep
python3 build_pdf.py                             # rebuilds SwarmWatch-Report.pdf
```

Outputs: `results/all_runs.json`, `results/aggregate.json`,
`results/dashboard.html` (self-contained), `results/metrics.md`.
Python 3.12, standard library only — except `reportlab` for the PDF
(`pip install --break-system-packages reportlab`; reinstall if the VM restarts,
`/usr/local` is ephemeral).

## Layout

```
swarmwatch/
  env.py        Workspace, hash-chained AuditLog, SharedBoard (quarantine),
                RestrictedResource (quorum K in window W, freeze)
  agents.py     BenignAgent; CuriousAgent (discover -> probe -> claim ->
                ready -> breach; hydra rotates 5 aliases; 2 scrubbers)
  monitor.py    5 detectors on observable traces only (covert channel,
                task split, coordinator, identity multiplicity, log scrub)
  mitigation.py Latching 3-part mitigation (quarantine + rotate + freeze)
  simulate.py   run() / run_many(), metrics, ground-truth FP scoring
  report.py     JSON / HTML dashboard / Markdown metrics export
experiments/run_all.py   4 arms x 5 seeds + 18-run sweep
tests/          18 unit + E2E tests
results/        measured outputs (JSON, dashboard, metrics)
REPORT-DRAFT.md    Full report text (Markdown)
SwarmWatch-Report.pdf  Submission PDF (7 pages; main body 5 pages, within
                       the 8-page limit excl. references/appendices; 22 KB)
build_pdf.py       PDF builder (reads results/*.json — numbers are measured)
DEMO-SCRIPT.md     Optional 3-5 min video shot list
SUBMISSION.md      Exact form field values + what is still needed to submit
```

## Honesty notes (also in the report's Limitations appendix)

- Agents are **deterministic, seeded policy agents — not LLMs**. Behaviour is
  scripted to reproduce the incident pattern from the sprint page. The experiment
  measures whether coordination can be **detected and stopped**, not whether an
  LLM would spontaneously do this.
- No API keys, no network, no paid services. Nothing to configure.
- The report PDF's code link (`github.com/umarshareef0165-netizen/swarmwatch`)
  points to a repo that does **not exist yet** — it must be created and the code
  pushed before submission (see SUBMISSION.md).
```

## Files

- [REPORT-DRAFT.md](sandbox:/workspace/swarm-alignment-hackathon/REPORT-DRAFT.md)
- [SwarmWatch-Report.pdf](sandbox:/workspace/swarm-alignment-hackathon/SwarmWatch-Report.pdf)
- [README.md](sandbox:/workspace/swarm-alignment-hackathon/README.md)
- [DEMO-SCRIPT.md](sandbox:/workspace/swarm-alignment-hackathon/DEMO-SCRIPT.md)
- [SUBMISSION.md](sandbox:/workspace/swarm-alignment-hackathon/SUBMISSION.md)
- [results/dashboard.html](sandbox:/workspace/swarm-alignment-hackathon/results/dashboard.html)
- [results/metrics.md](sandbox:/workspace/swarm-alignment-hackathon/results/metrics.md)
- [results/aggregate.json](sandbox:/workspace/swarm-alignment-hackathon/results/aggregate.json)
