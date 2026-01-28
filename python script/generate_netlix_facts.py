import pandas as pd
import numpy as np
from datetime import datetime

np.random.seed(42)

# ==== CONFIG ====
TITLES_CSV = "../netflix_titles.csv"
OUT_DIR = "data/generated"
START_DATE = "2023-01-01"
END_DATE = "2024-12-31"

countries = ["Canada", "United States", "India", "United Kingdom", "Australia"]
devices   = ["Mobile", "TV", "Laptop", "Tablet"]

# ====== LOAD TITLES ======
titles = pd.read_csv(TITLES_CSV)
# Ensure expected column names
if "show_id" not in titles.columns:
    raise ValueError("Expected column 'show_id' in netflix_titles.csv")

titles = titles.rename(columns={"show_id": "ShowKey"})


titles = titles[["ShowKey", "title", "type", "release_year", "rating", "listed_in"]].dropna(subset=["ShowKey"])
titles = titles.drop_duplicates(subset=["ShowKey"]).reset_index(drop=True)

#  popularity weight (newer titles slightly more popular)
yr = titles["release_year"].fillna(titles["release_year"].median())
pop_weight = (yr - yr.min() + 1).astype(float)
pop_weight = pop_weight / pop_weight.sum()

# ====== DIM DATE ======
dates = pd.date_range(start=START_DATE, end=END_DATE, freq="D")
dim_date = pd.DataFrame({
    "Date": dates,
    "DateKey": dates.strftime("%Y%m%d").astype(int),
    "Year": dates.year,
    "Month": dates.month,
    "MonthName": dates.strftime("%b"),
    "YearMonth": dates.strftime("%Y-%m"),
    "Quarter": "Q" + (((dates.month - 1)//3) + 1).astype(str),
    "DayOfWeek": dates.strftime("%a"),
    "DayOfWeekNum": dates.dayofweek + 1,  # Mon=1
    "WeekOfYear": dates.isocalendar().week.astype(int)
})

# ====== FACT VIEWING (DAILY) ======
#  realistic seasonality: weekends higher viewing, summer slightly higher
dow_factor = dim_date["DayOfWeek"].map({"Mon":0.85,"Tue":0.85,"Wed":0.9,"Thu":0.95,"Fri":1.1,"Sat":1.25,"Sun":1.2}).values
month_factor = dim_date["Month"].map({1:0.95,2:0.95,3:1.0,4:1.0,5:1.05,6:1.1,7:1.12,8:1.1,9:1.0,10:1.02,11:1.05,12:1.15}).values

base_viewers = 45000  # controls volume
rows = []

for i, d in enumerate(dim_date["Date"]):
    day_mult = dow_factor[i] * month_factor[i]

    # Country distribution (Canada emphasized)
    country_shares = np.array([0.18, 0.30, 0.25, 0.15, 0.12])  # sums to 1
    day_total_viewers = int(base_viewers * day_mult)

    for c_idx, c in enumerate(countries):
        c_viewers = int(day_total_viewers * country_shares[c_idx])

        # Device distribution
        dev_shares = np.array([0.35, 0.40, 0.18, 0.07])
        for dev_idx, dev in enumerate(devices):
            dev_viewers = int(c_viewers * dev_shares[dev_idx])

            # Pick a subset of titles watched that day for that segment
            n_titles_today = 60
            chosen = np.random.choice(titles["ShowKey"].values, size=n_titles_today, replace=False, p=pop_weight)

            # Allocate viewers across titles using a Dirichlet distribution
            alloc = np.random.dirichlet(np.ones(n_titles_today) * 0.6)
            viewers_per_title = np.maximum(1, (alloc * dev_viewers).astype(int))

            # Sessions per viewer & minutes per session vary by device
            if dev == "TV":
                avg_sessions = 1.3
                avg_minutes = 55
            elif dev == "Mobile":
                avg_sessions = 1.6
                avg_minutes = 28
            elif dev == "Laptop":
                avg_sessions = 1.4
                avg_minutes = 40
            else:
                avg_sessions = 1.3
                avg_minutes = 35

            for show_key, v in zip(chosen, viewers_per_title):
                sessions = int(np.round(v * np.random.normal(avg_sessions, 0.15)))
                sessions = max(1, sessions)

                watch_minutes = int(np.round(sessions * np.random.normal(avg_minutes, 6)))
                watch_minutes = max(5, watch_minutes)

                rows.append([d, int(d.strftime("%Y%m%d")), show_key, c, dev, v, sessions, watch_minutes])

fact_viewing = pd.DataFrame(rows, columns=[
    "Date", "DateKey", "ShowKey", "Country", "Device",
    "UniqueViewers", "Sessions", "WatchMinutes"
])

# ====== FACT SUBSCRIPTIONS (MONTHLY) ======
months = pd.date_range(start=START_DATE, end=END_DATE, freq="MS")
sub_rows = []
starting_subs = {"Canada": 1200000, "United States": 6500000, "India": 5200000, "United Kingdom": 2100000, "Australia": 900000}

for m in months:
    ym = m.strftime("%Y-%m")
    season_mult = 1.0 + (0.08 if m.month in [11,12,1] else 0.0)  # holiday spike
    for c in countries:
        prev = starting_subs[c]

        # Growth + churn dynamics
        new_subs = int(prev * np.random.uniform(0.015, 0.03) * season_mult)
        churned = int(prev * np.random.uniform(0.010, 0.022) / season_mult)

        subscribers = max(1000, prev + new_subs - churned)
        starting_subs[c] = subscribers

        # Revenue & ARPU (simplified, country-based)
        base_arpu = {"Canada": 14.5, "United States": 15.5, "India": 6.0, "United Kingdom": 13.5, "Australia": 15.0}[c]
        arpu = np.random.normal(base_arpu, 0.35)
        revenue = subscribers * arpu

        sub_rows.append([m.date(), int(m.strftime("%Y%m01")), ym, c, subscribers, new_subs, churned, round(arpu,2), round(revenue,2)])

fact_subs = pd.DataFrame(sub_rows, columns=[
    "MonthStartDate", "MonthKey", "YearMonth", "Country",
    "Subscribers", "NewSubscribers", "ChurnedSubscribers", "ARPU", "Revenue"
])

# ====== SAVE ======
import os
os.makedirs(OUT_DIR, exist_ok=True)

dim_date.to_csv(f"{OUT_DIR}/DimDate.csv", index=False)
fact_viewing.to_csv(f"{OUT_DIR}/FactViewingDaily.csv", index=False)
fact_subs.to_csv(f"{OUT_DIR}/FactSubscriptionsMonthly.csv", index=False)

print("✅ Generated:")
print(f"- {OUT_DIR}/DimDate.csv")
print(f"- {OUT_DIR}/FactViewingDaily.csv")
print(f"- {OUT_DIR}/FactSubscriptionsMonthly.csv")
print("Rows:", len(fact_viewing), "viewing rows;", len(fact_subs), "subscription rows")