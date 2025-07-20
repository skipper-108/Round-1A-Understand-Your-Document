# PDF Outline Extractor - Windows Setup Guide

## 📋 Overview

This guide provides step-by-step instructions to set up and run the PDF Outline Extractor application on Windows. The application extracts structured outlines (Title, H1, H2, H3 with page numbers) from PDF files and outputs valid JSON files.

## 🎯 Features

- ✅ Extract document titles and headings from PDF files
- ✅ Generate structured JSON output with page numbers
- ✅ Support for multiple PDF formats
- ✅ Robust text extraction with proper spacing
- ✅ Docker support for containerized deployment
- ✅ Cross-platform compatibility

## 📋 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10 (64-bit) or later
- **Python**: Python 3.8 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 500 MB free space
- **Processor**: Intel/AMD 64-bit processor

### Recommended Requirements
- **Operating System**: Windows 11 (64-bit)
- **Python**: Python 3.10 or higher
- **RAM**: 8 GB or more
- **Storage**: 1 GB free space
- **Processor**: Multi-core processor

## 🛠️ Installation Steps

### Step 1: Install Python

1. **Download Python**:
   - Go to [python.org](https://www.python.org/downloads/)
   - Download Python 3.10 or higher for Windows
   - Choose the "Windows installer (64-bit)" version

2. **Install Python**:
   - Run the downloaded installer
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Choose "Install Now" (recommended) or "Customize installation"
   - Wait for installation to complete

3. **Verify Installation**:
   - Open Command Prompt (cmd) or PowerShell
   - Run: `python --version`
   - You should see: `Python 3.x.x`

### Step 2: Install Git (Optional but Recommended)

1. **Download Git**:
   - Go to [git-scm.com](https://git-scm.com/download/win)
   - Download Git for Windows

2. **Install Git**:
   - Run the installer with default settings
   - This allows you to clone the repository easily

### Step 3: Download/Clone the Project

#### Option A: Using Git (Recommended)
```bash
# Open Command Prompt or PowerShell
git clone https://github.com/your-repo/pdf_outline_extractor.git
cd pdf_outline_extractor
```

#### Option B: Manual Download
1. Download the project ZIP file
2. Extract to a folder (e.g., `C:\pdf_outline_extractor`)
3. Open Command Prompt and navigate to the folder:
   ```bash
   cd C:\pdf_outline_extractor
   ```

### Step 4: Set Up Virtual Environment

1. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate Virtual Environment**:
   ```bash
   # On Windows Command Prompt
   venv\Scripts\activate

   # On Windows PowerShell
   .\venv\Scripts\Activate.ps1
   ```

3. **Verify Activation**:
   - You should see `(venv)` at the beginning of your command prompt

### Step 5: Install Dependencies

```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### Step 6: Verify Installation

```bash
# Test Python imports
python -c "import pdfminer.high_level; print('PDFMiner installed successfully')"
```

## 🚀 Running the Application

### Method 1: Local Python Execution

1. **Prepare PDF Files**:
   - Place your PDF files in the `input/` directory
   - Supported formats: `.pdf`

2. **Run the Application**:
   ```bash
   # Make sure virtual environment is activated
   python main.py
   ```

3. **Check Results**:
   - Output JSON files will be created in the `output/` directory
   - Each PDF will have a corresponding JSON file

### Method 2: Docker Execution (Recommended for Production)

#### Prerequisites for Docker
1. **Install Docker Desktop**:
   - Download from [docker.com](https://www.docker.com/products/docker-desktop)
   - Install Docker Desktop for Windows
   - Restart your computer after installation

2. **Verify Docker Installation**:
   ```bash
   docker --version
   docker-compose --version
   ```

#### Running with Docker

1. **Build Docker Image**:
   ```bash
   docker build -t pdf-outline-extractor .
   ```

2. **Run Container**:
   ```bash
   # Mount input and output directories
   docker run -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" pdf-outline-extractor
   ```

3. **Alternative Docker Run Command** (Windows CMD):
   ```cmd
   docker run -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" pdf-outline-extractor
   ```

## 📁 Project Structure

```
pdf_outline_extractor/
├── input/                  # Place PDF files here
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
├── output/                 # Generated JSON files
│   ├── document1.json
│   ├── document2.json
│   └── ...
├── main.py                 # Main application entry point
├── utils.py                # Core extraction logic
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── README.md              # Project documentation
└── WINDOWS_SETUP.md       # This file
```

## 📊 Output Format

The application generates JSON files with the following structure:

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Heading Text",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "Subheading Text",
      "page": 2
    }
  ]
}
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Python Not Found
**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
- Ensure Python is added to PATH during installation
- Restart Command Prompt after Python installation
- Try using `py` instead of `python` on Windows

#### 2. Virtual Environment Issues
**Error**: `venv\Scripts\activate` not working

**Solution**:
```bash
# Try PowerShell instead of CMD
powershell
.\venv\Scripts\Activate.ps1

# Or use full path
C:\path\to\project\venv\Scripts\activate.bat
```

#### 3. Permission Issues
**Error**: Permission denied when creating virtual environment

**Solution**:
- Run Command Prompt as Administrator
- Or use a different directory with write permissions

#### 4. PDFMiner Installation Issues
**Error**: Failed to install pdfminer.six

**Solution**:
```bash
# Update pip first
python -m pip install --upgrade pip

# Install with specific version
pip install pdfminer.six==20221105
```

#### 5. Docker Issues
**Error**: Docker not running

**Solution**:
- Start Docker Desktop application
- Wait for Docker to fully initialize
- Check Docker status: `docker info`

#### 6. File Path Issues
**Error**: File not found or path issues

**Solution**:
- Use absolute paths on Windows
- Ensure proper directory structure
- Check file permissions

## 🧪 Testing the Installation

### Test Script
Create a test script to verify everything works:

```python
# test_setup.py
import sys
import pdfminer.high_level
from pathlib import Path

def test_setup():
    print("Testing PDF Outline Extractor Setup...")
    print(f"Python version: {sys.version}")
    print(f"PDFMiner version: {pdfminer.__version__}")
    print("✅ Setup is working correctly!")

if __name__ == "__main__":
    test_setup()
```

Run the test:
```bash
python test_setup.py
```

### Sample Test
1. Place a sample PDF in the `input/` directory
2. Run the application
3. Check the generated JSON in `output/` directory
4. Verify the structure and content

## 📝 Usage Examples

### Basic Usage
```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Place PDF files in input directory
# 3. Run the application
python main.py

# 4. Check results
dir output\
```

### Batch Processing
```bash
# Process multiple PDFs at once
# Just place all PDFs in input/ directory and run
python main.py
```

### Docker Usage
```bash
# Build and run in one command
docker build -t pdf-extractor . && docker run -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" pdf-extractor
```

## 🔒 Security Considerations

- Keep your virtual environment isolated
- Don't commit sensitive PDF files to version control
- Use Docker for production deployments
- Regularly update dependencies

## 📞 Support

### Getting Help
1. Check the troubleshooting section above
2. Review the main README.md file
3. Check Python and Docker documentation
4. Verify all requirements are met

### Common Commands Reference
```bash
# Python version
python --version

# Pip version
pip --version

# List installed packages
pip list

# Update pip
python -m pip install --upgrade pip

# Check virtual environment
where python

# Docker commands
docker --version
docker images
docker ps
```

## 🎯 Performance Tips

1. **Use SSD storage** for better I/O performance
2. **Close other applications** when processing large PDFs
3. **Use Docker** for consistent environment
4. **Monitor memory usage** for large documents
5. **Batch process** multiple PDFs together

## 📋 Checklist

- [ ] Python 3.8+ installed and in PATH
- [ ] Git installed (optional)
- [ ] Project downloaded/cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Test script runs successfully
- [ ] Sample PDF processed correctly
- [ ] Docker installed (optional)
- [ ] Docker image built (optional)

## 🚀 Next Steps

After successful setup:
1. Process your PDF files
2. Review the generated JSON output
3. Integrate with your applications
4. Deploy to production if needed
5. Customize extraction logic if required

---

**Note**: This application is designed for the Adobe India Hackathon and follows all specified constraints including max 50 pages, 10 seconds per PDF, offline operation, CPU-only AMD64 support, and ≤200MB dependencies. 