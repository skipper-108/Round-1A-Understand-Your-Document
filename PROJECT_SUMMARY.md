# PDF Outline Extractor - Project Summary

## Adobe India Hackathon Round 1A

### 🎯 Project Overview

A fully functional, Dockerized Python application that extracts structured outlines from PDF files using advanced layout analysis and heading heuristics. The application processes PDF files and outputs clean JSON with document titles and hierarchical outlines.

#### 📁 Folder Structure

```
pdf_outline_extractor/
├── Dockerfile
├── main.py
├── utils.py
├── requirements.txt
├── README.md
├── input/
└── output/
```

#### 🔧 Functionality

- Accepts all `.pdf` files from `/app/input` directory
- Extracts document title (first detected H1 or topmost heading)
- Extracts structured outline of headings (H1, H2, H3)
- Provides page numbers for each heading
- Writes `{filename}.json` files to `/app/output`
- Follows exact JSON format specification

### 🏗️ Technical Implementation

#### Core Technology Stack

- **Python 3.10**: Base runtime environment
- **pdfminer.six==20221105**: Advanced PDF layout parsing
- **Docker**: Containerization with AMD64 support

#### Heading Detection Algorithm

The application uses sophisticated heuristics based on:

1. **Font Analysis**:

   - Font size ratios (normalized against document maximum)
   - Bold/italic style detection from font names
   - Relative font size comparisons

2. **Layout Analysis**:

   - Position on page (top/middle/bottom)
   - Text positioning and spacing
   - Page layout structure

3. **Content Patterns**:

   - Numbered lists (1., 2., 3., etc.)
   - Chapter markers (Chapter, Section, Part)
   - Bullet points (•, ●, -, ○)
   - Text length and formatting

4. **Hierarchical Classification**:
   - **H1**: Large font (>80% max), bold, top position, or specific patterns
   - **H2**: Medium-large font (>50%), numbered patterns, or bold text
   - **H3**: Medium font (>30%), descriptive text, or bullet patterns

### 📊 Output Format

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

### 🚀 Docker Deployment

#### Build Command

```bash
docker build --platform linux/amd64 -t outline-extractor .
```

#### Run Command

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none outline-extractor
```

### ⚡ Performance Constraints

- **Max PDF size**: 50 pages (enforced)
- **Max execution time**: 10 seconds per PDF (enforced)
- **Offline operation**: No internet required
- **CPU only**: AMD64 architecture support
- **Size limit**: Model + dependencies ≤ 200MB
- **Generic logic**: No hardcoded values or file-specific rules

### 🔍 Key Features

#### Robust Error Handling

- Graceful handling of corrupted PDFs
- Timeout protection (10-second limit)
- Page limit enforcement (50 pages)
- UTF-8 encoding support
- Comprehensive error reporting

#### Advanced Layout Analysis

- Precise text positioning extraction
- Font information analysis
- Page structure understanding
- Multi-page document support

#### Intelligent Heading Detection

- Multi-factor classification algorithm
- Relative size normalization
- Pattern recognition
- Position-aware analysis

### 🧪 Testing & Validation

#### Test Results

- Application structure test passed
- Dependency installation successful
- PDF processing pipeline working
- JSON output format correct
- Docker configuration valid
- Error handling functional

#### Local Testing

```bash
# Test application structure
python3 test_local.py

# Process PDFs
python3 main.py

# Check results
ls -la output/
```

### 📚 Documentation

- **README.md**: Comprehensive usage guide with Docker instructions
- **PROJECT_SUMMARY.md**: This summary document
- **Inline code documentation**: Detailed function documentation
- **Type hints**: Full type annotation support

1.  Complete Functionality\*\*: All requirements implemented
2.  Technical Excellence\*\*: Advanced PDF parsing with layout analysis
3.  Docker Ready\*\*: Containerized for easy deployment
4.  Performance Optimized\*\*: Meets all constraint requirements
5.  Well Documented\*\*: Comprehensive guides and examples
6.  Error Resilient\*\*: Robust error handling and validation
7.  Generic Logic\*\*: Works with any PDF structure

### 🚀 Quick Start

```bash
# Build Docker image
docker build --platform linux/amd64 -t outline-extractor .

# Add PDF files to input directory
cp your_document.pdf input/

# Run the application
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none outline-extractor

# Check results
ls -la output/
cat output/your_document.json
```

### 📈 Technical Highlights

- **Advanced PDF Parsing**: Uses pdfminer.six for precise layout analysis
- **Intelligent Heuristics**: Multi-factor heading classification
- **Performance Optimized**: Efficient processing within constraints
- **Generic Design**: Works with various PDF formats and structures
- **Production Ready**: Robust error handling and validation
- **Docker Native**: Optimized containerization for deployment

---
