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

Then build the HTML version:

```bash
pretext build html
```

Or build the PDF version:

```bash
pretext build pdf
```

The output will be in the `output/` directory.

## Chapter Structure

The chapters follow the same structure as the original Rmd files:

1. Introduction
2. Working with data
3. Summarizing data
4. Data Visualization
5. Fitting models to data
6. Probability
7. Sampling
8. Resampling and simulation
9. Hypothesis testing
10. Quantifying effects and designing studies
11. Bayesian statistics
12. Modeling categorical relationships
13. Modeling continuous relationships
14. The General Linear Model
15. Comparing means
16. Multivariate statistics
17. Practical statistical modeling
18. Doing reproducible research

## Deployment

The PreTeXt book is automatically built and deployed to GitHub Pages when changes are pushed to the master branch via the GitHub Actions workflow `.github/workflows/deploy-pretext.yml`.
