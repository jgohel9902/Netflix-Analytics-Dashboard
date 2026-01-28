# 🎬 Netflix Analytics Dashboard
## Customer Engagement, Content Performance & Churn Analysis

A single-page **executive analytics dashboard** built using **Power BI**, designed to analyze a Netflix-style streaming platform across subscribers, engagement, content, devices, and churn indicators.
This project demonstrates **end-to-end analytics skills**, combining **Python-based data generation**, **Power BI data modeling**, **DAX**, and **executive-focused dashboard design**.
> ⚠️ This is a portfolio/demo project. Netflix is not affiliated with this work.

---

## 🎯 Project Objectives

- Build a realistic **streaming analytics dashboard**
- Demonstrate **data engineering + BI integration**
- Apply **star schema modeling**
- Create **business-relevant KPIs**
- Design a **Netflix-inspired executive UI**
- Extract clear, decision-oriented insights

---

## 🐍 Python-Based Fact Table Generation

The original Netflix titles dataset does not contain **engagement-level metrics** required for analytics (watch hours, MAU, revenue, churn).  
To address this, **Python was used to generate a realistic fact table**.

### Why Python was used
- Simulate real-world streaming KPIs
- Create a proper **fact table**
- Demonstrate analytics engineering skills
- Separate data generation from visualization

### Metrics generated using Python
- Total Watch Hours
- Monthly Active Users (MAU)
- Average Watch Time
- Revenue estimates
- Churn Rate %

### Python workflow
Netflix Titles Dataset
↓
Python (pandas)
↓
Generated Fact Table (CSV)
↓
Power BI Data Model
↓
Dashboard & Insights


### Sample Python logic
```python
import pandas as pd
import numpy as np

titles = pd.read_csv("netflix_titles.csv")

fact_data = titles.assign(
    WatchHours=np.random.randint(1000, 50000, len(titles)),
    MonthlyActiveUsers=np.random.randint(500, 20000, len(titles)),
    Revenue=np.random.uniform(10000, 500000, len(titles)),
    ChurnRate=np.random.uniform(0.5, 5.0, len(titles))
)

fact_data.to_csv("FactViewingDaily.csv", index=False)
```

## 🔹 Phase 1: Data Acquisition & Understanding
Reviewed Netflix titles dataset structure
Identified missing engagement-level metrics
Planned star schema design
Defined business KPIs


## 🔹 Phase 2: Data Cleaning & Transformation (Power Query)
Removed duplicates and invalid rows
Standardized column names
Split multi-value genres into a dimension table
Created surrogate keys (ShowKey, GenreKey)
Generated Date and Month keys
Validated data types

## 🔹 Phase 3: Data Modeling (Star Schema)
Fact Table
FactViewingDaily

Dimension Tables
DimShow
DimGenre
DimDate
DimDevice
DimCountry

Relationships were designed to ensure:
Correct aggregation
Proper filtering
Support for Top-N analysis


## 🔹 Phase 4: DAX Measures

Key measures created:

Total Watch Hours =
SUM ( FactViewingDaily[WatchHours] )

Monthly Active Users =
SUM ( FactViewingDaily[MonthlyActiveUsers] )

Avg Watch Time per Viewer =
DIVIDE ( [Total Watch Hours], [Monthly Active Users] )

Monthly Revenue =
SUM ( FactViewingDaily[Revenue] )

Churn Rate % =
AVERAGE ( FactViewingDaily[ChurnRate] )


Additional measures:
Latest Subscribers
Device contribution %
Top 10 rankings
Engagement mix calculations


## 🔹 Phase 5: Dashboard Design & UX

Design principles:

Netflix-inspired dark UI
High-contrast red highlights
Clean spacing and alignment
Executive-level readability

Visuals included
KPI cards (Subscribers, MAU, Watch Hours, Revenue, Churn)
Engagement Mix by Device (100% stacked bars)
Top 10 Most Watched Shows
Viewing by Device
Top 10 Genres by Watch Hours (Pie Chart)
Interactive slicers (Date, Country, Genre)

## 🔹 Phase 6: Key Insights

TV devices generate the highest watch hours
Mobile has higher user volume but lower engagement depth
A small set of genres contributes most of total watch time
Tablet usage is comparatively underutilized
Engagement patterns vary significantly by device

## 🛠 Tools & Technologies

Power BI (Power Query, DAX, Data Modeling)
Python (pandas)
GitHub
Data Visualization & UX Design


## ⚠️ Disclaimer

This project is for educational and portfolio purposes only.
All engagement metrics are simulated and do not represent real Netflix data.
