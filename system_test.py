import unittest
from ine_engine import ScientificDecisionEngine

class TestINEEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ScientificDecisionEngine()

    def test_atomic_structure_selection(self):
        """Test if the engine selects the right instruments for atomic structure goals."""
        goal = "Determine atomic structure of protein."
        result = self.engine.run_experiment_planning(goal)
        self.assertIn("NMR Spectrometer", result['instrument_stack'])
        self.assertGreater(result['confidence_score'], 0.8)

    def test_surface_morphology_selection(self):
        """Test if the engine selects SEM for surface morphology goals."""
        goal = "Analyze surface morphology of a thin film."
        result = self.engine.run_experiment_planning(goal)
        self.assertIn("Scanning Electron Microscope (SEM)", result['instrument_stack'])

    def test_empty_goal(self):
        """Test how the engine handles unknown or empty goals."""
        goal = "Do something irrelevant."
        result = self.engine.run_experiment_planning(goal)
        # Should fall back to default or generic stack
        self.assertIsInstance(result['instrument_stack'], list)

if __name__ == "__main__":
    print("Running INE-Engine System Tests...")
    unittest.main()
