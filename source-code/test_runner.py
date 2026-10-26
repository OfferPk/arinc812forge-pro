#!/usr/bin/env python3
"""
ARINC812Forge Pro — Automated Unit Test Suite
10 Automated Unit Tests Verifying CAN 2.0B 29-bit Framing, Feeder Power Budgeting,
Dynamic Load Shedding, Food Safety Preservation, ARINC 429 Bus Parity, and Normative Audit Rules.
"""

import unittest
import importlib.util
import os
import sys

# Dynamically import arinc812-cli
spec = importlib.util.spec_from_file_location("arinc812_cli", os.path.join(os.path.dirname(__file__), "arinc812-cli.py"))
arinc812_cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arinc812_cli)
ARINC812CLI = arinc812_cli.ARINC812CLI

class TestARINC812Engine(unittest.TestCase):
    def setUp(self):
        self.cli = ARINC812CLI()

    def test_01_aircraft_galley_metadata(self):
        """Test 1: Verify aircraft registration, galley complex, and AC power bus type."""
        ac = self.cli.aircraft
        self.assertEqual(ac["tailNumber"], "A6-EGA")
        self.assertEqual(ac["type"], "Boeing 777-300ER")
        self.assertIn("G5 Aft Main Galley", ac["galleyComplex"])
        self.assertIn("115VAC 400Hz", ac["electricalBus"])

    def test_02_can_29bit_extended_identifier_packing(self):
        """Test 2: Verify CAN 2.0B 29-bit identifier encoding (Priority, Type, Dest, Source)."""
        # Priority 2, Type 0x05, Dest 0x01, Source 0x11
        can_id = self.cli.encode_can_id(2, 0x05, 0x01, 0x11)
        self.assertLessEqual(can_id, 0x1FFFFFFF)
        self.assertEqual((can_id >> 26) & 0x07, 2)
        self.assertEqual((can_id >> 16) & 0xFF, 0x05)
        self.assertEqual((can_id >> 8) & 0xFF, 0x01)
        self.assertEqual(can_id & 0xFF, 0x11)

    def test_03_gain_device_address_uniqueness(self):
        """Test 3: Verify all 6 GAIN inserts hold unique valid ARINC 812 addresses."""
        addrs = [g["canAddress"] for g in self.cli.gainDevices]
        self.assertEqual(len(addrs), 6)
        self.assertEqual(len(set(addrs)), 6)
        for a in addrs:
            self.assertTrue(0x10 <= a <= 0xFE)

    def test_04_feeder_power_budget_compliance(self):
        """Test 4: Verify Feeder A and B current loads remain within rated capacities."""
        fa = self.cli.powerFeeders["feederA"]
        fb = self.cli.powerFeeders["feederB"]
        self.assertLessEqual(fa["currentKva"], fa["ratedKva"])
        self.assertLessEqual(fb["currentKva"], fb["ratedKva"])
        self.assertGreater(fa["currentKva"], 0)
        self.assertGreater(fb["currentKva"], 0)

    def test_05_food_safety_chiller_preservation(self):
        """Test 5: Verify Priority 1 Chiller is granted power and maintains <= 4.0°C."""
        chiller = next((g for g in self.cli.gainDevices if g["type"] == "CHILLER"), None)
        self.assertIsNotNone(chiller)
        self.assertEqual(chiller["priority"], 1)
        self.assertTrue(chiller["powerGranted"])
        self.assertLessEqual(chiller["temperatureC"], 4.0)

    def test_06_dynamic_load_shedding_hierarchy(self):
        """Test 6: Verify low-priority GAINs (Compactor, Boiler) shed before ovens."""
        compactor = next(g for g in self.cli.gainDevices if g["type"] == "TRASH_COMPACTOR")
        boiler = next(g for g in self.cli.gainDevices if g["type"] == "WATER_BOILER")
        oven1 = next(g for g in self.cli.gainDevices if g["id"] == "GAIN_OVN_01")
        # In current load configuration, high-priority ovens (p=2, p=3) are powered, lower ones idle/shedded
        self.assertTrue(oven1["powerGranted"])
        self.assertFalse(compactor["powerGranted"])
        self.assertFalse(boiler["powerGranted"])

    def test_07_single_generator_cabin_derate(self):
        """Test 7: Verify single-generator mode engages shedding to respect 8.0 kVA cap."""
        self.cli.powerFeeders["singleGeneratorMode"] = True
        self.cli.recompute_loads()
        tot = self.cli.powerFeeders["feederA"]["currentKva"] + self.cli.powerFeeders["feederB"]["currentKva"]
        self.assertLessEqual(tot, 8.0)
        self.assertTrue(self.cli.powerFeeders["sheddingEngaged"])
        # Chiller MUST still be powered
        chiller = next(g for g in self.cli.gainDevices if g["type"] == "CHILLER")
        self.assertTrue(chiller["powerGranted"])

    def test_08_rtca_do160g_power_quality(self):
        """Test 8: Verify AC power feeder voltage and frequency within DO-160G limits."""
        fa = self.cli.powerFeeders["feederA"]
        self.assertTrue(104.0 <= fa["voltageVac"] <= 122.0)
        self.assertTrue(380.0 <= fa["frequencyHz"] <= 420.0)

    def test_09_arinc_429_labels_odd_parity(self):
        """Test 9: Verify ARINC 429 Labels 264 & 265 generation and Bit 32 odd parity."""
        bus = self.cli.generate_arinc429()
        l264 = bus["label264"]
        l265 = bus["label265"]
        self.assertEqual(l264["octal"], "264")
        self.assertEqual(l265["octal"], "265")
        self.assertTrue(l264["parity_valid"])
        self.assertTrue(l265["parity_valid"])
        self.assertEqual(len(l264["binary"]), 32)
        self.assertEqual(len(l265["binary"]), 32)
        self.assertEqual(bin(int(l264["hex"], 16)).count('1') % 2, 1)
        self.assertEqual(bin(int(l265["hex"], 16)).count('1') % 2, 1)

    def test_10_normative_audit_full_pass(self):
        """Test 10: Verify 10-point normative audit reports 10/10 PASS (100.0% compliance)."""
        tests = self.cli.run_audit()
        self.assertEqual(len(tests), 10)
        passed = sum(1 for t in tests if t[3])
        self.assertEqual(passed, 10)
        self.assertTrue(all(t[3] for t in tests))

if __name__ == "__main__":
    unittest.main()
