# PDF Outline Extractor

A Dockerized Python application that extracts structured outlines from PDF files using layout analysis and heading heuristics.

## Approach

This application uses **pdfminer.six** for advanced PDF layout parsing to extract structured outlines. The approach involves:

1. **Layout Analysis**: Extract text elements with precise positioning, font information, and page layout
2. **Heading Detection**: Use multiple heuristics based on:
   - Font size and style (bold/italic)
   - Position in layout (top/middle/bottom of page)
   - Text patterns (numbered lists, chapter markers)
   - Relative font size ratios
3. **Title Extraction**: Identify document title from first H1 heading or topmost significant text
4. **Structured Output**: Generate clean JSON with title and hierarchical outline

## Dependencies

- **pdfminer.six==20221105**: Advanced PDF text extraction with layout analysis
- **Python 3.10**: Base runtime environment

## Docker Build and Run

### Build the Docker image:
```bash
docker build --platform linux/amd64 -t outline-extractor .
```

### Run the container:
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none outline-extractor
```

## Usage

1. Place your PDF files in the `input/` directory
2. Run the Docker container
3. Check the `output/` directory for generated JSON files

## Output Format

Each PDF generates a JSON file with the following structure:

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

## Constraints

- Maximum PDF size: 50 pages
- Maximum execution time: 10 seconds per PDF
- Works offline (no internet required)
- CPU only (AMD64 architecture)
- Model + dependencies size: ≤ 200MB
- Generic, reusable logic with no manual rules

## Features

- **Robust Heading Detection**: Uses font size, style, position, and text patterns
- **Error Handling**: Graceful handling of corrupted or invalid PDFs
- **UTF-8 Encoding**: Proper handling of international characters
- **Performance Optimized**: Efficient processing within time constraints
- **Generic Logic**: Works with various PDF formats and structures 