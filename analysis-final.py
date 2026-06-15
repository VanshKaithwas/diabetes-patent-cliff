# Diabetes Drug Patent Cliff Analyzer
# Vansh Kaithwas | Class 12

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# load dataset
df = pd.read_csv("diabetes_patents.csv")

print("=" * 50)
print("  Diabetes Patent Cliff Analyzer — Vansh Kaithwas")
print("=" * 50)
print(f"\n drugs in dataset : {len(df)}")
print(f" companies        : {df['company'].nunique()}")
print(f" total revenue    : ${df['annual_revenue_usd_bn'].sum():.1f}B")

# convert yes/no to true/false
df["generic_available"] = df["generic_available"].map({"Yes": True, "No": False})

# years until patent expires
current_year = 2024
df["years_until_expiry"] = df["patent_expiry_year"] - current_year

# classify urgency
def classify_urgency(years):
    if years <= 0:
        return "Already Expired"
    elif years <= 2:
        return "Expiring Soon"
    elif years <= 5:
        return "Near Term"
    else:
        return "Long Term"

df["urgency"] = df["years_until_expiry"].apply(classify_urgency)

# revenue per year
print("\n-- revenue expiring per year --")
yearly = df.groupby("patent_expiry_year")["annual_revenue_usd_bn"].sum().round(2)
print(yearly.to_string())

# company exposure
print("\n-- company exposure --")
company_exposure = df.groupby("company").agg(
    drugs   = ("drug_name", "count"),
    revenue = ("annual_revenue_usd_bn", "sum")
).sort_values("revenue", ascending=False).round(2)
print(company_exposure.to_string())

# expiring within 3 years
print("\n-- expiring within 3 years --")
soon = df[df["years_until_expiry"] <= 3][
    ["drug_name", "company", "patent_expiry_year", "annual_revenue_usd_bn"]
].sort_values("annual_revenue_usd_bn", ascending=False)
print(soon.to_string(index=False))

# boehringer ingelheim focus
print("\n-- Boehringer Ingelheim --")
bi = df[df["company"] == "Boehringer Ingelheim"][
    ["drug_name", "patent_expiry_year", "annual_revenue_usd_bn", "urgency"]
]
print(bi.to_string(index=False))
print(f"\n total BI revenue at risk: ${bi['annual_revenue_usd_bn'].sum():.1f}B")

# charts
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Diabetes Patent Cliff — Vansh Kaithwas", fontsize=13, fontweight="bold")

# chart 1 - revenue per year
colors = ["#c0392b" if y <= 2026 else "#1a3a5c" for y in yearly.index]
axes[0].bar(yearly.index.astype(str), yearly.values, color=colors)
axes[0].set_title("Revenue Expiring Per Year ($B)", fontweight="bold")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Revenue ($B)")
for i, v in enumerate(yearly.values):
    axes[0].text(i, v + 0.1, f"${v}B", ha="center", fontsize=8)
axes[0].tick_params(axis="x", rotation=45)

# chart 2 - company exposure
top = company_exposure.head(6)
bars = axes[1].barh(top.index, top["revenue"], color="#1a3a5c")
axes[1].set_title("Company Exposure ($B)", fontweight="bold")
for bar, company in zip(bars, top.index):
    if company == "Boehringer Ingelheim":
        bar.set_color("#c0392b")
axes[1].invert_yaxis()

# chart 3 - urgency pie
urgency_data = df.groupby("urgency")["annual_revenue_usd_bn"].sum()
colors_pie = {
    "Already Expired": "#aaa",
    "Expiring Soon":   "#c0392b",
    "Near Term":       "#e8a838",
    "Long Term":       "#1a3a5c"
}
pie_colors = [colors_pie.get(u, "#999") for u in urgency_data.index]
axes[2].pie(urgency_data.values, labels=urgency_data.index,
            colors=pie_colors, autopct="%1.1f%%", startangle=90,
            textprops={"fontsize": 8})
axes[2].set_title("Revenue by Urgency", fontweight="bold")

plt.tight_layout()
plt.savefig("patent_cliff_charts.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n saved: patent_cliff_charts.png")

print("\n" + "=" * 50)
print("  KEY FINDING")
print("=" * 50)
print("""
  Boehringer Ingelheim has 3 diabetes drugs all
  expiring in 2025 — Jardiance, Synjardy, Trajenta.
  That is around $7B in one year.

  2026 is the worst year overall — multiple big
  drugs expire at the same time.

  Novo Nordisk is actually in a safe position,
  most of their drugs go until 2031+.
""")
