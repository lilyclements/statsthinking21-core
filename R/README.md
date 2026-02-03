# R Directory - Shared R Code

This directory contains shared R code extracted from the individual chapter `.Rmd` files. The purpose of this restructuring is to reduce code duplication and improve maintainability.

## Files

### `setup.R`
Common setup code used across all chapters:
- Core library imports (`tidyverse`, `cowplot`, `knitr`)
- Default knitr chunk options
- Display options (digits = 2)
- Colorblind-friendly palette (`cbPalette`)

**Usage in .Rmd files:**
```r
source("R/setup.R")
```

### `load_data.R`
Data loading and preprocessing functions:
- `load_nhanes()`: Loads and cleans the NHANES dataset
  - Removes duplicated IDs
  - Adds `isChild` indicator variable
  - Returns both full dataset and adult-only subset

**Usage in .Rmd files:**
```r
source("R/load_data.R")
nhanes_data <- load_nhanes()
NHANES <- nhanes_data$NHANES
NHANES_adult <- nhanes_data$NHANES_adult
```

## Benefits of This Structure

1. **Reduced Duplication**: Common code is defined once and reused across chapters
2. **Easier Maintenance**: Changes to setup code only need to be made in one place
3. **Consistency**: All chapters use the same setup and data loading procedures
4. **Clarity**: Chapter files focus on content rather than boilerplate code

## Migration Summary

The following code was extracted from individual chapter files:
- Library imports for `tidyverse`, `cowplot`, and `knitr`
- NHANES data loading and duplicate removal
- Colorblind palette definition
- Common knitr options and display settings

All 18 chapter `.Rmd` files plus `index.Rmd` now use these shared files.

## Generating Figures for PreTeXt

### `generate_comparing_means_figures.R`

Generates static PNG figures for the Comparing Means chapter (ch-comparing-means.ptx). The PreTeXt version requires pre-generated images, unlike the R Markdown version which generates them dynamically.

**To generate the figures:**
```bash
Rscript R/generate_comparing_means_figures.R
```

**Generated files:**
- `images/PotTVViolin.png` - Violin plots showing TV watching by marijuana use
- `images/BPfig.png` - Paired blood pressure measurements  
- `images/BPDiffHist.png` - Histogram of blood pressure differences
- `images/DrugTrial.png` - Box plots for clinical trial with three groups
- `images/FDist.png` - F distributions with different degrees of freedom

**Required packages:** ggplot2, tidyr, dplyr, cowplot

**Note:** The generated PNG files should be committed to the repository to ensure they're available during the GitHub Actions build process.
