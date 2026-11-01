# Skincare Product Catalogue — Data Cleaning

## Project Overview

This project focuses on preparing and cleaning a skincare product catalogue for further analysis and ingredient-based applications.

The dataset contains **244 skincare products**, with product information, ingredient lists, and CosIng-related data.

The cleaning process identifies possible duplicates, standardizes product information, checks ingredient-list quality, and documents manual-review decisions.

## Project Structure

```text
skincare-project/
├── data/
│   ├── raw/
│   │   └── moisturizers_with_cosing.csv
│   └── interim/
│       ├── manual_ingredient_review.xlsx
│       ├── additional_single_ingredient_review.csv
│       └── duplicate_manual_review.csv
├── notebooks/
│   └── 02_Clean_catalogue.ipynb
├── requirements.txt
└── README.md
```

## Installation

**1. Clone the repository**

```bash
git clone <repository-url>
cd skincare-project
```

Replace `<repository-url>` with the actual GitHub repository URL.

**2. Install dependencies**

Make sure Python is installed, then run:

```bash
python -m pip install -r requirements.txt
```

**3. Open the notebook**

Open the project folder in VS Code and navigate to:

`notebooks/02_Clean_catalogue.ipynb`

Select a Python environment with the required packages installed.

**4. Run the notebook**

Restart the kernel and select **Run All**.

The notebook uses paths relative to the project folder, so teammates do not need to modify paths when using the provided folder structure.

## Data Cleaning Workflow

The notebook performs the following operations:

1. Loads the original dataset while preserving a working copy.
2. Performs initial data-quality checks.
3. Standardizes product categories, brands, and names.
4. Detects exact duplicates, repeated barcodes, and similar product names.
5. Parses ingredient lists and identifies records requiring manual verification.
6. Compares ingredient lists for candidate duplicate products.
7. Loads completed manual-review decisions.
8. Applies reviewed product-category corrections.
9. Validates the cleaned dataset and exports provisional results.

## Current Results

| Metric | Result |
|---|---:|
| Original products | 244 |
| Potential duplicate pairs | 8 |
| Ingredient records reviewed | 11 |
| Duplicate pairs retained separately | 5 |
| Unresolved duplicate pairs | 2 |
| Proposed duplicate merges | 1 |

No products are automatically deleted.

## Output Files

Running the notebook generates:

- `data/interim/catalogue_provisional.csv` — cleaned product information with reviewed category corrections.
- `data/interim/ingredient_comparison.csv` — preliminary ingredient-similarity results for candidate duplicate pairs.

The three manual-review files are required inputs and should not be overwritten by the cleaning pipeline.

## Important Notes

- The original dataset is preserved.
- The catalogue is **provisional**, not a finalized dataset.
- Ingredient corrections are documented separately and are not yet fully integrated into the exported catalogue.
- The proposed duplicate merge has not yet been applied.
- Some product formulations and duplicate identities remain unverified.
- The facial sunscreen review has been postponed.
- Ingredient-name normalization against CosIng is planned for the next project step.

## Next Steps

- Normalize INCI ingredient names and aliases.
- Complete remaining manual verification.
- Finalize catalogue version 1 and its data dictionary.
- Curate ingredient reference information.

## Collaboration

Team members should preserve raw data, document cleaning decisions, and avoid deleting or merging products without supporting evidence.
