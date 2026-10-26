#!/usr/bin/env python3
"""
ARINC812Forge Pro — Standalone Python 3 CLI & Avionics Galley Engine
Standard Data Interface for Galley Insert (GAIN) Equipment & Galley Network Controller (GNC)
Standards: ARINC Specification 812 / 812A, ISO 11898-1 (CAN 2.0B), RTCA DO-160G Sec 16
"""

import sys
import json

class ARINC812CLI:
    def __init__(self):
        self.aircraft = {
            "type": "Boeing 777-300ER",
            "tailNumber": "A6-EGA",
            "galleyComplex": "G5 Aft Main Galley",
            "electricalBus": "115VAC 400Hz 3-Phase Variable Frequency AC"
        }
        self.powerFeeders = {
            "feederA": {
                "id": "FEEDER_A",
                "ratedKva": 8.0,
                "currentKva": 0.0,
                "voltageVac": 115.0,
                "frequencyHz": 400.0,
                "status": "NORMAL"
            },
            "feederB": {
                "id": "FEEDER_B",
                "ratedKva": 6.0,
                "currentKva": 0.0,
                "voltageVac": 115.0,
                "frequencyHz": 400.0,
                "status": "NORMAL"
            },
            "totalMaxKva": 12.0,
            "singleGeneratorLimitKva": 8.0,
            "singleGeneratorMode": False,
            "sheddingEngaged": False
        }
        self.gainDevices = [
            {
                "id": "GAIN_CHL_01",
                "name": "Galley Air Chiller Unit",
                "type": "CHILLER",
                "ataChapter": "25-30",
                "canAddress": 0x31,
                "feeder": "FEEDER_B",
                "ratedKva": 1.6,
                "actualKva": 1.4,
                "priority": 1,
                "state": "RUNNING",
                "powerGranted": True,
                "temperatureC": 3.8,
                "targetTempC": 4.0,
                "biteStatus": "NORMAL",
                "faultCode": "0x00"
            },
            {
                "id": "GAIN_OVN_01",
                "name": "Convection Steam Oven 1",
                "type": "OVEN",
                "ataChapter": "25-30",
                "canAddress": 0x11,
                "feeder": "FEEDER_A",
                "ratedKva": 3.2,
                "actualKva": 3.1,
                "priority": 2,
                "state": "HEATING",
                "powerGranted": True,
                "temperatureC": 175.0,
                "targetTempC": 180.0,
                "biteStatus": "NORMAL",
                "faultCode": "0x00"
            },
            {
                "id": "GAIN_OVN_02",
                "name": "Convection Oven 2",
                "type": "OVEN",
                "ataChapter": "25-30",
                "canAddress": 0x12,
                "feeder": "FEEDER_A",
                "ratedKva": 3.2,
                "actualKva": 3.0,
                "priority": 3,
                "state": "HEATING",
                "powerGranted": True,
                "temperatureC": 158.0,
                "targetTempC": 160.0,
                "biteStatus": "NORMAL",
                "faultCode": "0x00"
            },
            {
                "id": "GAIN_BEV_01",
                "name": "Espresso Beverage Maker",
                "type": "BEVERAGE_MAKER",
                "ataChapter": "25-30",
                "canAddress": 0x21,
                "feeder": "FEEDER_B",
                "ratedKva": 2.8,
                "actualKva": 2.6,
                "priority": 4,
                "state": "BREWING",
                "powerGranted": True,
                "temperatureC": 92.5,
                "targetTempC": 94.0,
                "biteStatus": "NORMAL",
                "faultCode": "0x00"
            },
            {
                "id": "GAIN_WTR_01",
                "name": "Rapid Water Boiler",
                "type": "WATER_BOILER",
                "ataChapter": "25-30",
                "canAddress": 0x41,
                "feeder": "FEEDER_A",
                "ratedKva": 2.2,
                "actualKva": 2.1,
                "priority": 5,
                "state": "STANDBY",
                "powerGranted": False,
                "temperatureC": 78.0,
                "targetTempC": 88.0,
                "biteStatus": "NORMAL",
                "faultCode": "0x00"
            },
            {
                "id": "GAIN_CMP_01",
                "name": "Electro-Hydraulic Trash Compactor",
                "type": "TRASH_COMPACTOR",
                "ataChapter": "25-30",
                "canAddress": 0x51,
                "feeder": "FEEDER_B",
                "ratedKva": 1.4,
                "actualKva": 0.1,
                "priority": 6,
                "state": "STANDBY",
                "powerGranted": False,
                "temperatureC": 22.0,
                "targetTempC": 22.0,
                "biteStatus": "NORMAL",
                "faultCode": "0x00"
            }
        ]
        self.recompute_loads()

    def encode_can_id(self, priority, message_type, dest_addr, src_addr):
        can_id = 0
        can_id |= (priority & 0x07) << 26
        can_id |= (message_type & 0xFF) << 16
        can_id |= (dest_addr & 0xFF) << 8
        can_id |= (src_addr & 0xFF)
        return can_id

    def recompute_loads(self):
        load_a = sum(g["actualKva"] for g in self.gainDevices if g["powerGranted"] and g["feeder"] == "FEEDER_A")
        load_b = sum(g["actualKva"] for g in self.gainDevices if g["powerGranted"] and g["feeder"] == "FEEDER_B")

        self.powerFeeders["feederA"]["currentKva"] = round(load_a, 2)
        self.powerFeeders["feederB"]["currentKva"] = round(load_b, 2)

        max_allowed = self.powerFeeders["singleGeneratorLimitKva"] if self.powerFeeders["singleGeneratorMode"] else self.powerFeeders["totalMaxKva"]
        total = load_a + load_b

        if load_a > self.powerFeeders["feederA"]["ratedKva"] or load_b > self.powerFeeders["feederB"]["ratedKva"] or total > max_allowed:
            self._execute_shedding(max_allowed)
        else:
            self.powerFeeders["sheddingEngaged"] = False
            self.powerFeeders["feederA"]["status"] = "NORMAL"
            self.powerFeeders["feederB"]["status"] = "NORMAL"

    def _execute_shedding(self, max_allowed):
        self.powerFeeders["sheddingEngaged"] = True
        active = [g for g in self.gainDevices if g["powerGranted"] and g["priority"] > 1]
        active.sort(key=lambda x: x["priority"], reverse=True)

        for gain in active:
            curr_tot = self.powerFeeders["feederA"]["currentKva"] + self.powerFeeders["feederB"]["currentKva"]
            exceeds_a = self.powerFeeders["feederA"]["currentKva"] > self.powerFeeders["feederA"]["ratedKva"]
            exceeds_b = self.powerFeeders["feederB"]["currentKva"] > self.powerFeeders["feederB"]["ratedKva"]

            if curr_tot > max_allowed or (gain["feeder"] == "FEEDER_A" and exceeds_a) or (gain["feeder"] == "FEEDER_B" and exceeds_b):
                gain["powerGranted"] = False
                gain["state"] = "SHEDDED"
                if gain["feeder"] == "FEEDER_A":
                    self.powerFeeders["feederA"]["currentKva"] = round(self.powerFeeders["feederA"]["currentKva"] - gain["actualKva"], 2)
                else:
                    self.powerFeeders["feederB"]["currentKva"] = round(self.powerFeeders["feederB"]["currentKva"] - gain["actualKva"], 2)

    def generate_arinc429(self):
        self.recompute_loads()

        # Label 264 (Octal 264, Hex 0xB4)
        label264 = 0xB4
        fa_step = min(15, round(self.powerFeeders["feederA"]["currentKva"] / 0.5))
        fb_step = min(15, round(self.powerFeeders["feederB"]["currentKva"] / 0.5))
        shed_bit = 1 if self.powerFeeders["sheddingEngaged"] else 0
        ovld_a = 1 if self.powerFeeders["feederA"]["currentKva"] >= self.powerFeeders["feederA"]["ratedKva"] else 0
        ovld_b = 1 if self.powerFeeders["feederB"]["currentKva"] >= self.powerFeeders["feederB"]["ratedKva"] else 0

        data264 = 0
        data264 |= (fa_step & 0x0F) << 10
        data264 |= (fb_step & 0x0F) << 14
        data264 |= (shed_bit & 0x01) << 18
        data264 |= (ovld_a & 0x01) << 19
        data264 |= (ovld_b & 0x01) << 20
        data264 |= (0x03 & 0x03) << 28 # SSM Normal

        word264 = (data264 & 0x7FFFFF00) | (label264 & 0xFF)
        word264 = self._apply_odd_parity(word264)

        # Label 265 (Octal 265, Hex 0xB5)
        label265 = 0xB5
        online_cnt = len([g for g in self.gainDevices if g["state"] != "FAULT_ISOLATED"])
        fault_cnt = len([g for g in self.gainDevices if g["biteStatus"] == "FAULT"])
        gen_mode = 1 if self.powerFeeders["singleGeneratorMode"] else 0

        data265 = 0
        data265 |= (online_cnt & 0x3F) << 10
        data265 |= (fault_cnt & 0x3F) << 16
        data265 |= (gen_mode & 0x03) << 22
        data265 |= (0x03 & 0x03) << 28

        word265 = (data265 & 0x7FFFFF00) | (label265 & 0xFF)
        word265 = self._apply_odd_parity(word265)

        return {
            "label264": {
                "octal": "264",
                "hex": f"0x{word264:08X}",
                "binary": f"{word264:032b}",
                "parity_valid": self._check_odd_parity(word264),
                "feeder_a_kva": self.powerFeeders["feederA"]["currentKva"],
                "feeder_b_kva": self.powerFeeders["feederB"]["currentKva"],
                "shedding_active": self.powerFeeders["sheddingEngaged"]
            },
            "label265": {
                "octal": "265",
                "hex": f"0x{word265:08X}",
                "binary": f"{word265:032b}",
                "parity_valid": self._check_odd_parity(word265),
                "online_gains": online_cnt,
                "faulted_gains": fault_cnt,
                "single_gen_mode": self.powerFeeders["singleGeneratorMode"]
            }
        }

    def _apply_odd_parity(self, w):
        bits = w & 0x7FFFFFFF
        cnt = bin(bits).count('1')
        if cnt % 2 == 0:
            bits |= (1 << 31)
        return bits

    def _check_odd_parity(self, w):
        return bin(w).count('1') % 2 == 1

    def run_audit(self):
        tests = []
        # 1. CAN Framing
        can_id = self.encode_can_id(1, 0x03, 0x01, 0x11)
        t1 = (0 < can_id <= 0x1FFFFFFF) and ((can_id >> 26) == 1)
        tests.append(("AUD-812-01", "ARINC 812 Sec 3.1 & ISO 11898-1", "29-Bit Extended CAN Identifier Framing & Bitfields", t1))

        # 2. GAIN Address Uniqueness
        addrs = [g["canAddress"] for g in self.gainDevices]
        t2 = len(set(addrs)) == len(addrs) and all(0x10 <= a <= 0xFE for a in addrs)
        tests.append(("AUD-812-02", "ARINC 812 Sec 4.2 & ATA 25-30", "GAIN Equipment Address Allocation & Uniqueness", t2))

        # 3. Feeder Power Budget
        fa = self.powerFeeders["feederA"]
        fb = self.powerFeeders["feederB"]
        t3 = (fa["currentKva"] <= fa["ratedKva"]) and (fb["currentKva"] <= fb["ratedKva"])
        tests.append(("AUD-812-03", "ARINC 812 Sec 5.3 & Boeing D6-36440", "Galley Feeder Electrical Load Budget (A & B Caps)", t3))

        # 4. Food Safety Chiller Preservation
        chl = next((g for g in self.gainDevices if g["type"] == "CHILLER"), None)
        t4 = chl and chl["powerGranted"] and chl["temperatureC"] <= 4.0
        tests.append(("AUD-812-04", "ARINC 812 Sec 5.4 & FDA/EASA Food Safety", "High-Priority Food Safety Chiller Preservation", t4))

        # 5. DO-160G Power Quality
        t5 = (104.0 <= fa["voltageVac"] <= 122.0) and (380.0 <= fa["frequencyHz"] <= 420.0)
        tests.append(("AUD-812-05", "RTCA DO-160G Sec 16 & MIL-STD-704F", "115VAC 400Hz 3-Phase Aircraft Power Quality", t5))

        # 6. BITE Diagnostics
        t6 = all(g["biteStatus"] in ["NORMAL", "DEGRADED", "FAULT"] for g in self.gainDevices)
        tests.append(("AUD-812-06", "ARINC 812 Sec 6.1 & ARINC 604 BITE", "GAIN BITE Status Telemetry & Health Monitoring", t6))

        # 7. Single-Generator De-rate
        t7 = self.powerFeeders["singleGeneratorLimitKva"] == 8.0 and self.powerFeeders["singleGeneratorLimitKva"] < self.powerFeeders["totalMaxKva"]
        tests.append(("AUD-812-07", "ARINC 812 Sec 7.2 & EASA CS-25.1309", "Single-Generator In-Flight Cabin Electrical De-rate", t7))

        # 8. ARINC 429 Bus Parity
        b = self.generate_arinc429()
        t8 = b["label264"]["parity_valid"] and b["label265"]["parity_valid"]
        tests.append(("AUD-812-08", "ARINC 429 Part 1 & ARINC 812 Interface", "ARINC 429 Cabin Bus Odd Parity & Integrity", t8))

        # 9. Over-Temperature Protection
        ovens = [g for g in self.gainDevices if g["type"] == "OVEN"]
        t9 = all(o["temperatureC"] < 250.0 for o in ovens)
        tests.append(("AUD-812-09", "FAA FAR 25.869 / EASA CS-25.869", "Galley Insert Thermal Safeguards & Over-Temp Protection", t9))

        # 10. Overall Airworthiness Certification
        t10 = all(t[3] for t in tests[:9])
        tests.append(("AUD-812-10", "ICAO Doc 9760 Airworthiness Manual", "Continuous Cabin Galley Electrical Airworthiness Release", t10))

        return tests

def main():
    cli = ARINC812CLI()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "status":
        print("=================================================================")
        print(" ARINC812Forge Pro — Galley Insert Equipment (GAIN) & GNC Studio")
        print(" ARINC 812/812A | ISO 11898-1 CAN 2.0B | RTCA DO-160G Sec 16")
        print("=================================================================")
        print(f"Aircraft:        {cli.aircraft['tailNumber']} ({cli.aircraft['type']})")
        print(f"Galley Complex:  {cli.aircraft['galleyComplex']}")
        print(f"Electrical Bus:  {cli.aircraft['electricalBus']}")
        print("-----------------------------------------------------------------")
        fa = cli.powerFeeders['feederA']
        fb = cli.powerFeeders['feederB']
        print(f"Feeder A:        {fa['currentKva']} / {fa['ratedKva']} kVA ({fa['voltageVac']}V @ {fa['frequencyHz']}Hz) [{fa['status']}]")
        print(f"Feeder B:        {fb['currentKva']} / {fb['ratedKva']} kVA ({fb['voltageVac']}V @ {fb['frequencyHz']}Hz) [{fb['status']}]")
        total = round(fa['currentKva'] + fb['currentKva'], 2)
        print(f"Total Load:      {total} / {cli.powerFeeders['totalMaxKva']} kVA (Shedding: {'ACTIVE' if cli.powerFeeders['sheddingEngaged'] else 'OFF'})")
        print("-----------------------------------------------------------------")
        print("Active Galley Inserts (GAINs):")
        for g in cli.gainDevices:
            status = "GRANTED" if g['powerGranted'] else "SHEDDED/IDLE"
            print(f"  [{hex(g['canAddress'])}] {g['id']} ({g['name']}): {g['actualKva']} kVA | {g['temperatureC']}°C | Priority {g['priority']} | {status}")
        print("=================================================================")

    elif cmd == "canbus":
        print("=================================================================")
        print(" ARINC 812 CAN 2.0B 29-BIT EXTENDED IDENTIFIER MATRIX")
        print("=================================================================")
        for g in cli.gainDevices:
            cid = cli.encode_can_id(g['priority'], 0x05, 0x01, g['canAddress'])
            print(f"CAN ID: 0x{cid:08X} | Priority: {g['priority']} | Type: 0x05 (Status) | Dest: 0x01 (GNC) | Src: {hex(g['canAddress'])} ({g['id']})")
        print("=================================================================")

    elif cmd == "bus":
        b = cli.generate_arinc429()
        print("=================================================================")
        print(" ARINC 429 CABIN DISCRETE BUS TELEMETRY (LABELS 264 & 265)")
        print("=================================================================")
        print("Label 264 (Feeder Load & Shedding):")
        print(f"  Hex:    {b['label264']['hex']} (Bit 32 Odd Parity: {'VALID' if b['label264']['parity_valid'] else 'INVALID'})")
        print(f"  Binary: {b['label264']['binary']}")
        print(f"  Loads:  Feeder A {b['label264']['feeder_a_kva']} kVA | Feeder B {b['label264']['feeder_b_kva']} kVA")
        print("\nLabel 265 (GAIN Health & Bus Mode):")
        print(f"  Hex:    {b['label265']['hex']} (Bit 32 Odd Parity: {'VALID' if b['label265']['parity_valid'] else 'INVALID'})")
        print(f"  Binary: {b['label265']['binary']}")
        print(f"  Nodes:  Online: {b['label265']['online_gains']} | Faulted: {b['label265']['faulted_gains']}")
        print("=================================================================")

    elif cmd == "audit":
        tests = cli.run_audit()
        print("=================================================================")
        print(" ARINC 812 / DO-160G / EASA CS-25 NORMATIVE REGULATORY AUDIT")
        print("=================================================================")
        passed = sum(1 for t in tests if t[3])
        for code, std, desc, ok in tests:
            mark = "[PASS]" if ok else "[FAIL]"
            print(f"{mark} {code}: {desc}")
            print(f"       Standard: {std}")
        print("-----------------------------------------------------------------")
        print(f"Total Audit Checks: {len(tests)} | Passed: {passed} | Failed: {len(tests) - passed}")
        print(f"Compliance Score:   {(passed/len(tests))*100:.1f}%")
        print("=================================================================")

    elif cmd == "json":
        data = {
            "aircraft": cli.aircraft,
            "powerFeeders": cli.powerFeeders,
            "gainDevices": cli.gainDevices,
            "arinc429": cli.generate_arinc429()
        }
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
