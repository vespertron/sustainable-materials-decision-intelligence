import argparse
import os
import random
from dataclasses import dataclass
from typing import List, Dict

import numpy as np
import pandas as pd


CATEGORIES = ["Natural", "Synthetic", "Recycled", "Bio-based"]
USE_CASES = ["Fabric", "Upper", "Midsole", "Outsole", "Packaging", "Trim"]
REGIONS = ["Vietnam", "China", "India", "Turkey", "USA", "Mexico", "Brazil", "Indonesia", "Thailand", "Italy"]
TIER_LEVELS = ["Tier 1", "Tier 2", "Tier 3"]

RISK_LEVELS = ["Low", "Medium", "High"]
CONF_LEVELS = ["Low", "Medium", "High"]


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def choice_weighted(items: List[str], weights: List[float]) -> str:
    return random.choices(items, weights=weights, k=1)[0]


def make_material_name(category: str) -> str:
    natural = ["Cotton", "Wool", "Leather", "Linen", "Hemp"]
    synthetic = ["Polyester", "Nylon", "Elastane", "EVA", "TPU"]
    recycled = ["Recycled Polyester", "Recycled Nylon", "Recycled TPU", "rPET"]
    biobased = ["Bio-EVA", "PLA", "Bio-TPU", "Castor-based Nylon"]

    pool = {
        "Natural": natural,
        "Synthetic": synthetic,
        "Recycled": recycled,
        "Bio-based": biobased,
    }[category]
    base = random.choice(pool)

    # add a small qualifier sometimes
    qualifiers = ["", "", "", " - Lightweight", " - Premium", " - High Tenacity", " - Low Dye"]
    return f"{base}{random.choice(qualifiers)}"


def gen_rows(n: int, seed: int) -> Dict[str, pd.DataFrame]:
    random.seed(seed)
    np.random.seed(seed)

    # category mix (tune as you like)
    cat_weights = [0.30, 0.30, 0.25, 0.15]

    materials = []
    impacts = []
    supply = []
    reg = []

    for i in range(1, n + 1):
        material_id = f"M{i:03d}"
        category = choice_weighted(CATEGORIES, cat_weights)
        use_case = random.choice(USE_CASES)
        primary_region = random.choice(REGIONS)
        tier_level = choice_weighted(TIER_LEVELS, [0.55, 0.30, 0.15])

        # Recycled content
        if category == "Recycled":
            recycled_content = clamp(int(np.random.normal(70, 20)), 20, 100)
        elif category == "Bio-based":
            recycled_content = clamp(int(np.random.normal(10, 10)), 0, 40)
        else:
            recycled_content = clamp(int(np.random.normal(2, 4)), 0, 15)

        name = make_material_name(category)

        # --- Environmental impacts (correlated, category-driven) ---
        # Base distributions (roughly plausible ranges; portfolio-grade, not scientific)
        if category == "Natural":
            carbon = np.random.normal(5.0, 1.2)
            water = np.random.lognormal(mean=9.0, sigma=0.35)  # large
            energy = np.random.normal(60, 15)
            land = np.random.normal(8.0, 2.0)
            microplastics = "Low"
            recyclability = np.random.normal(45, 15)
        elif category == "Synthetic":
            carbon = np.random.normal(6.0, 1.5)
            water = np.random.lognormal(mean=4.0, sigma=0.35)  # smaller
            energy = np.random.normal(85, 18)
            land = np.random.normal(2.5, 1.0)
            microplastics = choice_weighted(RISK_LEVELS, [0.15, 0.55, 0.30])
            recyclability = np.random.normal(55, 15)
        elif category == "Recycled":
            carbon = np.random.normal(3.0, 0.9)
            water = np.random.lognormal(mean=3.5, sigma=0.30)
            energy = np.random.normal(70, 15)
            land = np.random.normal(1.8, 0.8)
            microplastics = choice_weighted(RISK_LEVELS, [0.10, 0.55, 0.35])
            recyclability = np.random.normal(70, 12)
        else:  # Bio-based
            carbon = np.random.normal(3.8, 1.0)
            water = np.random.lognormal(mean=4.7, sigma=0.35)
            energy = np.random.normal(75, 15)
            land = np.random.normal(4.5, 1.5)
            microplastics = choice_weighted(RISK_LEVELS, [0.25, 0.55, 0.20])
            recyclability = np.random.normal(60, 15)

        # tie impacts lightly to recycled content
        carbon *= (1.0 - (recycled_content / 400.0))  # modest reduction
        water *= (1.0 - (recycled_content / 800.0))

        carbon = float(clamp(carbon, 0.8, 12.0))
        water = float(clamp(water, 10.0, 30000.0))
        energy = float(clamp(energy, 20.0, 140.0))
        land = float(clamp(land, 0.2, 15.0))
        recyclability = float(clamp(recyclability, 0.0, 100.0))

        # --- Supply chain risk ---
        # Concentration higher for Bio-based/Organic-like and some recycled streams
        base_conc = {
            "Natural": 0.45,
            "Synthetic": 0.55,
            "Recycled": 0.60,
            "Bio-based": 0.70,
        }[category]
        supplier_conc = float(clamp(np.random.normal(base_conc, 0.12), 0.05, 0.95))

        # Country risk loosely tied to region
        region_risk_map = {
            "USA": 20, "Italy": 25, "Mexico": 35, "Turkey": 45, "Brazil": 40,
            "Vietnam": 50, "Thailand": 45, "China": 55, "India": 55, "Indonesia": 60
        }
        country_risk = float(clamp(np.random.normal(region_risk_map[primary_region], 10), 0, 100))

        climate_exposure = float(clamp(np.random.normal(50 if category == "Natural" else 40, 15), 0, 100))
        price_vol = float(clamp(np.random.normal(65 if category in ["Natural", "Bio-based"] else 55, 15), 0, 100))

        lead_time = int(clamp(np.random.normal(45 if tier_level == "Tier 3" else 30, 10), 7, 120))

        # Disruption probability depends on concentration + country risk + lead time
        disruption = (0.45 * supplier_conc) + (0.35 * (country_risk / 100)) + (0.20 * (lead_time / 120))
        disruption = float(clamp(disruption + np.random.normal(0, 0.05), 0.01, 0.95))

        # --- Regulatory & confidence ---
        # PFAS risk more likely for synthetics
        if category in ["Synthetic", "Recycled"]:
            pfas_risk = choice_weighted(RISK_LEVELS, [0.25, 0.55, 0.20])
        else:
            pfas_risk = choice_weighted(RISK_LEVELS, [0.65, 0.30, 0.05])

        forced_labor_risk = choice_weighted(RISK_LEVELS, [0.55, 0.30, 0.15])
        # tie forced labor risk a bit to country risk
        if country_risk > 60:
            forced_labor_risk = choice_weighted(RISK_LEVELS, [0.35, 0.40, 0.25])

        disclosure_level = int(clamp(np.random.normal(3, 1.0), 1, 5))

        # Data confidence: higher for Natural (more studied), lower for recycled streams variability
        if category == "Natural":
            data_conf = choice_weighted(CONF_LEVELS, [0.10, 0.35, 0.55])
        elif category == "Recycled":
            data_conf = choice_weighted(CONF_LEVELS, [0.45, 0.40, 0.15])
        else:
            data_conf = choice_weighted(CONF_LEVELS, [0.25, 0.50, 0.25])

        audit_freq = int(clamp(np.random.normal(3 if data_conf == "Low" else 2, 1.5), 0, 12))
        certification = "Y" if category in ["Natural", "Bio-based"] and random.random() < 0.55 else "N"

        materials.append({
            "material_id": material_id,
            "material_name": name,
            "category": category,
            "use_case": use_case,
            "primary_region": primary_region,
            "tier_level": tier_level,
            "recycled_content_pct": recycled_content,
            "notes": ""
        })

        impacts.append({
            "material_id": material_id,
            "carbon_kgco2e_per_kg": round(carbon, 3),
            "water_l_per_kg": round(water, 1),
            "energy_mj_per_kg": round(energy, 1),
            "land_use_m2_per_kg": round(land, 2),
            "recyclability_score": round(recyclability, 1),
            "microplastic_risk": microplastics
        })

        supply.append({
            "material_id": material_id,
            "supplier_concentration_index": round(supplier_conc, 3),
            "country_risk_score": round(country_risk, 1),
            "climate_exposure_score": round(climate_exposure, 1),
            "price_volatility_index": round(price_vol, 1),
            "lead_time_days": lead_time,
            "disruption_probability": round(disruption, 3)
        })

        reg.append({
            "material_id": material_id,
            "pfas_regulatory_risk": pfas_risk,
            "forced_labor_risk": forced_labor_risk,
            "disclosure_requirement_level": disclosure_level,
            "data_confidence": data_conf,
            "audit_frequency_per_year": audit_freq,
            "certification_available": certification
        })

    return {
        "materials_master": pd.DataFrame(materials),
        "environmental_impact": pd.DataFrame(impacts),
        "supply_chain_risk": pd.DataFrame(supply),
        "regulatory_confidence": pd.DataFrame(reg),
        "scenarios": pd.DataFrame([
            {"scenario": "Baseline", "microplastics_penalty_factor": 1.00, "pfas_penalty_factor": 1.00, "country_risk_multiplier": 1.00},
            {"scenario": "Microplastics_Ban_On", "microplastics_penalty_factor": 1.25, "pfas_penalty_factor": 1.00, "country_risk_multiplier": 1.00},
            {"scenario": "Geo_Tension_Spike", "microplastics_penalty_factor": 1.00, "pfas_penalty_factor": 1.00, "country_risk_multiplier": 1.15},
        ])
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=90)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=str, default="data")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    dfs = gen_rows(args.rows, args.seed)

    for name, df in dfs.items():
        path = os.path.join(args.out, f"{name}.csv")
        df.to_csv(path, index=False)

    print(f"✅ Wrote {len(dfs)} files to: {os.path.abspath(args.out)}")


if __name__ == "__main__":
    main()