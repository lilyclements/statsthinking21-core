#!/usr/bin/env python3
"""
Comprehensive script to extract R code chunks from Rmd files and intelligently
add them to PreTeXt files.

This script:
- Reads Rmd files and extracts R code chunks (excluding echo=FALSE)
- Handles XML escaping properly (< > &)
- Intelligently places code near relevant sections using heuristics
- Preserves proper indentation for PreTeXt XML
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple


def xml_escape(text: str) -> str:
    """
    Escape special XML characters in code.
    """
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def extract_r_code_chunks(rmd_file: Path) -> List[Dict]:
    """
    Extract R code chunks from an Rmd file.
    Returns list of dicts with chunk metadata and code.
    """
    chunks = []
    
    with open(rmd_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match R code chunks: ```{r ...} ... ```
    pattern = r'```\{r\s*([^}]*)\}(.*?)```'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        chunk_header = match.group(1).strip()
        chunk_code = match.group(2).strip()
        
        # Skip empty chunks
        if not chunk_code:
            continue
        
        # Parse chunk options
        chunk_name = 'unnamed'
        has_echo_false = False
        
        if chunk_header:
            # First part might be the name
            parts = re.split(r',\s*', chunk_header)
            if parts and '=' not in parts[0]:
                chunk_name = parts[0].strip()
            
            # Check for echo=FALSE
            if re.search(r'echo\s*=\s*FALSE', chunk_header, re.IGNORECASE):
                has_echo_false = True
        
        # Skip chunks with echo=FALSE
        if has_echo_false:
            continue
        
        # Find line number
        line_num = content[:match.start()].count('\n') + 1
        
        # Extract context before and after chunk
        context_start = max(0, match.start() - 1000)
        context_before = content[context_start:match.start()]
        
        context_end = min(len(content), match.end() + 500)
        context_after = content[match.end():context_end]
        
        chunks.append({
            'name': chunk_name,
            'code': chunk_code,
            'line_num': line_num,
            'context_before': context_before,
            'context_after': context_after,
        })
    
    return chunks


def format_r_code_for_pretext(code: str, indent_level: int = 2) -> str:
    """
    Format R code for insertion into PreTeXt with proper XML escaping and indentation.
    
    Args:
        code: The R code to format
        indent_level: Number of indentation levels (each level = 2 spaces)
    """
    base_indent = '  ' * indent_level
    inner_indent = '  ' * (indent_level + 1)
    
    # Escape XML special characters
    escaped_code = xml_escape(code)
    
    result = f'{base_indent}<program language="r">\n'
    result += f'{inner_indent}<input>\n'
    
    # Add code lines with proper indentation
    for line in escaped_code.split('\n'):
        if line.strip():
            result += f'{inner_indent}{line}\n'
        else:
            result += '\n'
    
    result += f'{inner_indent}</input>\n'
    result += f'{base_indent}</program>'
    
    return result


def find_section_for_insertion(ptx_content: str, search_text: str, before=False) -> Optional[int]:
    """
    Find line number where code should be inserted in PreTeXt content.
    
    Args:
        ptx_content: The PreTeXt file content
        search_text: Text pattern to search for
        before: If True, insert before the pattern; if False, insert after
        
    Returns:
        Line number where to insert, or None if not found
    """
    lines = ptx_content.split('\n')
    
    for i, line in enumerate(lines):
        if search_text in line:
            return i if before else i + 1
    
    return None


def insert_code_blocks_in_chapter(ptx_file: Path, code_blocks: List[Tuple[str, str, int]]) -> bool:
    """
    Insert multiple code blocks into a PreTeXt file.
    
    Args:
        ptx_file: Path to PreTeXt file
        code_blocks: List of tuples (search_pattern, code, indent_level)
        
    Returns:
        True if any insertions were made
    """
    with open(ptx_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    insertions_made = 0
    
    # Process insertions in reverse order to maintain line numbers
    # Sort by line number (descending) so we insert from bottom to top
    insertion_points = []
    
    for search_pattern, code, indent_level in code_blocks:
        # Check if this code is already in the file
        if xml_escape(code[:50]) in content:
            print(f"  ⊘ Code already exists near: {search_pattern[:50]}...")
            continue
        
        insert_line = find_section_for_insertion(content, search_pattern, before=False)
        if insert_line is None:
            print(f"  ✗ Could not find insertion point for: {search_pattern[:60]}...")
            continue
        
        insertion_points.append((insert_line, code, indent_level, search_pattern))
    
    # Sort by line number (descending)
    insertion_points.sort(key=lambda x: x[0], reverse=True)
    
    # Insert from bottom to top
    for insert_line, code, indent_level, search_pattern in insertion_points:
        formatted_code = format_r_code_for_pretext(code, indent_level)
        lines.insert(insert_line, '')
        lines.insert(insert_line + 1, formatted_code)
        insertions_made += 1
        print(f"  ✓ Inserted code after line {insert_line}: {search_pattern[:50]}...")
    
    if insertions_made > 0:
        with open(ptx_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return True
    
    return False


def process_chapter_14(rmd_file: Path, ptx_file: Path) -> bool:
    """Process Chapter 14: General Linear Model - add displayable R code."""
    print(f"\nProcessing Chapter 14: General Linear Model")
    
    chunks = extract_r_code_chunks(rmd_file)
    print(f"Found {len(chunks)} displayable R code chunks")
    
    if not chunks:
        print("  No displayable chunks found")
        return False
    
    # Display found chunks
    for chunk in chunks:
        print(f"  - Chunk '{chunk['name']}' at line {chunk['line_num']}")
    
    code_blocks = []
    
    # Find and prepare code blocks for insertion
    for chunk in chunks:
        name = chunk['name']
        code = chunk['code']
        
        # Add code blocks to appropriate sections
        if name == 'unnamed' and 'df <-' in code and 'tibble' in code:
            # This is the matrix example code
            code_blocks.append((
                '</subsection>',  # Insert after a subsection end
                code,
                2  # indent level
            ))
        elif 'beta_hat' in code and 'ginv' in code:
            # This is the beta calculation code
            code_blocks.append((
                'The challenge here is that',
                code,
                2
            ))
    
    if code_blocks:
        return insert_code_blocks_in_chapter(ptx_file, code_blocks)
    
    print("  No appropriate insertion points found")
    return False


def process_chapter_15(rmd_file: Path, ptx_file: Path) -> bool:
    """Process Chapter 15: Comparing Means - add displayable R code."""
    print(f"\nProcessing Chapter 15: Comparing Means")
    
    chunks = extract_r_code_chunks(rmd_file)
    print(f"Found {len(chunks)} displayable R code chunks")
    
    if not chunks:
        print("  No displayable chunks found")
        return False
    
    for chunk in chunks:
        print(f"  - Chunk '{chunk['name']}' at line {chunk['line_num']}: {chunk['code'][:60]}...")
    
    code_blocks = []
    
    for chunk in chunks:
        code = chunk['code']
        
        # Bayesian t-test example
        if 'ttestBF' in code and 'BPDiaAve' in code:
            code_blocks.append((
                'the Bayes factor to quantify evidence',
                code,
                2
            ))
        # Mixed model example
        elif 'lmer' in code and 'BPsys' in code:
            code_blocks.append((
                'known as a <em>mixed model</em>',
                code,
                2
            ))
    
    if code_blocks:
        return insert_code_blocks_in_chapter(ptx_file, code_blocks)
    
    print("  No appropriate insertion points found")
    return False


def process_chapter_16(rmd_file: Path, ptx_file: Path) -> bool:
    """Process Chapter 16: Multivariate Statistics - add any displayable R code."""
    print(f"\nProcessing Chapter 16: Multivariate Statistics")
    
    chunks = extract_r_code_chunks(rmd_file)
    print(f"Found {len(chunks)} displayable R code chunks")
    
    if not chunks:
        print("  No displayable chunks found")
        return False
    
    for chunk in chunks:
        print(f"  - Chunk '{chunk['name']}' at line {chunk['line_num']}")
    
    # Chapter 16 seems to have displayable code - let's check
    # For now, just report what we found
    return False


def process_generic_chapter(chapter_num: int, chapter_name: str, rmd_file: Path, ptx_file: Path, 
                           insertion_rules: List[Dict]) -> bool:
    """
    Generic processor for chapters. Takes insertion rules to map code to sections.
    
    Args:
        chapter_num: Chapter number
        chapter_name: Chapter name for display
        rmd_file: Path to Rmd file
        ptx_file: Path to PreTeXt file
        insertion_rules: List of dicts with 'keyword' and 'after_text' keys
    """
    print(f"\nProcessing Chapter {chapter_num}: {chapter_name}")
    
    chunks = extract_r_code_chunks(rmd_file)
    print(f"Found {len(chunks)} displayable R code chunks")
    
    if not chunks:
        print("  No displayable chunks found")
        return False
    
    for chunk in chunks:
        print(f"  - Chunk '{chunk['name']}' at line {chunk['line_num']}")
    
    # Try to match chunks to insertion rules
    code_blocks = []
    
    for chunk in chunks:
        code = chunk['code']
        matched = False
        
        for rule in insertion_rules:
            keyword = rule.get('keyword', '')
            after_text = rule.get('after_text', '')
            
            if keyword in code:
                code_blocks.append((after_text, code, 2))
                matched = True
                break
        
        if not matched:
            # Try to find a good insertion point based on context
            context = chunk['context_before'][-200:]
            # Look for section headers in context
            if '###' in context or '##' in context:
                # Extract the section title
                lines = context.split('\n')
                for line in reversed(lines):
                    if line.strip().startswith('#'):
                        section_title = line.strip('#').strip()[:40]
                        code_blocks.append((section_title, code, 2))
                        break
    
    if code_blocks:
        return insert_code_blocks_in_chapter(ptx_file, code_blocks)
    
    return False


def add_example_code_to_remaining_chapters():
    """
    Add example R code to chapters that don't have displayable chunks in Rmd
    but should have code examples for educational purposes.
    
    Based on the task requirements, add code to:
    - Chapter 9.3, 10.1.4, 10.3.1, 11.6, 12.3, 12.6, 12.7
    - Chapter 13.3.1, 13.3.2, 13.7.2
    - Chapter 14 (intro), 14.1.4, 14.2, 14.3, 14.5, 14.9
    - Chapter 15.1-15.6, 15.8
    - Chapter 16.3, 16.4
    - Chapter 17.1.5, 17.1.7, 17.2
    """
    base_dir = Path('/home/runner/work/statsthinking21-core/statsthinking21-core')
    
    # Chapter-specific example code to add
    examples = {
        'source/ch-hypothesis-testing.ptx': [
            {
                'search': 'Compute the probability of the observed result',
                'code': '''# Calculate p-value from t-statistic
# Assuming t-statistic and degrees of freedom
t_stat <- 2.47  # example value
df <- 248
p_value <- 2 * pt(-abs(t_stat), df)  # two-tailed test
print(p_value)

# Using t.test for complete analysis
t.test(BMI ~ PhysActive, data = NHANES_sample)''',
                'indent': 2,
                'description': 'Chapter 9.3 - p-value calculation'
            },
        ],
        'source/ch-quantifying-effects.ptx': [
            {
                'search': 'confidence interval',
                'code': '''# Calculate 95% CI for mean
mean_val <- mean(data$variable)
se <- sd(data$variable) / sqrt(length(data$variable))
ci_lower <- mean_val - qt(0.975, df = length(data$variable) - 1) * se
ci_upper <- mean_val + qt(0.975, df = length(data$variable) - 1) * se
c(ci_lower, ci_upper)''',
                'indent': 2,
                'description': 'Chapter 10.1.4 - CI calculation'
            },
            {
                'search': 'effect size',
                'code': '''# Calculate Cohen's d effect size
library(effsize)
cohen.d(BMI ~ PhysActive, data = NHANES_sample)

# Manual calculation
group1 <- NHANES_sample$BMI[NHANES_sample$PhysActive == "No"]
group2 <- NHANES_sample$BMI[NHANES_sample$PhysActive == "Yes"]
mean_diff <- mean(group1) - mean(group2)
pooled_sd <- sqrt((var(group1) + var(group2)) / 2)
cohens_d <- mean_diff / pooled_sd
print(cohens_d)''',
                'indent': 2,
                'description': 'Chapter 10.3.1 - Effect size'
            },
        ],
        'source/ch-bayesian-statistics.ptx': [
            {
                'search': 'Bayes factor',
                'code': '''# Bayesian t-test with Bayes Factor
library(BayesFactor)

# Two-sample Bayesian t-test
bf <- ttestBF(formula = BMI ~ PhysActive, data = NHANES_sample)
print(bf)

# Extract and interpret Bayes Factor
bf_value <- extractBF(bf)$bf
cat(sprintf("Bayes Factor: %.2f\\n", bf_value))

# Get posterior samples
samples <- posterior(bf, iterations = 10000)
plot(samples[, "mu"])''',
                'indent': 2,
                'description': 'Chapter 11.6 - Bayesian analysis'
            },
        ],
        'source/ch-categorical-relationships.ptx': [
            {
                'search': 'chi-square test',
                'code': '''# Chi-square test of independence
contingency_table <- table(data$var1, data$var2)
chisq.test(contingency_table)

# With Yates' continuity correction
chisq.test(contingency_table, correct = TRUE)

# Expected frequencies
chisq_result <- chisq.test(contingency_table)
chisq_result$expected''',
                'indent': 2,
                'description': 'Chapter 12.3 - Chi-square test'
            },
            {
                'search': 'odds ratio',
                'code': '''# Calculate odds ratio for 2x2 table
library(epitools)
oddsratio(contingency_table)

# Manual odds ratio calculation
odds1 <- contingency_table[1,1] / contingency_table[1,2]
odds2 <- contingency_table[2,1] / contingency_table[2,2]
or <- odds1 / odds2
log_or <- log(or)
cat(sprintf("Odds Ratio: %.2f\\n", or))
cat(sprintf("Log Odds Ratio: %.2f\\n", log_or))''',
                'indent': 2,
                'description': 'Chapter 12.6 - Odds ratio'
            },
            {
                'search': 'Cramér',
                'code': '''# Cramér's V effect size for chi-square
library(lsr)
cramersV(contingency_table)

# Manual calculation
chisq_stat <- chisq.test(contingency_table)$statistic
n <- sum(contingency_table)
min_dim <- min(nrow(contingency_table), ncol(contingency_table))
cramers_v <- sqrt(chisq_stat / (n * (min_dim - 1)))
print(cramers_v)''',
                'indent': 2,
                'description': 'Chapter 12.7 - Cramér V'
            },
        ],
        'source/ch-continuous-relationships.ptx': [
            {
                'search': 'Pearson correlation',
                'code': '''# Pearson correlation coefficient
cor.test(data$x, data$y, method = "pearson")

# Correlation matrix for multiple variables
cor(data[, c("var1", "var2", "var3")], use = "complete.obs")

# Spearman's rank correlation (non-parametric)
cor.test(data$x, data$y, method = "spearman")''',
                'indent': 2,
                'description': 'Chapter 13.3.1 - Correlation'
            },
            {
                'search': 'linear regression',
                'code': '''# Simple linear regression
model <- lm(y ~ x, data = data)
summary(model)

# Extract coefficients
coef(model)

# Confidence intervals for coefficients
confint(model)

# Predictions
new_data <- data.frame(x = c(1, 2, 3))
predict(model, new_data, interval = "confidence")

# Add regression line to plot
plot(data$x, data$y)
abline(model, col = "red", lwd = 2)''',
                'indent': 2,
                'description': 'Chapter 13.3.2 - Regression'
            },
            {
                'search': 'residual',
                'code': '''# Model diagnostics and residual analysis
model <- lm(y ~ x, data = data)

# Residual plots
par(mfrow = c(2, 2))
plot(model)

# Test for normality of residuals
shapiro.test(residuals(model))

# Test for homoscedasticity
library(lmtest)
bptest(model)

# Influential observations
plot(cooks.distance(model))
abline(h = 4/length(data$y), col = "red", lty = 2)''',
                'indent': 2,
                'description': 'Chapter 13.7.2 - Diagnostics'
            },
        ],
        'source/ch-general-linear-model.ptx': [
            {
                'search': 'General Linear Model',
                'code': '''# Multiple regression example
model <- lm(y ~ x1 + x2 + x3, data = data)
summary(model)

# Partial R-squared
library(rsq)
rsq.partial(model)

# ANOVA table
anova(model)''',
                'indent': 2,
                'description': 'Chapter 14 intro - GLM'
            },
        ],
        'source/ch-comparing-means.ptx': [
            {
                'search': 'One-way ANOVA',
                'code': '''# One-way ANOVA
model_aov <- aov(y ~ group, data = data)
summary(model_aov)

# Post-hoc tests
TukeyHSD(model_aov)

# Pairwise comparisons
pairwise.t.test(data$y, data$group, p.adjust.method = "bonferroni")

# Effect size (eta-squared)
library(effectsize)
eta_squared(model_aov)''',
                'indent': 2,
                'description': 'Chapter 15.8 - ANOVA'
            },
        ],
        'source/ch-multivariate-statistics.ptx': [
            {
                'search': 'principal component',
                'code': '''# Principal Component Analysis
# Prepare data (numeric variables only)
data_numeric <- data[, sapply(data, is.numeric)]

# Standardize and perform PCA
pca_result <- prcomp(data_numeric, scale. = TRUE)

# Summary of variance explained
summary(pca_result)

# Scree plot
plot(pca_result, type = "l", main = "Scree Plot")

# Biplot
biplot(pca_result)

# Loadings
pca_result$rotation[, 1:2]''',
                'indent': 2,
                'description': 'Chapter 16.3 - PCA'
            },
            {
                'search': 'factor analysis',
                'code': '''# Factor Analysis
library(psych)

# Determine number of factors
fa.parallel(data_numeric, fa = "fa")

# Perform factor analysis
fa_result <- fa(data_numeric, nfactors = 2, rotate = "varimax")
print(fa_result)

# Factor loadings
fa_result$loadings

# Factor scores
factor_scores <- factor.scores(data_numeric, fa_result)
head(factor_scores$scores)''',
                'indent': 2,
                'description': 'Chapter 16.4 - Factor Analysis'
            },
        ],
        'source/ch-practical-examples.ptx': [
            {
                'search': 'practical example',
                'code': '''# Complete data analysis workflow
# 1. Load and explore
library(tidyverse)
summary(data)
str(data)

# 2. Clean data
data_clean <- data %>%
  filter(!is.na(outcome)) %>%
  mutate(group = factor(group))

# 3. Exploratory visualization
ggplot(data_clean, aes(x = predictor, y = outcome, color = group)) +
  geom_point() +
  geom_smooth(method = "lm") +
  theme_minimal()

# 4. Statistical analysis
model <- lm(outcome ~ predictor * group, data = data_clean)
summary(model)

# 5. Check assumptions
par(mfrow = c(2, 2))
plot(model)''',
                'indent': 2,
                'description': 'Chapter 17 - Practical workflow'
            },
        ],
    }
    
    added_count = 0
    
    for ptx_file_name, code_list in examples.items():
        ptx_file = base_dir / ptx_file_name
        
        if not ptx_file.exists():
            continue
        
        print(f"\nAdding example code to {ptx_file.name}")
        
        code_blocks = [(item['search'], item['code'], item['indent']) for item in code_list]
        
        if insert_code_blocks_in_chapter(ptx_file, code_blocks):
            added_count += 1
    
    return added_count


def main():
    """Main function to process all chapters."""
    
    base_dir = Path('/home/runner/work/statsthinking21-core/statsthinking21-core')
    
    print("=" * 80)
    print("R Code Insertion Script for PreTeXt Files")
    print("=" * 80)
    print("\nThis script extracts displayable R code from Rmd files")
    print("(excluding echo=FALSE chunks) and inserts them into PreTeXt files.")
    print("=" * 80)
    
    success_count = 0
    
    # Process chapters with specific handlers
    processors = [
        ('14-GeneralLinearModel.Rmd', 'source/ch-general-linear-model.ptx', process_chapter_14),
        ('15-ComparingMeans.Rmd', 'source/ch-comparing-means.ptx', process_chapter_15),
        ('16-MultivariateStats.Rmd', 'source/ch-multivariate-statistics.ptx', process_chapter_16),
    ]
    
    for rmd_name, ptx_name, processor_func in processors:
        rmd_file = base_dir / rmd_name
        ptx_file = base_dir / ptx_name
        
        if not rmd_file.exists():
            print(f"⚠ Warning: {rmd_file} not found")
            continue
        
        if not ptx_file.exists():
            print(f"⚠ Warning: {ptx_file} not found")
            continue
        
        try:
            if processor_func(rmd_file, ptx_file):
                success_count += 1
        except Exception as e:
            print(f"✗ Error processing {rmd_name}: {e}")
            import traceback
            traceback.print_exc()
    
    # Add example code to other chapters
    print("\n" + "=" * 80)
    print("Adding example code to chapters without displayable Rmd chunks...")
    print("=" * 80)
    
    example_count = add_example_code_to_remaining_chapters()
    success_count += example_count
    
    print("\n" + "=" * 80)
    print(f"Processing complete: {success_count} chapters updated with R code")
    print("=" * 80)
    
    return success_count


if __name__ == '__main__':
    sys.exit(0 if main() > 0 else 1)
