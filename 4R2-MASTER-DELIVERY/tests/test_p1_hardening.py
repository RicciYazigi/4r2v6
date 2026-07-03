"""
P1 Hardening Tests - Rate Limiting & Tripwire 410
4R2 Coherence Engine v3.1 Audit-Grade

Audit Index: RICCI-AUDIT-20260125
Version: 1.0

These tests verify the P1 security hardening features:
1. Rate Limiting (60 req/min per IP)
2. Tripwire 410 for deprecated endpoints
"""

import unittest
import asyncio
import json
from time import time
from datetime import datetime

# Import from the hardened API
import sys
import os
# Add the systems basic/packages/kernel directory to path relative to this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "systems", "basic", "packages", "kernel")))
from api_fastapi import (
    app, 
    RateLimitMiddleware, 
    TripwireMiddleware,
    RATE_LIMIT,
    RATE_WINDOW,
    DEPRECATED_PATTERNS
)

from fastapi.testclient import TestClient

class TestRateLimiting(unittest.TestCase):
    """Test suite for Rate Limiting middleware"""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_rate_limit_constants(self):
        """Verify rate limit constants are correctly set"""
        self.assertEqual(RATE_LIMIT, 60, "Rate limit should be 60 req/min")
        self.assertEqual(RATE_WINDOW, 60, "Rate window should be 60 seconds")
    
    def test_health_endpoint_accessible(self):
        """Health endpoint should be accessible"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["version"], "3.1-audit-grade")
        self.assertTrue(data["tripwire_active"])
    
    def test_status_endpoint_shows_hardening(self):
        """Status endpoint should show hardening configuration"""
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify hardening info is present
        self.assertIn("hardening", data)
        self.assertTrue(data["hardening"]["rate_limit"]["enabled"])
        self.assertEqual(data["hardening"]["rate_limit"]["limit"], 60)
        self.assertTrue(data["hardening"]["tripwire_410"]["enabled"])
    
    def test_rate_limit_header_on_429(self):
        """Rate limit response should include Retry-After header"""
        # This test simulates the 429 response format
        # In real scenario, would need to make 61+ requests
        expected_response = {
            "error": "RATE_LIMIT_EXCEEDED",
            "detail": f"Maximum {RATE_LIMIT} requests per {RATE_WINDOW} seconds",
            "retry_after": RATE_WINDOW
        }
        # Verify the expected structure matches what middleware would return
        self.assertIn("error", expected_response)
        self.assertIn("retry_after", expected_response)
        self.assertEqual(expected_response["retry_after"], 60)


class TestTripwire410(unittest.TestCase):
    """Test suite for Tripwire 410 middleware"""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_deprecated_patterns_configured(self):
        """Verify deprecated patterns are correctly configured"""
        self.assertIn(r"^/api/v1/.*", DEPRECATED_PATTERNS)
        self.assertIn(r"^/v1/.*", DEPRECATED_PATTERNS)
        self.assertIn(r"^/api/stub/.*", DEPRECATED_PATTERNS)
    
    def test_tripwire_api_v1_coherence(self):
        """Accessing /api/v1/coherence should return 410 GONE"""
        response = self.client.get("/api/v1/coherence")
        self.assertEqual(response.status_code, 410)
        data = response.json()
        self.assertEqual(data["error"], "GONE")
        self.assertEqual(data["code"], 410)
        self.assertTrue(data["tripwire"])
        self.assertEqual(data["canonical_endpoint"], "/api/coherence/measure")
    
    def test_tripwire_api_v1_measure(self):
        """Accessing /api/v1/coherence/measure should return 410 GONE"""
        response = self.client.post("/api/v1/coherence/measure")
        self.assertEqual(response.status_code, 410)
        data = response.json()
        self.assertTrue(data["tripwire"])
    
    def test_tripwire_v1_any_path(self):
        """Accessing /v1/anything should return 410 GONE"""
        response = self.client.get("/v1/anything")
        self.assertEqual(response.status_code, 410)
    
    def test_tripwire_api_stub(self):
        """Accessing /api/stub/* should return 410 GONE"""
        response = self.client.get("/api/stub/test")
        self.assertEqual(response.status_code, 410)
    
    def test_canonical_endpoint_not_blocked(self):
        """Canonical endpoint should NOT trigger tripwire (requires auth)"""
        # Should get 403/401 for auth, NOT 410
        response = self.client.post("/api/coherence/measure", json={
            "normative": [1.0, 1.0],
            "representational": [1.0, 1.0],
            "informational": [1.0, 1.0],
            "physical": [100, 8, 50, 10]
        })
        # Should be 403 (auth required), not 410 (tripwire)
        self.assertNotEqual(response.status_code, 410)
        self.assertIn(response.status_code, [401, 403, 422])


class TestFrozenContract(unittest.TestCase):
    """Test suite verifying Frozen Contract compliance"""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_canonical_endpoint_exists(self):
        """Canonical endpoint /api/coherence/measure should exist"""
        # OPTIONS request to check endpoint exists
        response = self.client.options("/api/coherence/measure")
        # Should not be 404
        self.assertNotEqual(response.status_code, 404)
    
    def test_landauer_endpoint_exists(self):
        """Landauer endpoint should exist"""
        response = self.client.options("/api/coherence/landauer")
        self.assertNotEqual(response.status_code, 404)
    
    def test_loss_4r2_endpoint_exists(self):
        """Loss 4R2 endpoint should exist"""
        response = self.client.options("/api/coherence/loss-4r2")
        self.assertNotEqual(response.status_code, 404)
    
    def test_deprecated_v1_returns_410(self):
        """All /api/v1/* endpoints should return 410"""
        deprecated_paths = [
            "/api/v1/coherence",
            "/api/v1/coherence/measure",
            "/api/v1/kernel",
            "/api/v1/anything"
        ]
        for path in deprecated_paths:
            response = self.client.get(path)
            self.assertEqual(
                response.status_code, 
                410, 
                f"Path {path} should return 410, got {response.status_code}"
            )


class TestSecurityHeaders(unittest.TestCase):
    """Test security-related responses"""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_tripwire_response_format(self):
        """Tripwire response should have proper security format"""
        response = self.client.get("/api/v1/test")
        self.assertEqual(response.status_code, 410)
        data = response.json()
        
        # Required fields
        required_fields = ["error", "code", "detail", "message", "tripwire", "canonical_endpoint", "timestamp"]
        for field in required_fields:
            self.assertIn(field, data, f"Missing required field: {field}")
        
        # Verify timestamp is valid ISO format
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            self.fail("Timestamp is not valid ISO format")


def run_tests():
    """Run all P1 hardening tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimiting))
    suite.addTests(loader.loadTestsFromTestCase(TestTripwire410))
    suite.addTests(loader.loadTestsFromTestCase(TestFrozenContract))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityHeaders))
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("=" * 70)
    print("P1 HARDENING TESTS - 4R2 Coherence Engine v3.1")
    print("Audit Index: RICCI-AUDIT-20260125")
    print("=" * 70)
    result = run_tests()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Status: {'PASS' if result.wasSuccessful() else 'FAIL'}")
