# Word-to-PDF Conversion Web App

This web application converts `.docx` files into `.pdf` format. It includes:
- A user-friendly Streamlit interface.
- A FastAPI backend for processing.
- Basic authentication for secure access.
- Docker support for containerization.

## Features
- Upload `.docx` files and convert them to `.pdf`.
- View conversion status and download the resulting file.
- Secure with username and password.
- Containerized for easy deployment.

## Requirements
- Python 3.9+ (3.12.3 used here)
- Streamlit
- FastAPI
- Docker

## Usage

### 1. Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/himanshuuu7/word-to-pdf.git
   cd word-to-pdf/

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the bash script:
   ```bash
   ./run.sh
