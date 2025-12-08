"""Prepare RAWGraphs Circle Packing input from `data.json`.

This script reads `data.json` (expected fields: `sector`, `asset`, `investment`),
aggregates/sanitizes the data, ensures there are 15-20 rows (creating synthetic
rows if needed), and writes `rawgraphs_circle_packing.csv` and
`rawgraphs_circle_packing.tsv` in the same folder. The CSV/TSV are ready to
copy-paste into RAWGraphs (https://rawgraphs.io/) and map:

- Hierarchy / Color: `sector`
- Label: `asset`
- Size: `investment`

The script prints concise RAWGraphs instructions after writing the files.
"""

import json
import os
import random
import pandas as pd


def ensure_min_rows(df, min_rows=15, seed=42):
    """If df has fewer than min_rows, append synthetic assets to reach min_rows.

    Synthetic rows copy sectors from existing data and sample investments
    based on the existing distribution to keep values realistic.
    """
    random.seed(seed)
    if len(df) >= min_rows:
        return df

    sectors = df['sector'].unique().tolist() if not df.empty else ['Other']
    mean = int(df['investment'].mean()) if len(df) > 0 else 1_000_000
    std = int(df['investment'].std()) if len(df) > 0 and df['investment'].std() > 0 else max(1, mean // 6)

    new_rows = []
    i = 1
    while len(df) + len(new_rows) < min_rows:
        sector = random.choice(sectors)
        asset = f"{sector} Asset {i}"
        invest = max(50_000, int(random.gauss(mean, std)))
        new_rows.append({'sector': sector, 'asset': asset, 'investment': invest})
        i += 1

    if new_rows:
        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

    return df


def main():
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, 'data.json')
    out_csv = os.path.join(base_dir, 'rawgraphs_circle_packing.csv')
    out_tsv = os.path.join(base_dir, 'rawgraphs_circle_packing.tsv')

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Place your `data.json` next to this script.")
        return

    with open(json_path, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
        except Exception as e:
            print('Error reading JSON:', e)
            return

    df = pd.DataFrame(data)
    if df.empty:
        print('No records found in data.json')
        return

    # Keep only expected columns and coerce investment to numeric
    expected_cols = ['sector', 'asset', 'investment']
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        print('Missing expected columns in data.json:', missing)
        return

    df = df[expected_cols].copy()
    df['investment'] = pd.to_numeric(df['investment'], errors='coerce').fillna(0).astype(int)

    # Aggregate duplicates
    df = df.groupby(['sector', 'asset'], as_index=False)['investment'].sum()

    # Ensure realistic 15-20 rows for RAWGraphs demo/exercise
    df = ensure_min_rows(df, min_rows=15)

    # Optionally sort for nicer presentation
    df = df.sort_values(['sector', 'investment'], ascending=[True, False])

    # Write CSV and TSV for RAWGraphs import (both human-friendly)
    df.to_csv(out_csv, index=False)
    df.to_csv(out_tsv, index=False, sep='\t')

    print(f'Wrote: {out_csv}')
    print(f'Wrote: {out_tsv}')
    print('\nRAWGraphs Circle Packing — quick mapping instructions:')
    print('- Open https://rawgraphs.io/ and choose "Circle Packing"')
    print("- Import: copy-paste the contents of `rawgraphs_circle_packing.csv` or upload it")
    print("- Map: 'sector' → Hierarchy / Color, 'asset' → Label, 'investment' → Size")
    print("- Customize: pick a professional palette (e.g. 'Set3' or 'Viridis'), enable labels")
    print("- Export: PNG at 300–512px (512x512 recommended for crispness)")
    print('\nThe CSV/TSV are ready for RAWGraphs Circle Packing import.')


if __name__ == '__main__':
    main()
