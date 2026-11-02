#Name = Mantosh Yadav
#email = mantosh0180@gmail.com 
#erp = Ru-26-02950
#section = B5
#Ps no. = 31


"""
PS No. 31 - Population Data Visualizer
Run: python population_visualizer.py
Required packages: pandas, matplotlib
Install: python -m pip install pandas matplotlib
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = Path(__file__).with_name("population.csv")


def load_and_clean_data(file_path=CSV_FILE):   
    """Load CSV data, validate rows, and remove duplicate city-year entries."""
    try:
        raw = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: '{file_path}' was not found.")
        return pd.DataFrame(columns=["City", "Year", "Population"])
    except Exception as error:
        print(f"Error reading CSV file: {error}")
        return pd.DataFrame(columns=["City", "Year", "Population"])

    required = {"City", "Year", "Population"}
    if not required.issubset(raw.columns):
        missing = ", ".join(sorted(required - set(raw.columns)))
        print(f"Error: CSV is missing required column(s): {missing}")
        return pd.DataFrame(columns=["City", "Year", "Population"])

    # Keep only the columns required by the project.
    data = raw[["City", "Year", "Population"]].copy()
    data["City"] = data["City"].astype("string").str.strip()
    data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
    data["Population"] = pd.to_numeric(data["Population"], errors="coerce")

    valid = (
        data["City"].notna()
        & data["City"].ne("")
        & data["Year"].notna()
        & data["Population"].notna()
        & data["Population"].gt(0)
        & data["Year"].mod(1).eq(0)
    )

    # Report invalid rows using CSV line numbers (header is line 1).
    for index, row in data.loc[~valid].iterrows():
        csv_line = index + 2
        if pd.isna(row["Population"]):
            reason = "invalid Population"
        elif pd.notna(row["Population"]) and row["Population"] <= 0:
            reason = "Population must be positive"
        elif pd.isna(row["Year"]) or (pd.notna(row["Year"]) and row["Year"] % 1 != 0):
            reason = "invalid Year"
        else:
            reason = "invalid City"
        print(f"Row {csv_line} skipped: {reason}.")

    clean = data.loc[valid].copy()
    clean["Year"] = clean["Year"].astype(int)
    clean["Population"] = clean["Population"].astype(int)

    # For repeated city/year records, keep the last occurrence.
    duplicate_mask = clean.duplicated(subset=["City", "Year"], keep="last")
    if duplicate_mask.any():
        print(f"Duplicate city/year rows removed: {int(duplicate_mask.sum())}")
        clean = clean.loc[~duplicate_mask]

    clean = clean.sort_values(["City", "Year"]).reset_index(drop=True)
    print(f"Valid rows: {len(clean)}")
    return clean

# Purpose: Reads the CSV file, validates required columns and values, removes invalid or duplicate records, and returns cleaned population data ready for analysis.


def calculate_city_growth(data):
    """Calculate growth from each city's earliest to latest available year."""
    results = []

    for city, group in data.groupby("City"):
        group = group.sort_values("Year")
        first = group.iloc[0]
        latest = group.iloc[-1]

        if first["Year"] == latest["Year"]:
            continue

        growth = ((latest["Population"] - first["Population"])
                  / first["Population"]) * 100

        results.append({
            "City": city,
            "Earliest Year": int(first["Year"]),
            "Latest Year": int(latest["Year"]),
            "Earliest Population": int(first["Population"]),
            "Latest Population": int(latest["Population"]),
            "Growth (%)": growth
        })

    return pd.DataFrame(results)

# Purpose: Compares each city's earliest and latest recorded population values to calculate percentage growth for the full period.


def show_summary(data):
    """Display total population, largest city and fastest-growing city."""
    if data.empty:
        print("No valid population data available.")
        return

    latest_year = int(data["Year"].max())
    latest_data = data[data["Year"] == latest_year]
    total_population = int(latest_data["Population"].sum())
    largest = latest_data.loc[latest_data["Population"].idxmax()]

    print(f"\nTotal population ({latest_year}): {total_population}")
    print(f"Largest city: {largest['City']} ({int(largest['Population'])})")

    growth = calculate_city_growth(data)
    if growth.empty:
        print("Growth: not available (only one year of data)")
    else:
        fastest = growth.loc[growth["Growth (%)"].idxmax()]
        print(f"Fastest growing: {fastest['City']} (+{fastest['Growth (%)']:.2f}%)")

# Purpose: Prints the total population, the largest city in the newest year, and the city with the strongest growth trend.


def show_growth_and_charts(data):
    """Display city growth and create bar and line charts."""
    if data.empty:
        print("No valid population data available for charts.")
        return

    growth = calculate_city_growth(data)
    if growth.empty:
        print("Growth analysis not available: each city needs at least two years of data.")
        return

    print("\nPopulation growth by city:")
    for _, row in growth.iterrows():
        print(f"{row['City']}: {row['Growth (%)']:+.2f}%")

    # Bar chart: percentage growth by city.
    plt.figure(figsize=(8, 5))
    bars = plt.bar(growth["City"], growth["Growth (%)"])
    plt.title("Population Growth by City")
    plt.xlabel("City")
    plt.ylabel("Growth (%)")
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.bar_label(bars, fmt="%.2f%%", padding=3)
    plt.tight_layout()
    plt.savefig(Path(__file__).with_name("population_growth.png"), dpi=150)

    # Line chart: population over time for each city.
    plt.figure(figsize=(8, 5))
    for city, group in data.groupby("City"):
        group = group.sort_values("Year")
        plt.plot(group["Year"], group["Population"], marker="o", label=city)

    plt.title("Population Trend")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.legend(title="City")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(Path(__file__).with_name("population_trend.png"), dpi=150)

    print("\nCharts saved as population_growth.png and population_trend.png.")
    plt.show()

# Purpose: Creates visual summaries of city growth by generating a bar chart and a multi-line population trend chart for each city.


def main():
    print("=" * 48)
    print("          POPULATION DATA VISUALIZER")
    print("=" * 48)

    data = load_and_clean_data()

    while True:
        print("\nMENU")
        print("1. Population Summary")
        print("2. Growth Analysis and Charts")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            show_summary(data)
        elif choice == "2":
            show_growth_and_charts(data)
        elif choice == "3":
            print("Thank you for using Population Data Visualizer!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Purpose: Runs the menu-driven program, loads the cleaned data, and lets the user choose between summary and chart-based analysis.


if __name__ == "__main__":
    main()
