# Population Data Visualizer — PS No. 31

## Requirements
- Python 3
- pandas
- matplotlib

## Installation
Open a terminal in this folder and run:

```bash
python -m pip install pandas matplotlib
```

## Run
```bash
python population_visualizer.py
```

Keep `population_visualizer.py` and `population.csv` in the same folder.

## Menu
1. Population Summary — latest-year total, largest city, fastest-growing city.
2. Growth Analysis and Charts — growth percentages, a bar chart, and a line chart.
3. Exit.

The program validates the City, Year, and Population columns, skips invalid rows,
removes duplicate City-Year records (keeping the last one), and calculates
growth as `(latest population - earliest population) / earliest population * 100`.

## Test the other university cases
- Case 2: Replace the contents of `population.csv` with:
  `City,Year,Population` then `Raipur,2024,1100000`.
- Case 3: Replace the contents with:
  `City,Year,Population` then `Raipur,2020,1000000`, `Durg,2020,abc`,
  `Bhilai,2020,-500`.
- Restore the original CSV to test Case 1 and Case 4.
