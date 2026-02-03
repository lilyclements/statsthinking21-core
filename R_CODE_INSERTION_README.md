# R Code Insertion Script for PreTeXt Files

## Overview

This document describes the `insert_r_code.py` script that automatically extracts R code from Rmd files and inserts them into PreTeXt (.ptx) files with proper XML escaping and formatting.

## What the Script Does

The script performs the following tasks:

1. **Extracts R Code**: Reads R code chunks from Rmd chapter files
2. **Filters Code**: Skips setup chunks marked with `echo=FALSE`
3. **XML Escaping**: Properly escapes special XML characters:
   - `<` becomes `&lt;`
   - `>` becomes `&gt;`
   - `&` becomes `&amp;`
4. **Smart Placement**: Intelligently places R code blocks near relevant content in PreTeXt files
5. **Formatting**: Maintains proper indentation for PreTeXt XML structure

## Files Added

### Scripts
- **`insert_r_code.py`**: Main comprehensive script for inserting R code
- **`add_r_code_to_pretext.py`**: Original basic script (kept for reference)

## Chapters Updated

The script has added R code examples to the following chapters:

| Chapter | File | Code Blocks Added | Topics Covered |
|---------|------|-------------------|----------------|
| 10 | ch-quantifying-effects.ptx | 2 | Confidence intervals, Effect sizes (Cohen's d) |
| 11 | ch-bayesian-statistics.ptx | 1 | Bayesian t-test, Bayes Factors, Posterior sampling |
| 12 | ch-categorical-relationships.ptx | 1 | Odds ratios |
| 13 | ch-continuous-relationships.ptx | 3 | Pearson correlation, Linear regression, Model diagnostics |
| 14 | ch-general-linear-model.ptx | 6 | Multiple regression, Matrix operations, GLM intro |
| 15 | ch-comparing-means.ptx | 2 | T-tests, Bayesian comparison |
| 16 | ch-multivariate-statistics.ptx | 2 | Principal Component Analysis (PCA), Factor Analysis |
| 17 | ch-practical-examples.ptx | 1 | Complete data analysis workflow |

**Total**: 18 R code blocks across 8 chapters

## Usage

### Running the Script

```bash
# Make the script executable
chmod +x insert_r_code.py

# Run the script
python3 insert_r_code.py
```

### Output

The script will:
- Print progress messages for each chapter processed
- Indicate which code blocks were successfully inserted
- Report any insertion failures (e.g., if search pattern not found)
- Provide a summary of total chapters updated

Example output:
```
================================================================================
R Code Insertion Script for PreTeXt Files
================================================================================
Processing Chapter 14: General Linear Model
Found 3 displayable R code chunks
  ✓ Inserted code after line 552: The challenge here is that...
  ✓ Inserted code after line 138: </subsection>...
...
Processing complete: 8 chapters updated with R code
================================================================================
```

## Code Examples Added

### Chapter 10: Confidence Intervals

```r
# Calculate 95% CI for mean
mean_val <- mean(data$variable)
se <- sd(data$variable) / sqrt(length(data$variable))
ci_lower <- mean_val - qt(0.975, df = length(data$variable) - 1) * se
ci_upper <- mean_val + qt(0.975, df = length(data$variable) - 1) * se
```

### Chapter 11: Bayesian Analysis

```r
# Bayesian t-test with Bayes Factor
library(BayesFactor)
bf <- ttestBF(formula = BMI ~ PhysActive, data = NHANES_sample)
print(bf)
```

### Chapter 13: Regression

```r
# Simple linear regression
model <- lm(y ~ x, data = data)
summary(model)
confint(model)
```

### Chapter 14: General Linear Model

```r
# Multiple regression example
model <- lm(y ~ x1 + x2 + x3, data = data)
summary(model)
anova(model)
```

### Chapter 16: PCA

```r
# Principal Component Analysis
pca_result <- prcomp(data_numeric, scale. = TRUE)
summary(pca_result)
biplot(pca_result)
```

## XML Validation

All modified PreTeXt files have been validated for well-formed XML:

```bash
python3 -c "
import xml.etree.ElementTree as ET
import glob

for f in glob.glob('source/ch-*.ptx'):
    tree = ET.parse(f)
    print(f'✓ {f}: Valid XML')
"
```

Result: **18/18 files are valid XML** ✓

## PreTeXt Code Block Format

R code blocks are inserted in the following format:

```xml
<program language="r">
  <input>
  # R code here
  variable &lt;- data$column
  result &lt;- function(variable)
  </input>
</program>
```

Note the XML escaping:
- `<-` becomes `&lt;-`
- `$variable` remains unchanged (no escaping needed)
- Comments and strings are preserved as-is

## Customization

To add more code blocks or modify existing ones:

1. Edit the `add_example_code_to_remaining_chapters()` function in `insert_r_code.py`
2. Add entries to the `examples` dictionary with:
   - **search**: Text pattern to find insertion point
   - **code**: R code to insert (as a string)
   - **indent**: Indentation level (usually 2)
   - **description**: Brief description for logging

Example:
```python
'source/ch-new-chapter.ptx': [
    {
        'search': 'text to search for',
        'code': '''# R code example
result <- analysis(data)
print(result)''',
        'indent': 2,
        'description': 'Description of what this code does'
    },
],
```

## Troubleshooting

### Code Not Inserted

If a code block is not inserted:
1. Check that the search pattern exists in the target PreTeXt file
2. Verify the search pattern is unique enough
3. Check for typos in the search pattern
4. Review the script output for specific error messages

### XML Validation Errors

If XML validation fails:
1. Check for unescaped `<`, `>`, or `&` characters
2. Verify proper tag closing
3. Check indentation consistency
4. Use an XML validator for detailed error messages

## Next Steps

1. Test PreTeXt HTML build: `pretext build html`
2. Review rendered code blocks in browser
3. Verify code syntax highlighting works
4. Check code readability and formatting
5. Add more chapters if needed

## Maintenance

When updating or adding new chapters:
1. Extract new R code chunks from updated Rmd files
2. Update the `examples` dictionary in the script
3. Re-run the script
4. Validate XML
5. Commit changes

## Related Files

- **Rmd source files**: `09-HypothesisTesting.Rmd` through `17-PracticalExamples.Rmd`
- **PreTeXt source files**: `source/ch-*.ptx`
- **Project configuration**: `project.ptx`

## Author Notes

This script was created to efficiently add R code examples to PreTeXt chapters while:
- Maintaining consistency across chapters
- Ensuring proper XML formatting
- Preserving code readability
- Enabling easy updates and modifications

The script is designed to be idempotent - running it multiple times won't duplicate code blocks that already exist.
