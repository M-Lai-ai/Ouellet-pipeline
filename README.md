# Ouellet Pipeline

[![Description de l'image](https://raw.githubusercontent.com/M-Lai-ai/logo/refs/heads/main/favicon.ico)](https://votre-lien-cible.com)


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Logging and Reports](#logging-and-reports)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

The **Ouellet Pipeline** is an automated system designed to:

1. **Crawl a specified website** to discover and download PDF and DOC/DOCX files.
2. **Process the downloaded files** by extracting text, performing OCR on scanned PDFs, restructuring content using OpenAI's GPT-4, and saving the processed content as separate `.txt` files per page.

This pipeline is ideal for organizations like **Ouellet Canada** looking to automate the collection and processing of documents for analysis, archiving, or further content management.

## Features

- **Web Crawling**:
  - Recursive crawling up to a specified depth.
  - Downloading of PDF and DOC/DOCX files.
  - Handling of multiple content types with appropriate directory structuring.
  
- **Content Processing**:
  - Extraction of text from PDFs (including OCR for scanned documents).
  - Extraction of text from DOC/DOCX files.
  - Restructuring of extracted content into Markdown format using GPT-4.
  - Generation of individual `.txt` files for each page of a PDF.
  
- **Logging and Reporting**:
  - Comprehensive logging of crawling and processing activities.
  - Generation of detailed reports and summaries post-execution.
  
- **Configuration**:
  - Easy setup using environment variables for sensitive data like API keys.
  
## Architecture

![Architecture Diagram](https://via.placeholder.com/800x400.png?text=Architecture+Diagram)

1. **WebCrawler (`crawler.py`)**:
   - Initiates crawling from a starting URL.
   - Discovers and downloads PDF and DOC/DOCX files.
   - Saves files in organized directories (`PDF`, `Doc`, etc.).
   
2. **ContentProcessor (`content_processor.py`)**:
   - Processes downloaded files.
   - Extracts text content using PyPDF2 and OCR (pytesseract) for PDFs.
   - Extracts text from DOC/DOCX using `python-docx`.
   - Sends content to OpenAI GPT-4 for restructuring into Markdown.
   - Saves processed content as separate `.txt` files per PDF page.
   
3. **Master Pipeline (`master_pipeline.py`)**:
   - Orchestrates the execution of `WebCrawler` and `ContentProcessor` sequentially.

## Prerequisites

- **Python 3.7 or higher**
- **Tesseract OCR**:
  - Required for performing OCR on scanned PDFs.
- **OpenAI API Key**:
  - Required for accessing GPT-4 for content restructuring.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/M-Lai-ai/Ouellet-pipeline.git
   cd Ouellet-pipeline
   ```

2. **Set Up a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   Ensure you have `pip` updated:

   ```bash
   pip install --upgrade pip
   ```

   Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**:

   - **Windows**:
     - Download the installer from [Tesseract at UB Mannheim](https://github.com/tesseract-ocr/tesseract/wiki/Downloads).
     - Run the installer and follow the setup instructions.
     - Add the Tesseract installation directory (e.g., `C:\Program Files\Tesseract-OCR`) to your system `PATH`.

   - **macOS**:
     ```bash
     brew install tesseract
     ```

   - **Linux**:
     ```bash
     sudo apt-get install tesseract-ocr
     ```

   - **Install Additional Language Packs** (if needed):
     ```bash
     # Exemple pour le français
     sudo apt-get install tesseract-ocr-fra
     ```

## Configuration

1. **Create a `.env` File**:

   At the root of your project directory, create a `.env` file to store environment variables securely.

   ```bash
   touch .env
   ```

2. **Add Your OpenAI API Key**:

   Open the `.env` file in a text editor and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   **Note**: Replace `your_openai_api_key_here` with your actual OpenAI API key. **Do not share or commit this file to version control.**

## Usage

Run the master pipeline script to start the crawling and processing workflow.

```bash
python master_pipeline.py
```

### Script Breakdown

1. **`crawler.py`**:
   - Crawls the specified website.
   - Downloads PDF and DOC/DOCX files.
   - Saves files in respective directories (`PDF`, `Doc`, etc.).

2. **`content_processor.py`**:
   - Processes the downloaded files.
   - Extracts text and performs OCR if necessary.
   - Sends content to GPT-4 for restructuring.
   - Saves processed content as individual `.txt` files per PDF page.

3. **`master_pipeline.py`**:
   - Coordinates the execution of both `WebCrawler` and `ContentProcessor`.
   - Ensures sequential processing and handles any critical errors.

## Directory Structure

```
/Ouellet-pipeline
│
├── crawler.py              # WebCrawler class
├── content_processor.py    # ContentProcessor class
├── master_pipeline.py      # Master script to run the pipeline
├── .env                    # Environment variables (API keys)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── /crawler_output_YYYYMMDD_HHMMSS
    ├── /PDF                # Downloaded PDF files
    ├── /Doc                # Downloaded DOC/DOCX files
    ├── /content            # Processed content (.txt files)
    ├── /Image              # Downloaded image files
    ├── /logs               # Logs generated by WebCrawler
    ├── crawler_report.txt  # Detailed crawl report
    └── summary.txt         # Summary of the crawling process
```

**Note**: Each execution of the crawler generates a new `crawler_output_YYYYMMDD_HHMMSS` directory based on the timestamp.

## Logging and Reports

- **Logs**:
  - **Crawler Logs**: Located at `crawler_output_<timestamp>/logs/crawler.log`
  - **Pipeline Logs**: Located at the root as `pipeline.log`

- **Reports**:
  - **Detailed Report**: `crawler_output_<timestamp>/crawler_report.txt`
  - **Summary**: `crawler_output_<timestamp>/summary.txt`

These logs provide insights into the crawling and processing activities, including any errors encountered.

## Troubleshooting

- **Tesseract OCR Not Found**:
  - Ensure Tesseract is installed and added to your system `PATH`.
  - Verify installation by running `tesseract --version` in your terminal.

- **OpenAI API Errors**:
  - Check your API key in the `.env` file.
  - Ensure your API key has sufficient permissions and quota.
  - Review the error messages in `pipeline.log` for specifics.

- **Dependency Issues**:
  - Ensure all dependencies are installed correctly via `requirements.txt`.
  - Consider recreating your virtual environment if issues persist.

- **Permission Errors**:
  - Ensure you have the necessary permissions to create and write to directories and files in the project path.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add some feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open a Pull Request**

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

**M-LAI** – [m.lai@example.com](mailto:m.lai@example.com)

Project Link: [https://github.com/M-Lai-ai/Ouellet-pipeline.git](https://github.com/M-Lai-ai/Ouellet-pipeline.git)
