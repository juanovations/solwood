"""Run: python3 -m unittest discover feasibility"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from proforma import annual_debt_service, apply, proforma  # noqa: E402

INPUTS = {
    "units": 2, "unit_sqft": 1000, "land_value": 100000,
    "hard_cost_per_sqft": 100, "site_work": 0,
    "soft_cost_pct_of_hard": 0.10, "contingency_pct_of_hard": 0.0,
    "construction_months": 12, "construction_loan_ltc": 0.5,
    "construction_rate": 0.10, "construction_avg_draw": 0.5,
    "rent_per_unit_month": 1000, "other_income_per_unit_month": 0,
    "vacancy_pct": 0.0, "opex_pct_of_egi": 0.5, "exit_cap_rate": 0.05,
    "perm_loan_ltv": 0.5, "perm_rate": 0.06, "perm_amort_years": 30,
}


class ProformaTest(unittest.TestCase):
    def test_hand_checked_numbers(self):
        r = proforma(INPUTS)
        # hard 200k + soft 20k + land 100k = 320k; loan 160k; interest 160k*0.5*0.10 = 8k
        self.assertAlmostEqual(r["tdc"], 328000)
        self.assertAlmostEqual(r["equity"], 168000)
        # rent 24k/yr, opex 50% -> NOI 12k; value 12k/5% = 240k
        self.assertAlmostEqual(r["noi"], 12000)
        self.assertAlmostEqual(r["value"], 240000)
        self.assertAlmostEqual(r["yield_on_cost"], 12000 / 328000)

    def test_debt_service_matches_standard_mortgage(self):
        # $100k at 6% over 30 years is the well-known $599.55/month payment
        self.assertAlmostEqual(annual_debt_service(100000, 0.06, 30) / 12, 599.55, places=2)

    def test_scenarios_move_the_right_way(self):
        base = proforma(INPUTS)
        self.assertLess(proforma(apply(INPUTS, {"rent_per_unit_month": 0.9}))["noi"], base["noi"])
        self.assertGreater(proforma(apply(INPUTS, {"hard_cost_per_sqft": 1.15}))["tdc"], base["tdc"])
        self.assertLess(proforma(apply(INPUTS, {"perm_rate": "+0.01"}))["dscr"], base["dscr"])

    def test_shipped_inputs_parse(self):
        i = json.loads((Path(__file__).parent / "inputs.json").read_text())
        self.assertGreater(proforma(i)["tdc"], 0)


if __name__ == "__main__":
    unittest.main()
