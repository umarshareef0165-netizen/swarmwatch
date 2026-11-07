# SUBMISSION.md — Swarm Alignment Hackathon submission checklist

**Deadline: Sun Nov 8, 2026, 11:59 PM AoE = Mon Nov 9, 3:59 AM PST.**
Registration already done ("You're signed up", invite code `je7jbkhx`, solo, online).
Resubmission with the same title before the deadline **replaces** the earlier one.

## Form field values (exact)

| Field | Value |
|---|---|
| Project title | SwarmWatch: Detecting and Stopping Emergent Rogue Coordination in Multi-Agent Systems |
| Project summary | A deterministic multi-agent simulation reproducing the swarm-coordination incident pattern (shared folder → message board → task split → coordinator → identity rotation → log scrubbing → quorum breach), plus SwarmWatch: 5 detectors on observable traces only and a latching 3-part mitigation (channel quarantine, board rotation, endpoint freeze pending human review). Measured over 38 runs: unmonitored swarm breaches 5/5 (mean tick 9.2); monitor-only still breaches 5/5 despite detection in 0.8 ticks; monitor + mitigation blocks 5/5 and 18/18 in the sweep, with 0 false positives and benign completion at 100%. Detection is fast — detection alone is not enough. |
| PDF report | `SwarmWatch-Report.pdf` (7 pages; main body 5 pages — within the 8-page limit excl. references/appendices; 22 KB, under the 25 MB limit; abstract 201 words, within 150–250) |
| Publishing interest | **⚠️ DECISION NEEDED — parent/user decides Yes/No. Do NOT decide this here.** (Yes = Apart may publish the report; No = keep it private. No default assumed.) |
| Tracks | **T4** Multi-Agent Oversight and Control + **T1** Sandboxes and Testbeds |
| Team name | Umar Shareef (REQUIRED even solo) |
| Location | Online |
| Team member 1 | Umar Shareef, umarshareef0165@gmail.com |
| GitHub repo (optional) | https://github.com/umarshareef0165-netizen/swarmwatch — **DOES NOT EXIST YET**; create + push before submitting (see below) |
| Video demo (optional) | Not recorded yet — see DEMO-SCRIPT.md (3–5 min, Umar's voice). Optional; submit without it if time is short. |
| Slides / project image (optional) | None prepared; skip. |

## What still needs the browser (parent agent — I cannot do this)

1. **Create the GitHub repo** `swarmwatch` (public) under `umarshareef0165-netizen`
   and push `~/workspace/swarm-alignment-hackathon/` (code + results + report).
   No VM GitHub auth exists — browser push only, ≤15 files per batch.
   The PDF's "Code and data" line points at this URL, so push **before** submitting
   the form, or the link will 404 for judges.
2. **Decide publishing interest** (Yes/No) — needs the user/parent call.
3. **Upload the PDF + submit the form** on the Apart sprint submission page.
4. (Optional) Record the demo video per DEMO-SCRIPT.md and attach its link.

## What needs nothing from Umar

- Nothing. The report, code, tests, and results are complete. The only optional
  Umar step is the demo video (his voice); the submission stands without it.

## Pre-submit verification checklist (for the parent)

- [ ] Repo `swarmwatch` exists, is public, and contains `swarmwatch/`, `experiments/`,
      `tests/`, `results/`, `REPORT-DRAFT.md`, `SwarmWatch-Report.pdf`, `README.md`.
- [ ] Open the uploaded PDF once and confirm it renders (7 pages, tables intact).
- [ ] Publishing interest decided (Yes/No).
- [ ] Verify the reference arXiv IDs in the PDF (Dafoe 2012.08630, Baker 1909.07528,
      Meinke 2412.04984, Irving 1805.00899, Bai 2212.08073) against live arXiv pages.
      They are high-confidence but were not live-checked during the build.
- [ ] Confirm the prize framing in the form/report: global cash pool **$4,000**
      (the "$8,000 total" figure combines the separate $4,000 LA-hub in-person pool;
      Umar is online-only, so only the $4,000 global pool applies to him).
- [ ] Submit before Sun Nov 8, 11:59 PM AoE. Resubmission with the same title
      replaces the earlier one if a fix is needed afterwards.

## Files ready to submit

- `SwarmWatch-Report.pdf` — the report (this folder)
- `REPORT-DRAFT.md` — full report text (Markdown source)
- `README.md` — run instructions + results
- `DEMO-SCRIPT.md` — optional video shot list
- `results/dashboard.html`, `results/metrics.md`, `results/aggregate.json`,
  `results/all_runs.json` — measured evidence
