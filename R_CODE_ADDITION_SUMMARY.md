# R Code Addition Summary

## Overview
This document summarizes the R code blocks that have been added to the PreTeXt versions of the Statistical Thinking for the 21st Century textbook.

## Issue Reference
GitHub Issue: "Add in R code to PreTeXt files"

The issue identified that R code in the Rmd files wasn't being transferred to the PreTeXt versions. The request was to add R code blocks using the PreTeXt `<program language="r">` format.

## Solution Implemented

### Scripts Created
1. **insert_r_code.py** - Comprehensive Python script that:
   - Extracts R code chunks from Rmd source files
   - Filters out echo=FALSE setup chunks (but key examples were manually added)
   - Implements proper XML escaping (`<` → `&lt;`, `>` → `&gt;`, `&` → `&amp;`)
   - Intelligently places code blocks near relevant content
   - Prevents duplicate insertions

2. **add_r_code_to_pretext.py** - Basic utility for code extraction and analysis

### Documentation Files
- **R_CODE_INSERTION_README.md** - Complete usage guide for the scripts
- **TASK_COMPLETION_SUMMARY.md** - Detailed task completion report
- **R_CODE_ADDITION_SUMMARY.md** - This summary document

## R Code Blocks Added by Chapter

### Chapter 9: Hypothesis Testing (3 blocks)
1. **BMI and Physical Activity Sample** - Sampling and summarizing NHANES data
2. **BMI Box Plot** - Visualization of BMI by physical activity status  
3. **Coin Flip Simulation** - Binomial distribution and simulation example

### Chapter 10: Quantifying Effects and Designing Studies (4 blocks)
1. **Confidence Intervals** - Computing confidence intervals
2. **Effect Size Calculations** - Effect size measures
3. **Power Analysis** - Statistical power calculations
4. **Bootstrap Methods** - Resampling techniques

### Chapter 11: Bayesian Statistics (2 blocks)
1. **Bayes Factor Calculation** - Computing Bayes factors
2. **Posterior Distribution** - Bayesian inference examples

### Chapter 12: Categorical Relationships (2 blocks)
1. **Chi-squared Test** - Candy color example with chi-squared calculation
2. **Odds Ratio** - Computing odds ratios for contingency tables

### Chapter 13: Continuous Relationships (3 blocks)
1. **Pearson Correlation** - Correlation coefficients and tests
2. **Linear Regression** - Simple linear regression models
3. **Correlation Matrix** - Multiple variable correlations

### Chapter 14: General Linear Model (9 blocks)
1. **Multiple Regression (intro)** - Basic multiple regression
2. **Multiple Regression (repeated)** - Additional examples
3. **Multiple Regression with NHANES** - Real data example
4. **Study Time and Grades** - Simulated example
5. **Matrix Operations** - Linear algebra approach to GLM
6. **Beta Coefficient Calculation** - Computing regression coefficients
7. **QQ Plots** - Model diagnostics
8. **Residual Analysis** - Additional model diagnostics
9. **Model Comparison** - Comparing different models

### Chapter 15: Comparing Means (2 blocks)
1. **Bayesian t-test** - Using BayesFactor package
2. **Independent Samples t-test** - Traditional and Welch t-tests

### Chapter 16: Multivariate Statistics (4 blocks)
1. **Principal Component Analysis** - PCA computation
2. **Variance Explained** - PCA variance analysis
3. **Correlation Heatmap** - Visualizing correlations
4. **Factor Analysis** - Factor analysis examples

### Chapter 17: Practical Examples (2 blocks)
1. **Weight Loss Analysis** - Analyzing A-to-Z diet study
2. **Residual Plot** - Diagnostic visualization

## Total Summary
- **9 chapters** enhanced with R code examples
- **31 total R code blocks** added across all chapters
- **All XML files validated** as well-formed
- **Proper XML escaping** implemented throughout

## Chapters Referenced in Original Issue

The issue mentioned these specific sections:
- ✅ Ch 9.3 - Hypothesis Testing (added)
- ✅ Ch 10.1.4, 10.3.1 - Quantifying Effects (added)
- ✅ Ch 11.6 - Bayesian Statistics (added)
- ✅ Ch 12.3, 12.6, 12.7 - Categorical Relationships (added)
- ✅ Ch 13.3.1, 13.3.2, 13.7.2 - Continuous Relationships (added)
- ✅ Ch 14 (intro), 14.1.4, 14.2, 14.3, 14.5, 14.9 - General Linear Model (added)
- ✅ Ch 15.1-15.6, 15.8 - Comparing Means (added)
- ✅ Ch 16.3, 16.4 - Multivariate Statistics (added)
- ✅ Ch 17.1.5, 17.1.7, 17.2 - Practical Examples (added)

## Format Example

The R code blocks follow the PreTeXt standard format:

```xml
<program language="r">
  <input>
# Sample R code with proper XML escaping
x &lt;- c(1, 2, 3, 4, 5)
mean_x &lt;- mean(x)
result &lt;- x %&gt;% 
  filter(value &gt; 2)
  </input>
</program>
```

## Validation

All PreTeXt chapter files have been validated:
- ✅ XML well-formedness checked
- ✅ Proper XML escaping verified
- ✅ Code block placement reviewed
- ✅ Indentation follows PreTeXt standards

## Future Maintenance

To add R code to additional chapters:
1. Use `insert_r_code.py` script as a starting point
2. Extract relevant code from Rmd files
3. Manually place code with proper XML escaping
4. Validate XML after changes
5. Test PreTeXt build process

## References

- Reference repository: `idemsinternational/dsbook-part-1`
- PreTeXt documentation: https://pretextbook.org/
- Script location: `/home/runner/work/statsthinking21-core/statsthinking21-core/insert_r_code.py`

## Files Modified

### Created
- `insert_r_code.py`
- `add_r_code_to_pretext.py`
- `R_CODE_INSERTION_README.md`
- `TASK_COMPLETION_SUMMARY.md`
- `R_CODE_ADDITION_SUMMARY.md`

### Modified
- `source/ch-hypothesis-testing.ptx`
- `source/ch-quantifying-effects.ptx`
- `source/ch-bayesian-statistics.ptx`
- `source/ch-categorical-relationships.ptx`
- `source/ch-continuous-relationships.ptx`
- `source/ch-general-linear-model.ptx`
- `source/ch-comparing-means.ptx`
- `source/ch-multivariate-statistics.ptx`
- `source/ch-practical-examples.ptx`

## Conclusion

The R code has been successfully added to the PreTeXt files, making the code examples visible and accessible in the PreTeXt version of the textbook, consistent with the approach used in the reference repository.
