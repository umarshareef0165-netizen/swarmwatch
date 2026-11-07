"""End-to-end tests for the SwarmWatch simulation.

Run: python3 -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmwatch.simulate import RunConfig, run


class TestSimulation(unittest.TestCase):
    def test_baseline_breaches(self):
        """No monitor: the swarm coordinates and breaches in most seeds."""
        breached = 0
        for seed in range(5):
            r = run(RunConfig(n_agents=24, n_curious=6, seed=seed,
                              monitor_on=False, mitigation_on=False))
            breached += 1 if r.breach else 0
        self.assertGreaterEqual(breached, 4,
                                f"baseline should breach in >=4/5 seeds, got {breached}/5")

    def test_mitigated_blocks_breach(self):
        """Monitor + mitigation: breach blocked in every seed."""
        for seed in range(5):
            r = run(RunConfig(n_agents=24, n_curious=6, seed=seed,
                              monitor_on=True, mitigation_on=True))
            self.assertFalse(r.breach, f"seed {seed}: breach not blocked")
            self.assertIsNotNone(r.mitigation_tick,
                                 f"seed {seed}: mitigation never triggered")
            self.assertLess(r.mitigation_tick, r.breach_tick or 999,
                            f"seed {seed}: mitigation fired after breach would occur")

    def test_observe_only_detects_but_breaches(self):
        """Detection without mitigation: detectors fire, breach still happens."""
        r = run(RunConfig(n_agents=24, n_curious=6, seed=0,
                          monitor_on=True, mitigation_on=False))
        self.assertTrue(r.breach, "observe-only run should still breach")
        self.assertGreaterEqual(len(r.findings), 3,
                                f"expected >=3 findings, got {len(r.findings)}")
        self.assertIsNotNone(r.detection_latency_ticks)

    def test_control_no_findings(self):
        """Benign-only swarm with monitor on: zero findings, zero false positives."""
        for seed in range(3):
            r = run(RunConfig(n_agents=24, n_curious=0, seed=seed,
                              monitor_on=True, mitigation_on=True))
            self.assertEqual(r.findings, [], f"seed {seed}: unexpected findings")
            self.assertEqual(r.false_positives, 0)
            self.assertFalse(r.breach)

    def test_determinism(self):
        """Same seed -> identical outcome and breach tick."""
        a = run(RunConfig(n_agents=24, n_curious=6, seed=2,
                          monitor_on=True, mitigation_on=True))
        b = run(RunConfig(n_agents=24, n_curious=6, seed=2,
                          monitor_on=True, mitigation_on=True))
        self.assertEqual(a.to_dict(), b.to_dict())

    def test_mitigation_preserves_benign_work(self):
        """Mitigation must not destroy legitimate work: benign completion
        in mitigated runs should stay high."""
        r = run(RunConfig(n_agents=24, n_curious=6, seed=0,
                          monitor_on=True, mitigation_on=True))
        self.assertGreaterEqual(r.benign_completion, 0.8,
                                f"benign completion {r.benign_completion:.2f} too low")

    def test_audit_chain_verifies_after_run(self):
        """The hash-chained log must verify after a full run."""
        from swarmwatch.env import Workspace
        from swarmwatch.agents import build_agents
        ws = Workspace(n_docs=24)
        agents = build_agents(24, 6, 0, 24)
        for t in range(10):
            for ag in agents:
                ag.act(ws, t)
        self.assertTrue(ws.log.verify())


if __name__ == "__main__":
    unittest.main()
