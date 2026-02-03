# PreTeXt Structure for Statistical Thinking for the 21st Century

This directory contains the PreTeXt source files for the textbook "Statistical Thinking for the 21st Century" by Russell A. Poldrack.

## Structure

- **project.ptx** - Main project configuration file
- **source/** - Contains all PreTeXt source files
  - **main.ptx** - Main book file that includes all chapters
  - **ch-*.ptx** - Individual chapter files
- **publication/** - Publication settings for different output formats
- **output/** - Generated output files (HTML, PDF, LaTeX) - excluded from git

## Chapters

The book is organized into the following chapters:

1. Introduction
2. Working with Data
3. Summarizing Data
4. Data Visualization
5. Fitting Models to Data
6. Probability
7. Sampling
8. Resampling and Simulation
9. Hypothesis Testing
10. Quantifying Effects and Designing Studies
11. Bayesian Statistics
12. Modeling Categorical Relationships
13. Modeling Continuous Relationships
14. The General Linear Model
15. Comparing Means
16. Multivariate Statistics
17. Practical Statistical Modeling
18. Doing Reproducible Research

## Building the Book

To build the PreTeXt book, you'll need to install the PreTeXt CLI:

```bash
pip install pretextbook
```

Then you can build the book in different formats:

### HTML
```bash
pretext build html
```

### PDF
```bash
pretext build pdf
```

### LaTeX
```bash
pretext build latex
```

## More Information

For more information about PreTeXt, visit:
- PreTeXt Guide: https://pretextbook.org/documentation.html
- PreTeXt GitHub: https://github.com/PreTeXtBook/pretext

## License

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
