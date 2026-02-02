# PreTeXt Structure

This directory contains the PreTeXt source files for the "Statistical Thinking for the 21st Century" textbook.

## Structure

- `main.ptx` - Main PreTeXt book file that includes all other files
- `frontmatter.ptx` - Preface and front matter content
- `ch-*.ptx` - Chapter files (one per chapter)
- `backmatter.ptx` - References and back matter

## Building

To build the PreTeXt book, you need to have PreTeXt installed:

```bash
pip install pretext
```

Install Playwright browsers (required for some PreTeXt features):

```bash
playwright install chromium
```

Then build the HTML version:

```bash
pretext build html
```

Or build the PDF version:

```bash
pretext build pdf
```

The output will be in the `output/` directory.

### Troubleshooting Build Issues

If you encounter issues with Runestone services during build (e.g., "cannot access local variable 'services_xml'"), this typically means PreTeXt cannot download external dependencies. This usually works fine in CI/CD environments like GitHub Actions with proper internet access, but may fail in restricted network environments.

## Chapter Structure

The chapters follow the same structure as the original Rmd files:

1. **Introduction** - Introduction to statistical thinking
2. **Working with data** - Understanding data types and structures
3. **Summarizing data** - Measures of central tendency and variability
4. **Data Visualization** - Principles and techniques for visualizing data
5. **Fitting models to data** - Statistical modeling concepts
6. **Probability** - Fundamentals of probability theory
7. **Sampling** - Sampling methods and inference
8. **Resampling and simulation** - Bootstrap and Monte Carlo methods
9. **Hypothesis testing** - Framework for hypothesis testing
10. **Quantifying effects and designing studies** - Confidence intervals, effect sizes, and power
11. **Bayesian statistics** - Bayesian approach to inference
12. **Modeling categorical relationships** - Methods for categorical data
13. **Modeling continuous relationships** - Correlation and regression
14. **The General Linear Model** - Unified framework for statistical modeling
15. **Comparing means** - t-tests and ANOVA
16. **Multivariate statistics** - PCA and factor analysis
17. **Practical statistical modeling** - Real-world applications
18. **Doing reproducible research** - Best practices for reproducibility

## Deployment

The PreTeXt book is automatically built and deployed to GitHub Pages when changes are pushed to the master branch via the GitHub Actions workflow `.github/workflows/deploy-pretext.yml`.

## Contributing

This is a skeleton structure with placeholder content. To fully populate the chapters with content from the original Rmd files, contributors should:

1. Copy content from the corresponding Rmd files
2. Convert R Markdown syntax to PreTeXt XML syntax
3. Adapt code blocks and figures to PreTeXt format
4. Test the build locally before committing

For more information on PreTeXt syntax, see the [PreTeXt Guide](https://pretextbook.org/doc/guide/html/guide-toc.html).
