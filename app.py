import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dishwashing Liquid Formulation Calculator", layout="wide")

st.title("🧴 Dishwashing Liquid Formulation Calculator")
st.caption("Myanmar/English — % adjust, batch sizing, Active Matter (AM%), cost & CSV export")

# -------- Helpers --------
def safe_float(x, default=0.0):
    try:
        return float(x)
    except:
        return default

def total_percent(ings):
    return sum(i["percent"] for i in ings)

def compute_active_matter(ings):
    """Sum(percent * active_fraction) / 100"""
    am = 0.0
    for i in ings:
        am += i["percent"] * i.get("active_frac", 0.0)
    return am / 100.0 * 100.0  # in %

def compute_batch_table(ings, batch_size_kg, density):
    """
    Assume final product density ~ density (kg/L). If user works in liters,
    we convert L to kg by *density. Internally we compute kg; also provide grams.
    """
    rows = []
    total_pct = total_percent(ings)
    # water auto-fill to reach 100 if 'Water' exists and total < 100
    # (we adjust before computing)
    return rows

# -------- Defaults (You can tweak freely) --------
st.sidebar.header("Preset / Load a style")
preset = st.sidebar.selectbox(
    "Choose preset style (ရွေးချယ်ရန်)",
    [
        "B. Medium Foam + Thick (Recommended)",
        "C. Premium High Foam",
        "A. Economy (Standard)",
        "D. Low-chemical / Sensitive",
    ],
)

# Ingredient table with common raw materials
# percent: user-editable, active_frac: active ingredient fraction (e.g. SLES 70% active -> 0.70)
# density_kg_per_l: optional reference (most liquids ~1.0)
if preset == "C. Premium High Foam":
    default_ings = [
        {"name": "SLES (70% active)", "percent": 14.0, "active_frac": 0.70, "cost_per_kg": 0.0},
        {"name": "SLS (Needles/Powder, 95% active)", "percent": 3.0, "active_frac": 0.95, "cost_per_kg": 0.0},
        {"name": "CAPB (30% active)", "percent": 5.0, "active_frac": 0.30, "cost_per_kg": 0.0},
        {"name": "NaCl (Salt for viscosity)", "percent": 2.0, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Citric Acid (pH adjust)", "percent": 0.20, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Preservative", "percent": 0.30, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Fragrance (Lemon/Lime)", "percent": 0.50, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Dye (Color)", "percent": 0.01, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Water (QS to 100%)", "percent": 74.99, "active_frac": 0.00, "cost_per_kg": 0.0},
    ]
elif preset == "A. Economy (Standard)":
    default_ings = [
        {"name": "SLES (70% active)", "percent": 10.0, "active_frac": 0.70, "cost_per_kg": 0.0},
        {"name": "CAPB (30% active)", "percent": 3.0, "active_frac": 0.30, "cost_per_kg": 0.0},
        {"name": "NaCl (Salt for viscosity)", "percent": 2.0, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Citric Acid (pH adjust)", "percent": 0.20, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Preservative", "percent": 0.20, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Fragrance", "percent": 0.30, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Dye", "percent": 0.01, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Water (QS to 100%)", "percent": 84.29, "active_frac": 0.00, "cost_per_kg": 0.0},
    ]
elif preset == "D. Low-chemical / Sensitive":
    default_ings = [
        {"name": "SLES (70% active)", "percent": 6.0, "active_frac": 0.70, "cost_per_kg": 0.0},
        {"name": "CAPB (30% active)", "percent": 4.0, "active_frac": 0.30, "cost_per_kg": 0.0},
        {"name": "APG (50% active)", "percent": 4.0, "active_frac": 0.50, "cost_per_kg": 0.0},
        {"name": "NaCl (Salt for viscosity)", "percent": 1.5, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Citric Acid (pH adjust)", "percent": 0.20, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Preservative", "percent": 0.30, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Fragrance", "percent": 0.30, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Dye", "percent": 0.01, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Water (QS to 100%)", "percent": 83.69, "active_frac": 0.00, "cost_per_kg": 0.0},
    ]
else:  # Medium Foam + Thick
    default_ings = [
        {"name": "SLES (70% active)", "percent": 12.0, "active_frac": 0.70, "cost_per_kg": 0.0},
        {"name": "SLS (Needles/Powder, 95% active)", "percent": 2.0, "active_frac": 0.95, "cost_per_kg": 0.0},
        {"name": "CAPB (30% active)", "percent": 4.0, "active_frac": 0.30, "cost_per_kg": 0.0},
        {"name": "NaCl (Salt for viscosity)", "percent": 2.0, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Citric Acid (pH adjust)", "percent": 0.20, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Preservative", "percent": 0.30, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Fragrance (Lemon/Lime)", "percent": 0.50, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Dye (Color)", "percent": 0.01, "active_frac": 0.00, "cost_per_kg": 0.0},
        {"name": "Water (QS to 100%)", "percent": 78.99, "active_frac": 0.00, "cost_per_kg": 0.0},
    ]

st.sidebar.subheader("Global Settings")
final_density = st.sidebar.number_input("Final product density (kg/L)", min_value=0.8, max_value=1.2, value=1.0, step=0.01,
                                        help="Typically ~1.00 kg/L. Adjust if you know your blend density.")
batch_unit = st.sidebar.selectbox("Batch input unit", ["Liters (final volume)", "Kilograms (final mass)"])
batch_size = st.sidebar.number_input("Batch size", min_value=0.1, value=20.0, step=0.5)

colA, colB = st.columns([2, 1])

with colA:
    st.subheader("1) Ingredients — % and Active Fractions")
    st.markdown("**မှတ်ချက်:** Water ကို 100% အဖြစ် ပါစေဖို့ အသားတင် (QS) လုပ်ပါမယ်။ % တွေကို ပြင်ပြီးသားဆိုရင် Water ကို app က အလိုအလျှောက်ပြန်ညှိပေးနိုင်ပါတယ်။")

    # Editable table
    df = pd.DataFrame(default_ings)
    df = st.data_editor(
        df,
        num_rows="dynamic",
        column_config={
            "name": st.column_config.TextColumn("Ingredient (Raw Material)"),
            "percent": st.column_config.NumberColumn("% (w/w)", step=0.01, help="Enter composition percentage"),
            "active_frac": st.column_config.NumberColumn("Active Fraction (0–1)", step=0.01, help="e.g., SLES 70% -> 0.70"),
            "cost_per_kg": st.column_config.NumberColumn("Cost per kg (optional)", step=0.01, help="USD/THB/MMK per kg"),
        },
        hide_index=True,
    )

    # Auto-fix water to 100%
    total_pct = float(df["percent"].sum())
    # If there is a row with "Water" in its name, adjust to hit 100%
    water_mask = df["name"].str.contains("Water", case=False, na=False)
    if any(water_mask):
        non_water_total = float(df.loc[~water_mask, "percent"].sum())
        new_water = max(0.0, 100.0 - non_water_total)
        df.loc[water_mask, "percent"] = new_water
        total_pct = float(df["percent"].sum())

    if abs(total_pct - 100.0) > 0.01:
        st.warning(f"Total = {total_pct:.2f}% (should be 100%). Adjust numbers or ensure a Water row exists for auto-QS.")

    am_percent = 0.0
    for _, r in df.iterrows():
        am_percent += r["percent"] * float(r.get("active_frac", 0.0))
    am_percent = am_percent / 100.0 * 100.0

    st.metric("Active Matter (AM%)", f"{am_percent:.2f}%")

with colB:
    st.subheader("2) Bottle / Cost (optional)")
    bottle_size_ml = st.number_input("Bottle size (mL)", min_value=50, value=500, step=50)
    bottle_loss = st.number_input("Production loss allowance %", min_value=0.0, value=1.0, step=0.5,
                                  help="Fill losses, spillage etc.")
    st.caption("Cost per kg ကို Ingredients table ထဲကနေ ထည့်နိုင်သည်။")

# Compute batch mass in kg
if batch_unit.startswith("Liters"):
    batch_mass_kg = batch_size * final_density
else:
    batch_mass_kg = batch_size

# Build output table
rows = []
for _, r in df.iterrows():
    pct = float(r["percent"])
    kg = batch_mass_kg * pct / 100.0
    g = kg * 1000.0
    cost_per_kg = safe_float(r.get("cost_per_kg", 0.0))
    cost = kg * cost_per_kg
    rows.append(
        {
            "Ingredient": r["name"],
            "%": round(pct, 4),
            "kg (this batch)": round(kg, 4),
            "g (this batch)": round(g, 1),
            "Cost per kg": round(cost_per_kg, 4),
            "Cost (this batch)": round(cost, 4),
        }
    )

out_df = pd.DataFrame(rows)

st.subheader("3) Batch Weights & Cost")
st.dataframe(out_df, use_container_width=True)

# Totals
total_cost = float(out_df["Cost (this batch)"].sum())
st.write(f"**Batch mass:** {batch_mass_kg:.3f} kg  |  **Estimated total cost:** {total_cost:.2f}")

# Bottles calc
# Account for loss %
usable_mass_kg = batch_mass_kg * (1.0 - bottle_loss / 100.0)
usable_liters = usable_mass_kg / final_density
bottle_count = int((usable_liters * 1000.0) // bottle_size_ml)

st.subheader("4) Packaging Estimate")
st.write(
    f"Usable volume ≈ **{usable_liters:.2f} L** after losses → "
    f"**{bottle_count} bottles** of {bottle_size_ml} mL"
)

# CSV export
csv = out_df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download CSV (batch breakdown)", data=csv, file_name="dishwashing_batch_breakdown.csv", mime="text/csv")

st.divider()
with st.expander("📌 Practical Notes (မြန်မာလို)"):
    st.markdown(
        """
**Formulation Tips:**
- **SLES/SLS/CAPB/APG Active %** မတိတိကျကျသိလျှင် Supplier COA ကိုစစ်ပါ (e.g., SLES 70%).
- **Viscosity** ကို **NaCl** ဖြင့်အနည်းငယ်ချင်း တိုးပါ—တစ်ခါတည်း မထည့်ပါနှင့် (0.3–0.5% စတင်, မျက်နှာပြင်နှေးလာရင် တဖြည်းဖြည်း တိုး).
- **pH target** ~ 6.0–7.0 (Citric Acid ဖြင့်ချိုသာညှိ). pH မီတာ သုံးချင်မလား?
- **Preservative** ကို Supplier usage rate အတိုင်း (ပုံမှန် 0.2–0.5%) ထားပါ.
- **Fragrance** 0.2–0.7% အတွင်း စမ်းသပ်ပါ—အလွန်များလျှင် cloudiness ဖြစ်နိုင်.
- အရင်ဆုံး **pilot 1–2 L** စမ်းပြီးမှ production တိုးပါ။
        """
    )
