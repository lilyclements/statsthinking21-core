# R Code in PreTeXt - Example

## Before (Rmd file only)
In the original Rmd files, R code was present but not transferred to PreTeXt:

```r
# From 09-HypothesisTesting.Rmd
sampSize <- 250

NHANES_sample <- 
  NHANES_adult %>%
  sample_n(sampSize)

sampleSummary <-
  NHANES_sample %>%
  group_by(PhysActive) %>%
  summarize(
    N = length(BMI),
    mean = mean(BMI),
    sd = sd(BMI)
  )
```

## After (PreTeXt .ptx file)
Now the R code is included in PreTeXt with proper XML formatting:

```xml
<program language="r">
  <input>
# sample 250 adults from NHANES and compute mean BMI separately for active
# and inactive individuals

sampSize &lt;- 250

NHANES_sample &lt;- 
  NHANES_adult %&gt;%
  sample_n(sampSize)

sampleSummary &lt;-
  NHANES_sample %&gt;%
  group_by(PhysActive) %&gt;%
  summarize(
    N = length(BMI),
    mean = mean(BMI),
    sd = sd(BMI)
  )
  </input>
</program>
```

## Key Features

1. **Proper XML Escaping**: 
   - `<-` becomes `&lt;-`
   - `%>%` becomes `%&gt;%`
   - `&` becomes `&amp;`

2. **PreTeXt Standard Format**:
   - Uses `<program language="r">` tag
   - Code wrapped in `<input>` tags
   - Maintains proper indentation

3. **Strategic Placement**:
   - Code placed near relevant tables, figures, or sections
   - Enhances learning by showing the code that generates results

## Coverage

The R code has been added to all major statistical chapters (9-17) covering:
- Hypothesis Testing
- Confidence Intervals & Effect Sizes  
- Bayesian Statistics
- Categorical & Continuous Relationships
- General Linear Models
- Comparing Means
- Multivariate Statistics
- Practical Examples

This makes the PreTeXt version complete with executable R code examples, matching the pedagogical value of the Rmd source files.
