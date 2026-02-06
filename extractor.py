from dotenv import load_dotenv
load_dotenv()

import pdfplumber
from openai import OpenAI
import json
import os
import re
from typing import Dict, Any, Optional

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

def read_document(file_path: str) -> str:
    """Read document content from PDF or text file"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if file_path.endswith(".pdf"):
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text() or ""
                    text += f"--- Page {page_num} ---\n{page_text}\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    else:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError(f"Could not decode file with any encoding: {file_path}")

def extract_json(text: str) -> Dict[str, Any]:
    """Safely extract JSON from Llama response with multiple fallback strategies"""
    if not text:
        raise ValueError("Empty response from model")
    
    # Strategy 1: Look for JSON pattern
    json_pattern = r'```json\s*(\{.*?\})\s*```|\{.*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)
    
    for match in matches:
        if isinstance(match, tuple):  # For capture groups
            match = match[0] if match[0] else match[1]
        
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue
    
    # Strategy 2: Try to find any JSON structure
    try:
        # Find the first { and last } and try to parse
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            candidate = text[start:end+1]
            return json.loads(candidate)
    except json.JSONDecodeError:
        pass
    
    # Strategy 3: Clean and retry
    try:
        # Remove any markdown code blocks
        cleaned = re.sub(r'```[a-z]*\n?', '', text)
        cleaned = re.sub(r'\n```', '', cleaned)
        
        # Remove explanatory text before/after JSON
        lines = cleaned.strip().split('\n')
        json_lines = []
        in_json = False
        
        for line in lines:
            if '{' in line or '[' in line:
                in_json = True
            if in_json:
                json_lines.append(line)
            if '}' in line or ']' in line:
                in_json = False
        
        json_text = '\n'.join(json_lines)
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse JSON from response. Error: {e}\nResponse: {text[:500]}")

def extract_fields_from_text(text: str) -> Dict[str, Any]:
    """Extract structured fields from FNOL text using LLM"""
    
    # Clean and preprocess text
    text = text.strip()
    
    prompt = f"""You are an expert insurance claims processor extracting structured data from First Notice of Loss (FNOL) documents.

GUIDELINES:
1. Extract ONLY ACTUAL VALUES filled in the document, not field labels or template text
2. For missing or unclear fields, return empty string "" (not null, not "N/A")
3. Clean and normalize extracted values:
   - Dates: Use YYYY-MM-DD format when possible
   - Numbers: Extract digits only (e.g., "8500" not "$8,500" or "ESTIMATE AMOUNT")
   - Names: Proper case (e.g., "John Smith")
   - Phone: Standard format (e.g., "+1-555-123-4567")
4. Be lenient with formatting but strict with data quality
5. Return ONLY valid JSON, no additional text

REQUIRED FIELDS TO EXTRACT:
1. Policy Number: Alphanumeric identifier (e.g., "AUTO-PL-45879231")
2. Policyholder Name: Full legal name of insured
3. Effective Dates: Policy period in "YYYY-MM-DD to YYYY-MM-DD" format
4. Date: Incident date in YYYY-MM-DD format
5. Time: 24-hour or AM/PM format
6. Location: Full address with city, state, zip
7. Description: Detailed incident description
8. Claimant: Name if different from policyholder
9. Third Parties: Names/details of other involved parties
10. Contact Details: Dict with "phone" and "email" keys
11. Asset Type: "Vehicle", "Property", "Home", etc.
12. Asset ID: VIN, license plate, property ID
13. Estimated Damage: Numeric value only (e.g., 18500)
14. Claim Type: "Auto Collision", "Property Damage", "Injury", "Theft", etc.
15. Attachments: List of documents/photos mentioned
16. Initial Estimate: Numeric value for initial assessment

CRITICAL: If a field contains placeholder text like "ENTER NAME HERE", "POLICY NUMBER", or form field labels without actual data, return empty string "".

DOCUMENT TEXT:
{text[:10000]}  # Limit to first 10k chars to avoid token limits

IMPORTANT: Return EXACTLY this JSON structure with no other text:
{{
  "Policy Number": "value or empty string",
  "Policyholder Name": "value or empty string",
  "Effective Dates": "value or empty string",
  "Date": "value or empty string",
  "Time": "value or empty string",
  "Location": "value or empty string",
  "Description": "value or empty string",
  "Claimant": "value or empty string",
  "Third Parties": "value or empty string",
  "Contact Details": {{"phone": "value or empty string", "email": "value or empty string"}},
  "Asset Type": "value or empty string",
  "Asset ID": "value or empty string",
  "Estimated Damage": "value or empty string",
  "Claim Type": "value or empty string",
  "Attachments": "value or empty string",
  "Initial Estimate": "value or empty string"
}}"""
    
    try:
        response = client.chat.completions.create(
            model="Meta-Llama-3.1-8B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # Slightly higher for better extraction
            max_tokens=2000,
        )
        
        raw_output = response.choices[0].message.content
        extracted_data = extract_json(raw_output)
        
        # Post-process extracted data
        return post_process_extraction(extracted_data)
        
    except Exception as e:
        raise Exception(f"Error in LLM extraction: {str(e)}")

def post_process_extraction(data: Dict[str, Any]) -> Dict[str, Any]:
    """Post-process and validate extracted data"""
    
    # Ensure all required fields exist
    required_fields = [
        "Policy Number", "Policyholder Name", "Effective Dates",
        "Date", "Time", "Location", "Description",
        "Claimant", "Third Parties", "Contact Details",
        "Asset Type", "Asset ID", "Estimated Damage",
        "Claim Type", "Attachments", "Initial Estimate"
    ]
    
    for field in required_fields:
        if field not in data:
            data[field] = ""
    
    # Clean string fields
    for key, value in data.items():
        if isinstance(value, str):
            # Remove excessive whitespace
            data[key] = ' '.join(value.strip().split())
            
            # Handle common placeholder patterns
            placeholder_patterns = [
                r'^enter\s+.+\s+here$',
                r'^\[.+\]$',
                r'^click\s+to\s+enter',
                r'^select\s+.+',
                r'^type\s+.+',
                r'^please\s+enter',
                r'^n/a$',
                r'^not\s+applicable$',
                r'^\s*$'
            ]
            
            for pattern in placeholder_patterns:
                if re.match(pattern, value.lower()):
                    data[key] = ""
                    break
    
    # Ensure Contact Details is proper dict
    if "Contact Details" in data:
        if not isinstance(data["Contact Details"], dict):
            data["Contact Details"] = {"phone": "", "email": ""}
        else:
            # Ensure both keys exist
            if "phone" not in data["Contact Details"]:
                data["Contact Details"]["phone"] = ""
            if "email" not in data["Contact Details"]:
                data["Contact Details"]["email"] = ""
    
    # Normalize date formats if possible
    date_fields = ["Date", "Effective Dates"]
    for field in date_fields:
        if field in data and data[field]:
            # Try to normalize date formats
            date_str = data[field]
            # Add date normalization logic here if needed
    
    return data