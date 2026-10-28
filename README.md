# Daily Stock Report Pipeline

A notebook-orchestrated pipeline that turns five raw supply-chain files into one
multi-sheet daily stock report. It consolidates store stock, DC stock, sell-out
history, pending purchase orders, and supplier lead time, then calculates stock
coverage metrics (DOH, cover date, stock + PO cover) for every SKU across the
distribution centres.

The interactive Streamlit version of this report lives in
[`../streamlit_stock_report`](../streamlit_stock_report); this folder is the
batch/notebook pipeline only.

---

## Pipeline

```
raw files ──► notebook 1  clean CJ stock ─────────┐
          ──► notebook 2  clean DC stock ─────────┤
          ──► notebook 3  clean sell-out ─────────┼──► notebook 6  merge + metrics ──► final Excel
          ──► notebook 4  extract PO pending ─────┤
          ──► notebook 5  finalise PO pending ────┘
          ──► notebook 7  weekly stock prep ──────► weekly output (separate)
```

| Notebook | Input | Output |
|---|---|---|
| `1.cleaned_cj_stock_report.ipynb` | Weekly CJ stock workbook | `cleaned_CJ_Stock_Report.xlsx` |
| `2.cleaned_dc_stock.ipynb` | Daily DC stock workbook(s) | `cleaned_DC_daily_stock.xlsx` |
| `3.cleaned-sales_out.ipynb` | Sell-out past 30 days | `appended_cleaned_SellOut.xlsx` |
| `4.cleaned_po_pending_access.ipynb` | Access PO query | `cleaned_PO_pending_other.xlsx` |
| `5.finalize_po_pending.ipynb` | Notebook 4 output + lead time | finalised PO tables |
| `6.merged_daily_stock_report.ipynb` | Outputs 1–5 | final daily stock report |
| `7.prep_raw_weekly_stock.ipynb` | CJ + DC stock | weekly stock snapshot |

---

## Metrics

- **DOH (Days on Hand)** — current stock ÷ average daily sales (90-day basis),
  per DC and combined.
- **DOH (Stock + PO)** — (stock + pending PO) ÷ average daily sales, with
  delivery-date awareness: a PO only counts toward cover if it lands before the
  projected stock-out date.
- **Cover Date** — projected date the stock (or stock + PO) runs out.
- **NPD** — flags SKUs within 15 days of their first sell-out date.
- **SO split by DC** — last 7-day and 30-day sell-out apportioned to each DC using
  a 90-day sales ratio.
- **Carton view** — quantity converted from pieces to cartons using `PC_Cartons`.

Business rules are parameterised in [`config.py`](config.py): DC list and plant
mapping, excluded divisions, soft-serve unit conversion, DOH caps, and duplicate
SKU handling.

---

## Project layout

```
DAILY_STOCK_REPORT/
├── config.py                  # paths, mappings, thresholds, notebook order
├── notebooks/
│   ├── 1.cleaned_cj_stock_report.ipynb
│   ├── 2.cleaned_dc_stock.ipynb
│   ├── 3.cleaned-sales_out.ipynb
│   ├── 4.cleaned_po_pending_access.ipynb
│   ├── 5.finalize_po_pending.ipynb
│   ├── 6.merged_daily_stock_report.ipynb
│   └── 7.prep_raw_weekly_stock.ipynb
├── scripts/
│   └── run_all_notebooks.py   # runs notebooks 1–6 in order
├── data/                      # local input/output (not committed)
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt      # runtime + Jupyter
# or: pip install -r requirements.txt    # runtime only
```

The notebooks do `import config`, so the project root must be importable. Either
launch Jupyter from the project root with the root on `PYTHONPATH`, or add a
`.pth` file to the virtual environment:

```powershell
# .venv\Lib\site-packages\project_root.pth
# contents: absolute path to this folder, e.g.
C:\path\to\DAILY_STOCK_REPORT
```

Notebooks 4–6 read the product/PO master from Microsoft Access, so the
**Microsoft Access Database Engine (x64)** must be installed and matched to the
Python bitness. If you only run the CJ/DC/sell-out part, you can stop after
notebook 3.

---

## Run

1. Put the source files in `data/raw/` (see [`data/README.md`](data/README.md)),
   or point the environment variables at your own folders:

   ```powershell
   $env:STOCK_REPORT_DATA_DIR = "D:\stock-report\data"
   # optional individual overrides
   $env:CJ_STOCK_SOURCE_DIR   = "D:\stock-report\raw\cj_stock"
   $env:ACCESS_DB_PATH        = "D:\stock-report\raw\master.accdb"
   ```

2. Run the whole pipeline:

   ```bash
   python scripts/run_all_notebooks.py
   ```

   Or open the notebooks in order (1 → 6) and run them interactively.

3. The final report is written to `data/output/` (or `STOCK_REPORT_OUTPUT_DIR`).

---

## Output

`Sahamit Daily Stock Report_<date>.xlsx` with four sheets:

| Sheet | Description |
|---|---|
| `Data by Qty` | Full stock report in unit quantity |
| `Data by Cartons` | Same data converted to cartons |
| `All PO Pending` | PO detail across divisions |
| `MIN ETA` | Earliest delivery date per SKU per DC |

---

## Notes

- Divisions configured in `CJ_STOCK_EXCLUDE_DIVISIONS` and
  `SELLOUT_EXCLUDE_DIVISIONS` are filtered out in notebooks 1 and 3.
- DC names are normalised through `DC_NAME_MAPPING` / `DC_PLANT_MAPPING`.
- Soft-serve materials are converted from mL to grams using
  `SOFT_SERVE_CONVERSION_FACTOR`.
- DOH values above `DOH_MAX_RAW` are capped at `DOH_CAP_VALUE` for display.
- Duplicate `CJ_Item` rows are resolved with the rules in
  `SPECIAL_DUPLICATE_PRODUCTS` to avoid double counting stock.
- No company data, credentials, or internal paths are included in this
  repository. Use your own inputs and never commit business files.
