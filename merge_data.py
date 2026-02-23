import pandas as pd

materials = pd.read_csv("data/materials_master.csv")
impact = pd.read_csv("data/environmental_impact.csv")
risk = pd.read_csv("data/supply_chain_risk.csv")
reg = pd.read_csv("data/regulatory_confidence.csv")

df = (
    materials
    .merge(impact, on="material_id")
    .merge(risk, on="material_id")
    .merge(reg, on="material_id")
)

df.to_csv("data/smdi_combined.csv", index=False)

print("Combined dataset created: data/smdi_combined.csv")