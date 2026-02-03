# Images Needed for Hypothesis Testing Chapter

The following images need to be generated from the R code in `09-HypothesisTesting.Rmd` and placed in the `images/` directory:

## Required Images

1. **bmi_boxplot.png** (fig-bmi-sample)
   - Box plot of BMI data from NHANES dataset
   - Split by PhysActive (Yes/No)
   - Generated from bmiSample code chunk

2. **t_versus_normal.png** (fig-t-versus-normal)
   - Two panels showing t distribution vs normal distribution
   - Left: df=4, Right: df=1000
   - Generated from tVersusNormal code chunk

3. **coin_flips_histogram.png** (fig-coin-flips)
   - Histogram of simulated coin flips (100,000 runs)
   - Vertical line at observed value of 70 heads
   - Generated from coinFlips code chunk

4. **squat_boxplot.png** (fig-squat-boxplot)
   - Two panels: original and shuffled data
   - Box plots comparing FB vs XC groups
   - Generated from squatPlot code chunk

5. **shuffle_histogram.png** (fig-shuffle-hist)
   - Histogram of t-values after shuffling
   - Vertical line showing observed t statistic
   - Dotted line showing theoretical t distribution
   - Generated from shuffleHist code chunk

6. **sim_diff_histogram.png** (fig-sim-diff)
   - Histogram of t statistics for BMI/activity example
   - Vertical line showing observed value
   - Gray shading for extreme values
   - Generated from simDiff code chunk

7. **sig_results_sample_size.png** (fig-sig-results)
   - Line plot showing proportion of significant results vs sample size
   - Log scale on x-axis
   - Generated from sigResults code chunk

8. **null_simulation_histogram.png** (fig-null-sim)
   - Two panels: before and after Bonferroni correction
   - Histograms of significant results in multiple testing
   - Generated from nullSim code chunk

## How to Generate

Run the R code chunks in `09-HypothesisTesting.Rmd` and save the plots as PNG files with the names listed above.

The PreTeXt file (`source/ch-hypothesis-testing.ptx`) already references these image filenames.
