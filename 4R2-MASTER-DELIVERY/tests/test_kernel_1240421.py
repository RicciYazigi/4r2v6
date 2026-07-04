"""
Unit Tests for 4R2 Coherence Kernel 1240421
Author: Ricardo Yazigi
Version: 3.0
"""

import unittest
import numpy as np
# Import from canonical single source of truth
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "core"))
from kernel_1240421 import CoherenceKernel, LayerState, create_kernel, LANDAUER_MIN

class TestCoherenceKernel(unittest.TestCase):
    """Test suite for CoherenceKernel"""
    
    def setUp(self):
        """Initialize kernel for each test"""
        self.kernel = create_kernel(lambda_landauer=0.05, beta_coherence=0.1)
        
        # Create sample states
        self.perfect_state = LayerState(
            normative=np.array([1.0, 1.0, 1.0, 1.0]),
            representational=np.array([1.0, 1.0, 1.0, 1.0]),
            informational=np.array([1.0, 1.0, 1.0, 1.0]),
            physical=np.array([1000, 8, 50, 10])
        )
        
        self.misaligned_state = LayerState(
            normative=np.array([1.0, 0.0, 1.0, 0.0]),
            representational=np.array([0.0, 1.0, 0.0, 1.0]),
            informational=np.array([0.5, 0.5, 0.5, 0.5]),
            physical=np.array([1000, 8, 50, 10])
        )
    
    def test_kernel_initialization(self):
        """Test kernel initializes correctly"""
        self.assertEqual(self.kernel.lambda_landauer, 0.05)
        self.assertEqual(self.kernel.beta_coherence, 0.1)
        self.assertIn('w_NR', self.kernel.weights)
        self.assertIn('w_RI', self.kernel.weights)
        self.assertIn('w_IF', self.kernel.weights)
    
    def test_weights_sum_to_one(self):
        """Test that weights sum to 1.0"""
        weight_sum = sum(self.kernel.weights.values())
        self.assertAlmostEqual(weight_sum, 1.0, places=6)
    
    def test_layer_state_validation(self):
        """Test LayerState validation"""
        valid_state = LayerState(
            normative=np.array([1.0, 1.0]),
            representational=np.array([1.0, 1.0]),
            informational=np.array([1.0, 1.0]),
            physical=np.array([100, 8, 50, 10])
        )
        # Should not raise
        valid_state.validate()
    
    def test_layer_state_validation_fails_on_invalid_physical(self):
        """Test LayerState validation fails with invalid physical layer"""
        invalid_state = LayerState(
            normative=np.array([1.0, 1.0]),
            representational=np.array([1.0, 1.0]),
            informational=np.array([1.0, 1.0]),
            physical=np.array([100, 8, 50])  # Only 3 elements
        )
        with self.assertRaises(AssertionError):
            invalid_state.validate()
    
    def test_compute_C_NR_perfect_alignment(self):
        """Test C_NR with perfectly aligned layers"""
        C_NR = self.kernel.compute_C_NR(
            self.perfect_state.normative,
            self.perfect_state.representational
        )
        # Perfect alignment should give C_NR â‰ˆ 0
        self.assertLess(C_NR, 0.1)
    
    def test_compute_C_NR_misalignment(self):
        """Test C_NR with misaligned layers"""
        C_NR = self.kernel.compute_C_NR(
            self.misaligned_state.normative,
            self.misaligned_state.representational
        )
        # Misalignment should give C_NR > 0
        self.assertGreaterEqual(C_NR, 0.5)
    
    def test_compute_C_RI(self):
        """Test C_RI computation"""
        C_RI = self.kernel.compute_C_RI(
            self.perfect_state.representational,
            self.perfect_state.informational
        )
        self.assertGreaterEqual(C_RI, 0)
        self.assertLessEqual(C_RI, 2.0)
    
    def test_compute_C_IF(self):
        """Test C_IF computation"""
        C_IF = self.kernel.compute_C_IF(
            self.perfect_state.informational,
            self.perfect_state.physical
        )
        self.assertGreaterEqual(C_IF, 0)
        self.assertLessEqual(C_IF, 2.0)  # Consistent with C_NR / C_RI (1 - cos)
    
    def test_compute_coherence_total_perfect(self):
        """Test total coherence with perfect state"""
        C_total, breakdown = self.kernel.compute_coherence_total(self.perfect_state)
        
        self.assertGreaterEqual(C_total, 0)
        self.assertLessEqual(C_total, 2.0)
        self.assertIn('C_NR', breakdown)
        self.assertIn('C_RI', breakdown)
        self.assertIn('C_IF', breakdown)
        self.assertIn('C_total', breakdown)
    
    def test_compute_coherence_total_misaligned(self):
        """Test total coherence with misaligned state"""
        C_total_perfect, _ = self.kernel.compute_coherence_total(self.perfect_state)
        C_total_misaligned, _ = self.kernel.compute_coherence_total(self.misaligned_state)
        
        # Misaligned should have higher (worse) coherence
        self.assertGreater(C_total_misaligned, C_total_perfect)
    
    def test_landauer_cost_normalized(self):
        """Test Landauer cost calculation (normalized)"""
        cost = self.kernel.compute_landauer_cost(decision_changes=5, normalize=True)
        
        expected = 0.05 * 5  # lambda_landauer * decision_changes
        self.assertAlmostEqual(cost, expected, places=6)
    
    def test_landauer_cost_physical(self):
        """Test Landauer cost calculation (physical units)"""
        cost = self.kernel.compute_landauer_cost(decision_changes=5, normalize=False)
        
        expected = 5 * LANDAUER_MIN
        self.assertAlmostEqual(cost, expected, places=30)
    
    def test_landauer_cost_zero_changes(self):
        """Test Landauer cost with zero decision changes"""
        cost = self.kernel.compute_landauer_cost(decision_changes=0, normalize=True)
        self.assertEqual(cost, 0.0)
    
    def test_compute_loss_4r2(self):
        """Test 4â™»ï¸2 loss function"""
        C_total = 0.5
        loss = self.kernel.compute_loss_4R2(
            base_loss=0.5,
            coherence_total=C_total,
            decision_changes=3,
            alpha=0.1,
            gamma=0.05
        )
        
        # Loss should be positive
        self.assertGreater(loss, 0)
        
        # Loss should be > base_loss due to penalties
        self.assertGreater(loss, 0.5)
    
    def test_compute_loss_4r2_perfect_coherence(self):
        """Test 4R2 loss with perfect coherence (CORRECTED SEMANTICS)"""
        loss_perfect = self.kernel.compute_loss_4R2(
            base_loss=0.5,
            coherence_total=0.0,   # Perfect coherence
            decision_changes=0,
            alpha=0.1,
            gamma=0.05
        )
        
        loss_imperfect = self.kernel.compute_loss_4R2(
            base_loss=0.5,
            coherence_total=1.0,   # Bad coherence
            decision_changes=5,
            alpha=0.1,
            gamma=0.05
        )
        
        # With correct semantics (higher C_total = worse):
        # loss_perfect   ≈ 0.5 + 0.1*(0)**2 + 0     = 0.5
        # loss_imperfect ≈ 0.5 + 0.1*(1)**2 + 0.0125 = 0.6125
        self.assertAlmostEqual(loss_perfect, 0.5, places=4)
        self.assertAlmostEqual(loss_imperfect, 0.6125, places=4)
        self.assertGreater(loss_imperfect, loss_perfect)

    
    def test_history_tracking(self):
        """Test that history is tracked"""
        initial_count = len(self.kernel.history)
        
        self.kernel.compute_coherence_total(self.perfect_state)
        self.kernel.compute_coherence_total(self.misaligned_state)
        
        self.assertEqual(len(self.kernel.history), initial_count + 2)
    
    def test_history_reset(self):
        """Test history reset"""
        self.kernel.compute_coherence_total(self.perfect_state)
        self.assertGreater(len(self.kernel.history), 0)
        
        self.kernel.reset_history()
        self.assertEqual(len(self.kernel.history), 0)
    
    def test_get_history_json(self):
        """Test history export to JSON"""
        self.kernel.compute_coherence_total(self.perfect_state)
        
        json_str = self.kernel.get_history_json()
        self.assertIsInstance(json_str, str)
        self.assertIn('C_NR', json_str)
        self.assertIn('C_RI', json_str)
        self.assertIn('C_IF', json_str)
    
    def test_safe_norm(self):
        """Test safe normalization"""
        vec = np.array([3.0, 4.0])
        normalized = self.kernel._safe_norm(vec)
        
        # Norm should be 1.0
        norm = np.linalg.norm(normalized)
        self.assertAlmostEqual(norm, 1.0, places=6)
    
    def test_safe_norm_zero_vector(self):
        """Test safe normalization with zero vector"""
        vec = np.array([0.0, 0.0, 0.0])
        normalized = self.kernel._safe_norm(vec)
        
        # Should not raise, should be finite
        self.assertTrue(np.all(np.isfinite(normalized)))
    
    def test_custom_weights(self):
        """Test kernel with custom weights"""
        custom_weights = {'w_NR': 0.5, 'w_RI': 0.3, 'w_IF': 0.2}
        kernel = create_kernel()
        kernel.weights = custom_weights
        
        C_total, breakdown = kernel.compute_coherence_total(self.perfect_state)
        
        # Verify weights are used
        self.assertEqual(breakdown['weights'], custom_weights)
    
    def test_coherence_bounds(self):
        """Test that coherence values stay within bounds"""
        for _ in range(10):
            random_state = LayerState(
                normative=np.random.rand(4),
                representational=np.random.rand(4),
                informational=np.random.rand(4),
                physical=np.array([1000, 8, 50, 10])
            )
            
            C_total, breakdown = self.kernel.compute_coherence_total(random_state)
            
            self.assertGreaterEqual(C_total, 0)
            self.assertLessEqual(C_total, 2.0)
            self.assertGreaterEqual(breakdown['C_NR'], 0)
            self.assertGreaterEqual(breakdown['C_RI'], 0)
            self.assertGreaterEqual(breakdown['C_IF'], 0)

class TestLayerState(unittest.TestCase):
    """Test suite for LayerState"""
    
    def test_layer_state_creation(self):
        """Test LayerState creation"""
        state = LayerState(
            normative=np.array([1.0, 2.0]),
            representational=np.array([1.0, 2.0]),
            informational=np.array([1.0, 2.0, 3.0, 4.0]),
            physical=np.array([100, 8, 50, 10])
        )
        
        self.assertEqual(len(state.normative), 2)
        self.assertEqual(len(state.representational), 2)
        self.assertEqual(len(state.informational), 4)
        self.assertEqual(len(state.physical), 4)

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_workflow(self):
        """Test complete workflow"""
        kernel = create_kernel()
        
        # Create state
        state = LayerState(
            normative=np.array([0.9, 0.8, 0.7, 0.6]),
            representational=np.array([0.85, 0.75, 0.65, 0.55]),
            informational=np.array([0.8, 0.7, 0.6, 0.5]),
            physical=np.array([1000, 8, 50, 10])
        )
        
        # Measure coherence
        C_total, breakdown = kernel.compute_coherence_total(state)
        
        # Calculate costs
        landauer_cost = kernel.compute_landauer_cost(5)
        
        # Calculate loss
        loss = kernel.compute_loss_4R2(
            base_loss=0.5,
            coherence_total=C_total,
            decision_changes=5
        )
        
        # Verify all outputs are valid
        self.assertIsInstance(C_total, float)
        self.assertIsInstance(landauer_cost, float)
        self.assertIsInstance(loss, float)
        self.assertGreater(loss, 0)



class TestNewModularFeatures(unittest.TestCase):
    """Pruebas unitarias para las extensiones del kernel v5.2."""
    
    def test_belief_tracker_ebbinghaus_decay(self):
        from kernel_1240421 import BeliefTracker
        tracker = BeliefTracker(decay_tau_episodic=10.0)
        
        # Guardar hecho episódico y consultar inmediatamente
        tracker.update([("hecho_1", 0.9, "episodic", "source_1")])
        prob, tag, ts = tracker.query("hecho_1")
        self.assertAlmostEqual(prob, 0.9, places=2)
        self.assertEqual(tag, "episodic")
        
        # Guardar hecho semántico (no tiene decaimiento temporal)
        tracker.update([("hecho_2", 0.8, "semantic", "source_2")])
        prob2, tag2, _ = tracker.query("hecho_2")
        self.assertAlmostEqual(prob2, 0.8, places=2)
        self.assertEqual(tag2, "semantic")
        
    def test_belief_tracker_contradiction(self):
        from kernel_1240421 import BeliefTracker
        tracker = BeliefTracker()
        
        # Registrar hechos contradictorios
        tracker.update([("hecho_A", 0.9, "semantic", "system")])
        tracker.update([("hecho_B", 0.1, "semantic", "system")])
        
        cost = tracker.get_contradiction_cost(["hecho_A", "hecho_B"])
        self.assertGreater(cost, 0.0)
        self.assertAlmostEqual(cost, 0.4, places=2)

    def test_calibrated_evaluator(self):
        from kernel_1240421 import CalibratedEvaluator
        evaluator = CalibratedEvaluator()
        
        # Test temperature scaling
        calibrated = evaluator.calibrate("c1", 1.5)
        self.assertTrue(0.0 <= calibrated <= 1.0)
        
        # Test severity keyword logic
        self.assertEqual(evaluator.get_severity("This is a severe error"), 1.0)
        self.assertEqual(evaluator.get_severity("We should try this first"), 0.6)
        
    def test_domain_kernel(self):
        from kernel_1240421 import DomainKernel
        dk = DomainKernel()
        
        # Detectar dominio
        self.assertEqual(dk.detect_domain("The patient has symptoms of fever"), "medical")
        self.assertEqual(dk.detect_domain("Let's query the API database function"), "technical")
        self.assertEqual(dk.detect_domain("Standard sentence"), "default")
        
        # Pesos asociados
        weights = dk.get_weights("medical")
        self.assertEqual(weights['w_IF'], 0.60)


if __name__ == '__main__':
    unittest.main(verbosity=2)


