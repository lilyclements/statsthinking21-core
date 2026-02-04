#!/usr/bin/env python3
"""
Script to extract R code chunks from Rmd files and add them to PreTeXt files.
This adds <program language="r"> blocks to PreTeXt files where appropriate.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict
import xml.etree.ElementTree as ET


def extract_r_code_chunks(rmd_file: Path) -> List[Tuple[str, str, int]]:
    """
    Extract R code chunks from an Rmd file.
    Returns list of tuples: (chunk_name, chunk_code, line_number)
    """
    chunks = []
    
    with open(rmd_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match R code chunks: ```{r ...} ... ```
    # Captures the chunk header and the code
    pattern = r'```\{r\s+([^}]*)\}(.*?)```'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        chunk_header = match.group(1).strip()
        chunk_code = match.group(2).strip()
        
        # Extract chunk name (first word in header)
        chunk_name = chunk_header.split(',')[0].strip() if chunk_header else 'unnamed'
        
        # Skip empty chunks
        if not chunk_code:
            continue
            
        # Find line number
        line_num = content[:match.start()].count('\n') + 1
        
        chunks.append((chunk_name, chunk_code, line_num))
    
    return chunks


def format_r_code_for_pretext(code: str, indent: int = 6) -> str:
    """
    Format R code for insertion into PreTeXt.
    Returns formatted <program> block.
    """
    base_indent = ' ' * indent
    inner_indent = ' ' * (indent + 2)
    
    result = f'{base_indent}<program language="r">\n'
    result += f'{inner_indent}<input>\n'
    
    # Add code lines with proper indentation
    for line in code.split('\n'):
        result += f'{inner_indent}{line}\n'
    
    result += f'{inner_indent}</input>\n'
    result += f'{base_indent}</program>\n'
    
    return result


def find_insertion_points(ptx_file: Path, rmd_file: Path) -> Dict[str, List[int]]:
    """
    Find appropriate insertion points in PreTeXt file for R code chunks.
    This is a heuristic approach based on context matching.
    """
    insertion_points = {}
    
    with open(ptx_file, 'r', encoding='utf-8') as f:
        ptx_lines = f.readlines()
    
    with open(rmd_file, 'r', encoding='utf-8') as f:
        rmd_content = f.read()
    
    # For now, return empty dict - we'll manually identify sections
    # In a production system, this would use more sophisticated matching
    return insertion_points


def add_r_code_to_section(ptx_content: str, chunk_name: str, r_code: str, 
                          after_text: str, indent: int = 6) -> str:
    """
    Add R code block after a specific text marker in PreTeXt content.
    """
    formatted_code = format_r_code_for_pretext(r_code, indent)
    
    # Find the position to insert
    pos = ptx_content.find(after_text)
    if pos == -1:
        print(f"Warning: Could not find marker text for chunk '{chunk_name}'")
        return ptx_content
    
    # Find the end of the line
    end_pos = ptx_content.find('\n', pos)
    if end_pos == -1:
        end_pos = len(ptx_content)
    
    # Insert the code block after the marker
    result = ptx_content[:end_pos+1] + '\n' + formatted_code + ptx_content[end_pos+1:]
    
    return result


def main():
    """Main function to process files."""
    
    # Map of Rmd files to PreTeXt files
    file_mapping = {
        '09-HypothesisTesting.Rmd': 'source/ch-hypothesis-testing.ptx',
        '10-ConfIntEffectSize.Rmd': 'source/ch-quantifying-effects.ptx',
        '11-BayesianStatistics.Rmd': 'source/ch-bayesian-statistics.ptx',
        '12-CategoricalRelationships.Rmd': 'source/ch-categorical-relationships.ptx',
        '13-ContinuousRelationships.Rmd': 'source/ch-continuous-relationships.ptx',
        '14-GeneralLinearModel.Rmd': 'source/ch-general-linear-model.ptx',
        '15-ComparingMeans.Rmd': 'source/ch-comparing-means.ptx',
        '16-MultivariateStats.Rmd': 'source/ch-multivariate-statistics.ptx',
        '17-PracticalExamples.Rmd': 'source/ch-practical-examples.ptx',
    }
    
    base_dir = Path('/home/runner/work/statsthinking21-core/statsthinking21-core')
    
    # Process each file
    for rmd_name, ptx_name in file_mapping.items():
        rmd_file = base_dir / rmd_name
        ptx_file = base_dir / ptx_name
        
        if not rmd_file.exists():
            print(f"Warning: {rmd_file} not found")
            continue
        
        if not ptx_file.exists():
            print(f"Warning: {ptx_file} not found")
            continue
        
        print(f"\nProcessing {rmd_name} -> {ptx_name}")
        
        # Extract R code chunks
        chunks = extract_r_code_chunks(rmd_file)
        print(f"Found {len(chunks)} R code chunks")
        
        # Display chunks for review
        for name, code, line_num in chunks[:5]:  # Show first 5
            print(f"  - Chunk '{name}' at line {line_num} ({len(code)} chars)")


if __name__ == '__main__':
    main()
