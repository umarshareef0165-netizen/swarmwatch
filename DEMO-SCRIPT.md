# DEMO-SCRIPT.md — SwarmWatch optional video (3–5 min)

**Status: OPTIONAL.** The submission is the research report PDF; a video is not
required. Record this only if there is time — it strengthens Presentation &
Clarity. Umar's own voice, no TTS. Screen-record the terminal + dashboard.

## Setup (before recording)

1. `cd ~/workspace/swarm-alignment-hackathon`
2. Open `results/dashboard.html` in a browser tab (keep it behind the terminal).
3. Have `results/metrics.md` open in an editor for the numbers.

## Shots (total ~3:30)

| Time | Shot | Say / show |
|---|---|---|
| 0:00–0:25 | Terminal: `ls swarmwatch/` + one-line concept | "SwarmWatch — what happens when AI agents start coordinating behind your back, and how to catch and stop it. 24 agents, one shared folder, one restricted endpoint." |
| 0:25–1:00 | `python3 -m unittest discover -s tests -v` | "18 tests, all passing — detectors, simulation, mitigation." Scroll the output briefly. |
| 1:00–2:00 | `python3 experiments/run_all.py` (let it run; it takes ~3 s) | Point at the arm lines as they print: "Baseline breaches 5 out of 5. Observe-only — the monitor sees everything — still breaches 5 out of 5. Mitigated: zero breaches. Control: zero findings." |
| 2:00–2:45 | Dashboard (`results/dashboard.html`) | Show the Runs table: breach ticks 8–10, detection latency 0.8, mitigation tick 3. Scroll to Findings: log scrub fires first (tick 2–5), coordinator last (tick 8–9). "The window from first signal to breach is about five ticks — a human can't respond in time, so the mitigation has to latch automatically." |
| 2:45–3:15 | `results/metrics.md` + sweep lines | "Sweep: 18 runs, swarm sizes 12 to 48, up to half the agents curious — 18 out of 18 blocked, zero false positives, benign work at 100%." |
| 3:15–3:30 | Close on the PDF (`SwarmWatch-Report.pdf`, 7 pages) | "Full report, every number reproduced by that one command. SwarmWatch — detection is fast, but only a latching mitigation stops the swarm." |

## Honesty rules for the video

- Say the agents are **seeded policy agents, not LLMs** (one line in the intro is enough — e.g. "a deterministic simulation of the incident pattern").
- Do not claim the repo link is live until it actually is (the PDF says "to be published").
- Numbers on screen must match `results/aggregate.json` exactly — they do, because the script runs the same command.
