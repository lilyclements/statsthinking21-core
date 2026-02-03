# Data loading and preprocessing functions
# This file contains functions for loading and cleaning datasets used in the book

# Load NHANES package at the top
library(NHANES)

#' Load and clean NHANES data
#'
#' This function loads the NHANES dataset and performs standard cleaning:
#' - Removes duplicated IDs
#' - Adds isChild indicator variable
#' - Creates adult-only subset with non-missing Height values
#'
#' @return A list containing:
#'   - NHANES: Full cleaned NHANES dataset
#'   - NHANES_adult: Adult subset (Age >= 18) with non-missing Height
load_nhanes <- function() {
  # Load and remove duplicated IDs within the NHANES dataset
  NHANES_clean <- NHANES %>% 
    dplyr::distinct(ID, .keep_all = TRUE)
  
  # Add child indicator
  NHANES_clean$isChild <- NHANES_clean$Age < 18
  
  # Create adult subset
  NHANES_adult <- NHANES_clean %>%
    drop_na(Height) %>%
    subset(subset = Age >= 18)
  
  return(list(
    NHANES = NHANES_clean,
    NHANES_adult = NHANES_adult
  ))
}
