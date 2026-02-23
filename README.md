# Sustainable Materials Decision Intelligence (SMDI)

### A decision-support analytics prototype for material selection under environmental, operational, and regulatory uncertainty

**Tableau Dashboard:** *(insert Tableau Public link)*

---

## Project Overview

The dashboard models a realistic scenario: a company evaluating candidate materials (e.g., fibers, polymers, or packaging inputs) where each option has different environmental impacts, supply chain risks, and regulatory exposure. Instead of ranking materials by a single “green” metric, the tool provides a transparent framework to evaluate tradeoffs.

---

## The Problem

Material sustainability decisions are difficult because:

* Environmental impact data (LCA) uses different methodologies and boundaries
* Supplier disclosures are incomplete and vary by region
* Regulatory risk is evolving (e.g., microplastics, chemical restrictions, forced labor rules)
* Operational constraints (lead time, availability, cost) cannot be ignored

As a result, teams often rely on static sustainability scores that do not reflect real business decisions.

This project demonstrates an alternative: **decision intelligence** — analytics designed to support a choice under uncertainty.

---

## Key Questions Addressed

* How can sustainability data be combined with operational risk?
* How should companies evaluate materials when no option is optimal?
* How does data reliability affect a decision?
* How do changing regulations alter recommended materials?

---

## Data Model

The dataset simulates a realistic corporate analytics environment with four integrated domains:

### 1. Materials Master Data

Defines materials, sourcing regions, and supply chain structure.

### 2. Environmental Impact (LCA-like metrics)

Includes carbon, water, energy, land use, recyclability, and microplastic risk.

### 3. Supply Chain Risk

Models disruption probability, supplier concentration, country risk, price volatility, and lead time.

### 4. Regulatory & Data Confidence

Captures regulatory exposure and reliability of reported sustainability data.

All values are illustrative and designed to represent real-world data quality challenges rather than exact measurements.

## How to Generate Data

The project includes a reproducible dummy data generator to simulate realistic sustainability, supply chain, and regulatory datasets.

All CSV files used in the dashboard are generated programmatically.

Requirements

Python 3.9+

pandas

numpy

### Install Dependencies (Windows)

Open Command Prompt or PowerShell and run:

``py -m pip install pandas numpy``

If py is not recognized:

``python -m pip install pandas numpy
Generate the Data``

From the root of the repository, run:

``py generate_dummy_data.py --rows 90 --seed 42 --out data``

### Parameters:

--rows → number of materials to generate

--seed → random seed for reproducibility

--out → output directory for CSV files

This will create:

```
/data
  materials_master.csv
  environmental_impact.csv
  supply_chain_risk.csv
  regulatory_confidence.csv
  scenarios.csv
```

## Reproducibility

Using a fixed seed ensures that results are deterministic and reproducible.
Changing the seed allows simulation of alternative supply chain distributions and impact scenarios.

---

## Dashboard Structure

### Executive Overview

A high-level material recommendation based on weighted environmental and operational criteria.

### Tradeoff Explorer

An interactive scatterplot allowing users to adjust priorities (carbon, cost, and risk) to see how recommended materials change.

### Supply Chain Risk

Visualizes geographic sourcing exposure and operational vulnerability.

### Uncertainty & Data Quality

Introduces a confidence-adjusted score to demonstrate how data reliability changes decisions.

### Scenario Simulator

Simulates policy changes (e.g., microplastics regulation) and shows how recommendations shift under new constraints.

---

## Methods

The analysis uses a multi-criteria decision framework combining:

* Environmental impact metrics
* Operational risk indicators
* Regulatory exposure
* Data confidence weighting

Instead of searching for a single “best” material, the system evaluates tradeoffs and supports transparent decision-making.

---

## Key Insights

* No material dominates across environmental, cost, and risk dimensions.
* A material with the lowest carbon impact may carry the highest operational risk.
* Data confidence materially changes recommendations.
* Sustainability decisions are optimization problems, not ranking problems.
* Regulatory scenarios can rapidly alter material suitability.

---

## Why This Matters

Sustainability reporting is mature, but sustainability decision support is not.
Organizations increasingly need analytics that helps teams choose actions, not just measure outcomes.

This project demonstrates how analytics can bridge environmental data and operational decision-making — moving sustainability from compliance reporting to product strategy.

---

## Tools Used

* Tableau Public (visual analytics & parameterized scenario modeling)
* Excel (data modeling & weighted scoring framework)

---

## Future Improvements

* Incorporate real LCA databases (e.g., ecoinvent)
* Add supplier-level traceability
* Include product performance metrics
* Extend to portfolio optimization across multiple products

---

## Author

**Vesper Annstas**
Data Analytics & Decision Intelligence
LinkedIn: *[(link)](https://www.linkedin.com/in/vesperannstas/)*
