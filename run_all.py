"""SwarmWatch experiments: four arms + size/curiosity sweep.

Arms (all N=24 agents, 6 curious = 25%, 5 seeds each):
  A baseline:      monitor OFF, mitigation OFF  (the incident, uninterrupted)
  B observe-only:  monitor ON,  mitigation OFF  (detection without action)
  C mitigated:     monitor ON,  mitigation ON   (detection + structural stop)
  D control:       benign-only swarm, monitor ON, mitigation ON (false positives)

Sweep (monitor ON + mitigation ON, 3 seeds each):
  N in {12, 24, 48} x curiosity in {0.25, 0.5}; quorum scales with swarm
  size (min(5, n_curious)) so small swarms can still breach in baseline.

Outputs (results/): all_runs.json, dashboard.html, metrics.md,
aggregate.json (arm-level means).
"""
from __future__ import annotations

import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmwatch.report import save_dashboard, save_metrics_markdown, save_run_json
from swarmwatch.simulate import RunConfig, run

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, "results")
os.makedirs(RESULTS, exist_ok=True)


def _arm_stats(results):
    def mean(xs):
        return round(statistics.mean(xs), 2) if xs else None
    return {
        "n_runs": len(results),
        "breach_rate": mean([1.0 if r.breach else 0.0 for r in results]),
        "mean_breach_tick": mean([r.breach_tick for r in results if r.breach_tick is not None]),
        "mean_first_signal_tick": mean([r.first_board_signal_tick for r in results
                                        if r.first_board_signal_tick is not None]),
        "mean_detection_latency_ticks": mean([r.detection_latency_ticks for r in results
                                             if r.detection_latency_ticks is not None]),
        "mean_board_detection_latency_ticks": mean(
            [r.board_detection_latency_ticks for r in results
             if r.board_detection_latency_ticks is not None]),
        "mean_findings": mean([len(r.findings) for r in results]),
        "mean_false_positives": mean([r.false_positives for r in results]),
        "mean_task_completion": mean([r.task_completion for r in results]),
        "mean_benign_completion": mean([r.benign_completion for r in results]),
        "mean_mitigation_tick": mean([r.mitigation_tick for r in results
                                      if r.mitigation_tick is not None]),
        "mean_denied_writes": mean([r.denied_writes for r in results]),
    }


def main() -> None:
    all_results = []
    arms: dict[str, list] = {}

    def do(label, **kw):
        cfg = RunConfig(label=label, **kw)
        r = run(cfg)
        all_results.append(r)
        arms.setdefault(label.split(" ")[0], []).append(r)
        print(f"{label}: breach={r.breach} tick={r.breach_tick} "
              f"signal={r.first_board_signal_tick} latency={r.detection_latency_ticks} "
              f"board_latency={r.board_detection_latency_ticks} "
              f"findings={len(r.findings)} fp={r.false_positives} "
              f"task={r.task_completion:.2f} benign={r.benign_completion:.2f} "
              f"mit={r.mitigation_tick}", flush=True)
        return r

    seeds = [0, 1, 2, 3, 4]
    for s in seeds:
        do(f"A baseline s{s}", n_agents=24, n_curious=6, seed=s,
           monitor_on=False, mitigation_on=False)
    for s in seeds:
        do(f"B observe s{s}", n_agents=24, n_curious=6, seed=s,
           monitor_on=True, mitigation_on=False)
    for s in seeds:
        do(f"C mitigated s{s}", n_agents=24, n_curious=6, seed=s,
           monitor_on=True, mitigation_on=True)
    for s in seeds:
        do(f"D control s{s}", n_agents=24, n_curious=0, seed=s,
           monitor_on=True, mitigation_on=True)

    for n in (12, 24, 48):
        for frac in (0.25, 0.5):
            nc = max(1, int(n * frac))
            q = min(5, nc)
            for s in (0, 1, 2):
                do(f"S sweep N{n} c{nc} s{s}", n_agents=n, n_curious=nc, seed=s,
                   quorum=q, monitor_on=True, mitigation_on=True)

    aggregate = {k: _arm_stats(v) for k, v in arms.items()}
    # Sweep rows keyed separately.
    sweep = [r for r in all_results if r.config.label.startswith("S sweep")]
    aggregate["sweep"] = [
        {"label": r.config.label, "n": r.config.n_agents, "curious": r.config.n_curious,
         "seed": r.config.seed, "breach": r.breach, "breach_tick": r.breach_tick,
         "latency": r.detection_latency_ticks,
         "board_latency": r.board_detection_latency_ticks,
         "findings": len(r.findings),
         "fp": r.false_positives, "task": round(r.task_completion, 2),
         "benign": round(r.benign_completion, 2), "mit": r.mitigation_tick}
        for r in sweep]

    with open(os.path.join(RESULTS, "all_runs.json"), "w") as f:
        json.dump([r.to_dict() for r in all_results], f, indent=2, default=str)
    with open(os.path.join(RESULTS, "aggregate.json"), "w") as f:
        json.dump(aggregate, f, indent=2)
    save_dashboard(all_results, os.path.join(RESULTS, "dashboard.html"))
    save_metrics_markdown(all_results, os.path.join(RESULTS, "metrics.md"))

    print("\n=== AGGREGATE ===")
    print(json.dumps(aggregate, indent=2))


if __name__ == "__main__":
    main()
