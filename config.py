import os
from pathlib import Path


# -----------------------------------------------------------------------------
# PATHS
# All paths can be overridden with environment variables, so the pipeline runs
# on any machine. Defaults are relative to this project folder.
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR     = Path(os.getenv('STOCK_REPORT_DATA_DIR', PROJECT_ROOT / 'data'))
RAW_DIR      = DATA_DIR / 'raw'

# SOURCE PATHS  (where raw data files come from) ==============================
CJ_STOCK_SOURCE_DIR     = str(Path(os.getenv('CJ_STOCK_SOURCE_DIR', RAW_DIR / 'cj_stock')))
DC_STOCK_SOURCE_DIR     = str(Path(os.getenv('DC_STOCK_SOURCE_DIR', RAW_DIR / 'dc_stock')))
SELLOUT_SOURCE_PATH     = str(Path(os.getenv('SELLOUT_SOURCE_PATH', RAW_DIR / 'sellout_past30D.xlsx')))
ACCESS_DB_PATH          = str(Path(os.getenv('ACCESS_DB_PATH', RAW_DIR / 'master.accdb')))
MASTER_LEADTIME_PATH    = str(Path(os.getenv('MASTER_LEADTIME_PATH', RAW_DIR / 'Master_LeadTime.xlsx')))
# =============================================================================


# PROCESSED / OUTPUT PATHS  (where cleaned files and final reports are saved)
# Intermediate cleaned files (produced by notebooks 1–5)
PROCESSED_DIR           = str(Path(os.getenv('STOCK_REPORT_PROCESSED_DIR', DATA_DIR / 'processed')))
# Final completed daily stock report (produced by notebook 6)
OUTPUT_DIR              = str(Path(os.getenv('STOCK_REPORT_OUTPUT_DIR', DATA_DIR / 'output')))

# Derived processed file paths — change PROCESSED_DIR above and these follow
CLEANED_CJ_STOCK_PATH   = os.path.join(PROCESSED_DIR, 'cleaned_CJ_Stock_Report.xlsx')
CLEANED_DC_STOCK_PATH   = os.path.join(PROCESSED_DIR, 'cleaned_DC_daily_stock.xlsx')
CLEANED_SELLOUT_PATH    = os.path.join(PROCESSED_DIR, 'appended_cleaned_SellOut.xlsx')
CLEANED_PO_PENDING_PATH = os.path.join(PROCESSED_DIR, 'cleaned_PO_pending_other.xlsx')
RAW_PO_PENDING_PATH     = os.path.join(PROCESSED_DIR, 'Raw_PO_pending.xlsx')
# =============================================================================


# FILE NAME PATTERNS  (for auto-detecting the latest dated file)
# == CJ STOCK ==
CJ_STOCK_FILE_PREFIX        = 'Sahamit Report '
CJ_STOCK_FILE_EXTENSION     = '.xlsx'
# == DC STOCK ==
DC_STOCK_FILE_PREFIX        = 'DC_End'
DC_STOCK_FILE_EXTENSION     = '.xlsx'
FILE_DATE_FORMAT            = '%d-%m-%Y'       # e.g. 14-05-2026
# =============================================================================


# SHEET NAMES
# --- Source sheet names (read from) ---
## === CJ STOCK ===
CJ_STOCK_SOURCE_SHEET       = 'Sahamit Report'
CJ_STOCK_SOURCE_HEADER_ROW  = 2

## === DC STOCK ===
DC_STOCK_SOURCE_SHEET       = 'Sheet1'

## === MASTER LEADTIME ===
MASTER_LEADTIME_SHEET       = 'All_Product'
MASTER_LEADTIME_HEADER_ROW  = 1                

# --- Processed/output sheet names (write to) ---
## === CJ STOCK ===
CJ_STOCK_OUTPUT_SHEET       = 'CJ Stock'

## === DC STOCK ===
DC_PIVOT_SHEET              = 'Pivot_DC_stock'
DC_CLEANED_SHEET            = 'cleaned data'

## === SALES OUT ===
SELLOUT_RAW_SHEET           = 'Daily SO'
SELLOUT_PIVOT_SHEET         = 'Pivot SO'

## === PO ACCESS ===
PO_PIVOT_SHEET              = 'Pivot All PO pending'
PO_CLEANED_SHEET            = 'cleaned data'

## === FINAL REPORT SHEETS ===
RAW_PO_ALL_SHEET            = 'All PO Pending'
RAW_PO_ETA_SHEET            = 'MIN ETA'
REPORT_QTY_SHEET            = 'Data by Qty'
REPORT_CTN_SHEET            = 'Data by Cartons'
# =============================================================================


# ACCESS DATABASE  (query names and filter values)
ACCESS_PO_QUERY_NAME        = 'qry_output_for_excel_new'
ACCESS_PRODUCT_QUERY_NAME   = 'qry_Product_List'
# =============================================================================


# DC CONFIGURATION
# Active DC list 
DC_LIST     = ['DC1', 'DC2', 'DC4', 'DC5']
DC_COLUMNS  = [1, 2, 4, 5]

# SAP Plant code → DC name (used in notebook 2)
DC_PLANT_MAPPING = {
    'D001': 'DC1',
    'D002': 'DC2',
    'D004': 'DC4',
    'D005': 'DC5',
}

# Thai warehouse name → DC code (used in notebooks 4 & 5)
DC_NAME_MAPPING = {
    'CJ DC1 ราชบุรี':'DC1',
    'CJ DC2 บางปะกง':'DC2',
    'DC โพธาราม':'DC1',
    'DC บางวัว 1':'DC2',
    'DC ขอนแก่น':'DC4',
    'DC บุรีรัมย์':'DC5',
    'DC บางวัว 2':'TD09',
}
# =============================================================================



# DIVISION FILTERS  (rows belonging to these divisions are excluded)
CJ_STOCK_EXCLUDE_DIVISIONS  = ['A-HOME', 'UNO']
SELLOUT_EXCLUDE_DIVISIONS   = ['A-HOME', 'LIFESTYLE']
# =============================================================================



# SOFT-SERVE PRODUCT HANDLING
# These materials are stocked in mL but sold in g — divide qty by the factor below
SOFT_SERVE_MATERIALS            = ['10000577', '10000578']
SOFT_SERVE_CONVERSION_FACTOR    = 13200
# =============================================================================


# DOH (DAYS ON HAND) THRESHOLDS
DOH_MAX_RAW     = 1825      # rows above this raw value are considered infinite
DOH_CAP_VALUE   = 365       # value applied when DOH exceeds DOH_MAX_RAW
# =============================================================================


# NPD (NEW PRODUCT) FLAG
NPD_DAYS_THRESHOLD = 15     # SKUs within this many days of first SO date → flagged "NPD"
# =============================================================================



# SPECIAL PRODUCTS — duplicate CJ_Item handling
# These SKUs appear under multiple SHM_Items (Supplier: ซัน ซัน).
# Custom logic zeroes out DC4 or non-DC4 columns per row to avoid double-counting.
SPECIAL_DUPLICATE_PRODUCTS = [
    '20000408', '20009203', '20014191',
    '20023778', '20023779', '20028264', '20039186',
]
# =============================================================================


# NOTEBOOK PATHS  (used by scripts/run_all_notebooks.py)
NOTEBOOK_DIR = os.path.join(PROJECT_ROOT, 'notebooks')

NOTEBOOK_PATHS = [
    os.path.join(NOTEBOOK_DIR, '1.cleaned_cj_stock_report.ipynb'),
    os.path.join(NOTEBOOK_DIR, '2.cleaned_dc_stock.ipynb'),
    os.path.join(NOTEBOOK_DIR, '3.cleaned-sales_out.ipynb'),
    os.path.join(NOTEBOOK_DIR, '4.cleaned_po_pending_access.ipynb'),
    os.path.join(NOTEBOOK_DIR, '5.finalize_po_pending.ipynb'),
    os.path.join(NOTEBOOK_DIR, '6.merged_daily_stock_report.ipynb'),
]
