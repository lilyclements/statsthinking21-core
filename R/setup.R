# Common setup code for Statistical Thinking for the 21st Century
# This file contains library imports and common configurations used across chapters

# Core libraries used throughout the book
library(tidyverse)
library(cowplot)
library(knitr)

# Set default knitr options
knitr::opts_chunk$set(
  fig.width = 6, 
  fig.height = 6,
  warning = FALSE,
  message = FALSE
)

# Set display options
options(digits = 2)

# Colorblind-friendly palette
# from http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/#a-colorblind-friendly-palette
cbPalette <- c(
  "#999999", "#E69F00", "#56B4E9", "#009E73", 
  "#F0E442", "#0072B2", "#D55E00", "#CC79A7"
)
