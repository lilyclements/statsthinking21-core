# Generate figures for Comparing Means chapter (ch-comparing-means.ptx)
# This script generates the PNG files needed for the PreTeXt version

library(ggplot2)
library(tidyr)
library(dplyr)
library(cowplot)

# Set random seed for reproducibility
set.seed(123456)

# Load NHANES data
source("R/setup.R")
source("R/load_data.R")
nhanes_data <- load_nhanes()
NHANES <- nhanes_data$NHANES

NHANES_adult <- 
  NHANES %>%
  subset(Age>=18) %>%
  drop_na(BMI)

# Ensure images directory exists
if (!dir.exists("images")) {
  dir.create("images")
}

# ==============================================================================
# Figure 1: PotTVViolin.png
# Violin plots for TV watching by marijuana use
# ==============================================================================

# Create sample with tv watching and marijuana use
NHANES_sample <-
  NHANES_adult %>%
  drop_na(TVHrsDay, RegularMarij) %>%
  mutate(
    TVHrsNum = recode( #recode character values into numerical values
      TVHrsDay,
      "More_4_hr" = 5,
      "4_hr" = 4, 
      "2_hr" = 2,
      "1_hr" = 1, 
      "3_hr" = 3, 
      "0_to_1_hr" = 0.5,
      "0_hrs" = 0
    )
  ) %>%
  sample_n(200)

p1 <- ggplot(NHANES_sample, aes(RegularMarij, TVHrsNum)) +
  geom_violin(draw_quantiles = .50) +
  labs(
    x = "Regular marijuana user",
    y = "TV hours per day"
  )

lm_summary <- summary(lm(TVHrsNum ~ RegularMarij, data = NHANES_sample))

p2 <- ggplot(NHANES_sample, aes(RegularMarij, TVHrsNum)) +
  geom_violin() +
  annotate('segment', x = 1, y = lm_summary$coefficients[1,1],
           xend = 2,
           yend = lm_summary$coefficients[1,1] + lm_summary$coefficients[2,1],
           linetype = 'dotted') +
  labs(
    x = "Regular marijuana user",
    y = "TV hours per day"
  )

png("images/PotTVViolin.png", width = 800, height = 400)
plot_grid(p1, p2)
dev.off()

cat("Generated: images/PotTVViolin.png\n")

# ==============================================================================
# Figure 2: BPfig.png
# Blood pressure measurements - paired observations
# ==============================================================================

set.seed(12345678)

NHANES_sample <- 
  NHANES %>% 
  dplyr::filter(Age > 17 & !is.na(BPSys2) & !is.na(BPSys1)) %>%
  dplyr::select(BPSys1, BPSys2, ID) %>%
  sample_n(200)

NHANES_sample_tidy <- 
  NHANES_sample %>%
  gather(timepoint, BPsys, -ID)

NHANES_sample <- 
  NHANES_sample %>%
  mutate(
    diff = BPSys1 - BPSys2,
    diffPos = as.integer(diff > 0),
    meanBP = (BPSys1 + BPSys2) / 2
  )

p1 <- ggplot(NHANES_sample_tidy, aes(timepoint, BPsys)) + 
  geom_violin() +
  scale_x_discrete(
    labels = c("Time 1", "Time 2"),
  ) 

p2 <- p1 + geom_line(aes(group = ID))

png("images/BPfig.png", width = 800, height = 400)
plot_grid(p1, p2)
dev.off()

cat("Generated: images/BPfig.png\n")

# ==============================================================================
# Figure 3: BPDiffHist.png
# Histogram of blood pressure differences
# ==============================================================================

png("images/BPDiffHist.png", width = 400, height = 400)
ggplot(NHANES_sample, aes(diff)) + 
  geom_histogram(bins = 30) +
  geom_vline(xintercept = mean(NHANES_sample$diff), color = 'blue')
dev.off()

cat("Generated: images/BPDiffHist.png\n")

# ==============================================================================
# Figure 4: DrugTrial.png
# Box plots for clinical trial with three groups
# ==============================================================================

set.seed(123456)

nPerGroup <- 36
noiseSD <- 10
meanSysBP <- 140
effectSize <- 0.8

df <- data.frame(
  group = as.factor(c(rep('placebo', nPerGroup),
                    rep('drug1', nPerGroup),
                    rep('drug2', nPerGroup))),
  sysBP = NA
) 

df$sysBP[df$group == 'placebo'] <- rnorm(nPerGroup, mean = meanSysBP, sd = noiseSD)
df$sysBP[df$group == 'drug1'] <- rnorm(nPerGroup, mean = meanSysBP - noiseSD * effectSize, sd = noiseSD)
df$sysBP[df$group == 'drug2'] <- rnorm(nPerGroup, mean = meanSysBP, sd = noiseSD)

png("images/DrugTrial.png", width = 400, height = 400)
ggplot(df, aes(group, sysBP)) + geom_boxplot()
dev.off()

cat("Generated: images/DrugTrial.png\n")

# ==============================================================================
# Figure 5: FDist.png
# F distributions with different degrees of freedom
# ==============================================================================

fdata <- 
  data.frame(x = seq(0.1, 10, .1)) %>%
  mutate(
    f_1_1 = df(x, 1, 1),
    f_1_50 = df(x, 1, 50),
    f_10_50 = df(x, 10, 50)
  )

png("images/FDist.png", width = 400, height = 400)
ggplot(fdata, aes(x, f_1_1)) +
  geom_line() +
  geom_line(aes(x, f_1_50), linetype = 'dotted') +
  geom_line(aes(x, f_10_50), linetype = 'dashed') +
  labs(y = "Density", x = "F values")
dev.off()

cat("Generated: images/FDist.png\n")

cat("\nAll figures for Comparing Means chapter generated successfully!\n")
