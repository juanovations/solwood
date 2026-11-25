"""Build-to-rent development pro forma for a Solwood apartment project.

Usage: python3 feasibility/proforma.py [inputs.json]  -> writes feasibility/REPORT.md
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent


def annual_debt_service(principal, rate, years):
    r = rate / 12
    n = years * 12
    return principal * r / (1 - (1 + r) ** -n) * 12


def proforma(i):
    sqft = i["units"] * i["unit_sqft"]
    hard = sqft * i["hard_cost_per_sqft"] + i["site_work"]
    soft = hard * i["soft_cost_pct_of_hard"]
    contingency = hard * i["contingency_pct_of_hard"]
    pre_interest = i["land_value"] + hard + soft + contingency
    # Interest on the average drawn balance over the build; capitalized into cost.
    loan = pre_interest * i["construction_loan_ltc"]
    interest = loan * i["construction_avg_draw"] * i["construction_rate"] * i["construction_months"] / 12
    tdc = pre_interest + interest
    equity = tdc - loan

    gpr = i["units"] * 12 * (i["rent_per_unit_month"] + i["other_income_per_unit_month"])
    egi = gpr * (1 - i["vacancy_pct"])
    opex = egi * i["opex_pct_of_egi"]
    noi = egi - opex

    value = noi / i["exit_cap_rate"]
    perm = value * i["perm_loan_ltv"]
    ds = annual_debt_service(perm, i["perm_rate"], i["perm_amort_years"])
    cash_flow = noi - ds
    cash_out = perm - loan  # positive: refinance returns equity
    left_in = equity - cash_out

    return {
        "sqft": sqft, "hard": hard, "soft": soft, "contingency": contingency,
        "interest": interest, "tdc": tdc, "tdc_per_unit": tdc / i["units"],
        "construction_loan": loan, "equity": equity,
        "gpr": gpr, "egi": egi, "opex": opex, "noi": noi,
        "yield_on_cost": noi / tdc, "value": value, "profit": value - tdc,
        "margin": (value - tdc) / tdc,
        "perm_loan": perm, "debt_service": ds, "dscr": noi / ds,
        "cash_flow": cash_flow, "refi_cash_out": cash_out, "equity_left_in": left_in,
        "cash_on_cash": cash_flow / left_in if left_in > 0 else None,
        "spread_bps": (noi / tdc - i["exit_cap_rate"]) * 10000,
    }


def verdict(r):
    problems = []
    if r["spread_bps"] < 0:
        problems.append(f"it would be worth less than it costs (yield on cost is {-r['spread_bps']:.0f} bps below the exit cap rate)")
    elif r["spread_bps"] < 100:
        problems.append(f"the development spread is only {r['spread_bps']:.0f} bps (aim for 100-200+)")
    if r["dscr"] < 1.20:
        problems.append(f"DSCR {r['dscr']:.2f} is below the 1.20 most lenders require")
    if not problems:
        return f"WORKS ON THESE INPUTS: {r['spread_bps']:.0f} bps development spread, DSCR {r['dscr']:.2f}."
    return ("FAILS" if r["spread_bps"] < 0 or r["dscr"] < 1.20 else "MARGINAL") + ": " + "; ".join(problems) + "."


# Multipliers are floats; "+x" strings add percentage points.
SCENARIOS = [
    ("Base case", {}),
    ("Rents -10%", {"rent_per_unit_month": 0.9}),
    ("Hard costs +15%", {"hard_cost_per_sqft": 1.15}),
    ("Rates +1 pt", {"construction_rate": "+0.01", "perm_rate": "+0.01"}),
    ("Exit cap +0.5 pt", {"exit_cap_rate": "+0.005"}),
]


def apply(i, changes):
    out = dict(i)
    for k, v in changes.items():
        out[k] = out[k] + float(v) if isinstance(v, str) else out[k] * v
    return out


def money(x):
    return f"-${-x:,.0f}" if x < 0 else f"${x:,.0f}"


def report(i, r):
    coc = "all equity returned at refinance" if r["cash_on_cash"] is None else f"{r['cash_on_cash']:.1%}"
    rows = [
        ("Building size", f"{r['sqft']:,} sq ft ({i['units']} units x {i['unit_sqft']} sq ft)"),
        ("Land (owned, at value)", money(i["land_value"])),
        ("Hard costs incl. site work", money(r["hard"])),
        ("Soft costs", money(r["soft"])),
        ("Contingency", money(r["contingency"])),
        ("Construction interest", money(r["interest"])),
        ("**Total development cost**", f"**{money(r['tdc'])}** ({money(r['tdc_per_unit'])} per unit)"),
        ("Construction loan", money(r["construction_loan"])),
        ("Equity needed (incl. land)", money(r["equity"])),
        ("Effective gross income", money(r["egi"]) + " / yr"),
        ("Operating expenses", money(r["opex"]) + " / yr"),
        ("**Net operating income**", f"**{money(r['noi'])} / yr**"),
        ("**Yield on cost**", f"**{r['yield_on_cost']:.2%}** vs {i['exit_cap_rate']:.2%} exit cap"),
        ("Stabilized value", money(r["value"])),
        ("Development profit", f"{money(r['profit'])} ({r['margin']:.1%} on cost)"),
        ("Permanent loan", money(r["perm_loan"])),
        ("Annual debt service", money(r["debt_service"])),
        ("DSCR", f"{r['dscr']:.2f}"),
        ("Cash flow after debt", money(r["cash_flow"]) + " / yr"),
        ("Cash out at refinance", money(r["refi_cash_out"])),
        ("Equity left in deal", money(r["equity_left_in"])),
        ("Cash-on-cash return", coc),
    ]
    lines = [
        "# Solwood: 6-unit build-to-rent feasibility",
        "",
        "> Generated by `feasibility/proforma.py` from `feasibility/inputs.json`.",
        "> **Inputs are placeholders until replaced with real site figures.**",
        "",
        f"**Verdict:** {verdict(r)}",
        "",
        "| Line | Amount |",
        "|---|---|",
        *[f"| {a} | {b} |" for a, b in rows],
        "",
        "## Sensitivity",
        "",
        "| Scenario | Yield on cost | Spread | DSCR | Profit |",
        "|---|---|---|---|---|",
    ]
    for name, changes in SCENARIOS:
        s = proforma(apply(i, changes))
        lines.append(f"| {name} | {s['yield_on_cost']:.2%} | {s['spread_bps']:.0f} bps | {s['dscr']:.2f} | {money(s['profit'])} |")
    return "\n".join(lines) + "\n"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "inputs.json"
    i = json.loads(path.read_text())
    out = HERE / "REPORT.md"
    out.write_text(report(i, proforma(i)))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
