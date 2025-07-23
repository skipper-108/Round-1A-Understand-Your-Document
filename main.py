
"""
PDF Outline Extractor - Main Entry Point

"""

import json
import sys
from pathlib import Path
from utils import extract_outline


def main():
    """
    Main entry point for PDF outline extraction.
    Processes all PDF files in /app/input and writes JSON output to /app/output.
    """
    # Define input and output directories (works both in Docker and locally)
    input_dir = Path("/app/input") if Path("/app/input").exists() else Path("input")
    output_dir = Path("/app/output") if Path("/app/output").exists() else Path("output")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files from input directory
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process.")
    
    # Process each PDF file
    for pdf_file in pdf_files:
        try:
            print(f"Processing: {pdf_file.name}")
            
            # Extract outline from PDF
            result = extract_outline(pdf_file)
            
            # Create output filename
            output_filename = f"{pdf_file.stem}.json"
            output_path = output_dir / output_filename
            
            # Write JSON output with UTF-8 encoding
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Saved outline to: {output_filename}")
            
        except Exception as e:
            print(f"✗ Error processing {pdf_file.name}: {e}")
            # Write error output
            error_result = {
                "title": f"Error processing {pdf_file.name}",
                "outline": [],
                "error": str(e)
            }
            output_filename = f"{pdf_file.stem}.json"
            output_path = output_dir / output_filename
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(error_result, f, indent=2, ensure_ascii=False)
    
    print("PDF outline extraction completed.")


if __name__ == "__main__":
    main() 
