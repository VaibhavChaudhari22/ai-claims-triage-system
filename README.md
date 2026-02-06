# FNOL Agent

A FastAPI-based agent for automated FNOL (First Notice of Loss) document processing using OpenAI's GPT-4o-mini model.

## Features

- **PDF & Text File Support**: Extract text from PDF and text documents
- **Intelligent Field Extraction**: Uses GPT-4o-mini to extract insurance claim information
- **RESTful API**: FastAPI-based endpoints for easy integration
- **CORS Enabled**: Ready for cross-origin requests

## Project Structure

```
.
├── main.py           # FastAPI application and server initialization
├── router.py         # API endpoints for document extraction
├── extractor.py      # Document reading and field extraction logic
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set the `OPENAI_API_KEY` environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Endpoints

- **POST /extract**: Extract FNOL fields from a document
  - **Request**: Multipart form data with file upload
  - **Response**: JSON with extracted fields
  
- **GET /health**: Health check endpoint
- **GET /**: Root endpoint

### Example Request

```bash
curl -X POST "http://localhost:8000/extract" \
  -F "file=@document.pdf"
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `openai` - OpenAI API client
- `pdfplumber` - PDF text extraction
- `python-dotenv` - Environment variable management
