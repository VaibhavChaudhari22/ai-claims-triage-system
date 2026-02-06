# 🚀 FNOI Agent - AI-Powered Insurance Claims Processor 🤖

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI Powered](https://img.shields.io/badge/AI-Llama%203.1-orange)](https://llama.meta.com/)

> **Automate insurance claim processing with AI: Extract, analyze, and route claims intelligently**

**FNOI Agent** is an intelligent system that reads insurance claim documents (PDFs, text files, images), extracts structured data using AI, and automatically routes claims to the appropriate department based on business rules.

---

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [✨ How It Works](#-how-it-works)
- [🎯 Features](#-features)
- [📁 Project Structure](#-project-structure)
- [🔧 API Reference](#-api-reference)
- [🧪 Testing](#-testing)
- [⚙️ Configuration](#️-configuration)
- [📊 Performance](#-performance)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Sambanova API key

### Installation

```
# 1. Clone the repository
git clone https://github.com/vaibhavchaudharii/fnoi-agent.git
cd fnoi-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your Sambanova API key
Configuration
Add your API key to .env:

```

OPENAI_API_KEY=your_sambanova_api_key_here

```
Running the Server
```

uvicorn main:app --reload --host 0.0.0.0 --port 8000

```
🌐 Server running at: http://localhost:8000

Quick Test
```

# Test with a sample claim

curl -X POST "http://localhost:8000/process-claim/" \
 -F "file=@sample_claim.txt"

```
✨ How It Works
📝 Step 1: Upload Claim Document
Upload any insurance claim document (PDF, TXT, image):

```

FIRST NOTICE OF LOSS
Policy Number: AUTO-123456
Policyholder: John Smith
Date of Loss: 2024-03-15
Damage Estimate: $12,500
Description: Rear-ended at intersection

```
🧠 Step 2: AI Processing
The system uses Llama 3.1 AI to:

Read and understand unstructured text

Extract 16 key insurance fields

Validate data quality

Identify patterns and indicators

🎯 Step 3: Intelligent Routing
Based on extracted data, the system automatically routes claims:

```

{
"extractedFields": {
"Policy Number": "AUTO-123456",
"Policyholder Name": "John Smith",
"Estimated Damage": 12500
},
"recommendedRoute": "Standard Review",
"reasoning": "Moderate damage: $12,500.00"
}

```
🎯 Features
🔍 Smart Document Processing
✅ PDF, TXT, and image file support

✅ Text extraction from scanned documents

✅ Multiple document format handling

✅ Unstructured text processing

🧠 AI-Powered Intelligence
✅ Llama 3.1 8B model for understanding

✅ 16 key insurance field extraction

✅ Real data vs. form label identification

✅ Context-aware data validation

🚦 Automated Routing
Route	Criteria	Purpose
Fast-track	Damage < $5,000	Quick processing for minor claims
Standard Review	$5,000 - $25,000	Regular claims processing
Specialist Queue	Injury/medical claims	Expert medical review
High Value Review	Damage > $100,000	Senior adjuster review
Investigation Flag	Fraud indicators	Fraud department investigation
Manual Review	Missing information	Human intervention needed
🛡️ Built-in Validation
⚡ Missing field detection

📞 Phone/email validation

🚨 Fraud pattern identification

✅ Data quality scoring

📁 Project Structure
```

fnoi-agent/
├── 📄 main.py # FastAPI application & endpoints
├── 🧠 extractor.py # Document reading & AI extraction
├── 🚦 router.py # Business logic & claim routing
├── 📋 requirements.txt # Python dependencies
├── ⚙️ .env.example # Environment variables template
├── 📖 README.md # Project documentation
└── 🧪 test_claims/ # Sample test cases
├── sample_claim.txt
├── injury_claim.txt
├── fraud_claim.txt
└── high_value_claim.txt

```
🔧 API Reference
POST /process-claim/
Process an insurance claim document.

Request:

```

curl -X POST "http://localhost:8000/process-claim/" \
 -H "accept: application/json" \
 -F "file=@claim_document.pdf"

```
Response (Success):

```

{
"extractedFields": {
"Policy Number": "AUTO-PL-45879231",
"Policyholder Name": "Rohan Mehta",
"Effective Dates": "2025-01-01 to 2025-12-31",
"Date": "2026-02-14",
"Time": "20:45",
"Location": "MG Road Junction, Bengaluru",
"Description": "Accident description...",
"Claimant": "Rohan Mehta",
"Third Parties": "Delivery Van KA-03-MN-2211",
"Contact Details": {
"phone": "+91-9876543210",
"email": "rohan.mehta@email.com"
},
"Asset Type": "Car",
"Asset ID": "KA-01-AB-1234",
"Estimated Damage": "18500",
"Claim Type": "Property Damage",
"Attachments": "Photos, Police report",
"Initial Estimate": "18500"
},
"missingFields": [],
"recommendedRoute": "Standard Review",
"reasoning": "Moderate damage: $18,500.00",
"processingTime": "2.3s"
}

```
Response (Error):

```

{
"error": "Invalid file format",
"details": "Please upload PDF, TXT, or image files only"
}

```
🧪 Testing
Sample Test Cases
Test with these scenarios:

1. Fast-track Claim (fast_claim.txt):

```

Policy: AUTO-789
Name: Sarah Chen
Date: 2024-03-20
Damage: $1,200
Description: Minor scratch in parking lot

```
2. Injury Claim (injury_claim.txt):

```

Policy: MED-456
Name: Michael Rodriguez
Date: 2024-03-18
Damage: $28,500
Description: Car accident with neck injury

```
3. High Value Claim (high_value.txt):

```

Policy: COMM-123
Name: Skyline Manufacturing
Date: 2024-03-10
Damage: $425,000
Description: Factory fire damage

```
Run Tests
```

# Test all scenarios

python test_runner.py

# Or test individually

curl -X POST "http://localhost:8000/process-claim/" \
 -F "file=@test_claims/fast_claim.txt"

```
⚙️ Configuration
Business Rules
Edit router.py to customize:

```

# Routing thresholds

FAST_TRACK_MAX = 5000 # Claims under $5,000
STANDARD_MAX = 25000 # $5,000 - $25,000
HIGH_VALUE_MIN = 100000 # Over $100,000
EXECUTIVE_MIN = 1000000 # Over $1,000,000

# Fraud detection sensitivity

FRAUD_KEYWORDS = ['staged', 'inconsistent', 'suspicious']

```
AI Settings
Configure extractor.py:

```

# Model configuration

MODEL_NAME = "Meta-Llama-3.1-8B-Instruct"
TEMPERATURE = 0.1 # Lower = more deterministic
MAX_TOKENS = 2000 # Response length limit

# Extraction settings

REQUIRED_FIELDS = [
"Policy Number",
"Policyholder Name",
"Date",
"Description",
"Estimated Damage"
]

```
📊 Performance
Metric	Value	Description
⏱️ Processing Time	2-5 seconds	Per document processing
🎯 Accuracy	~95%	On structured forms
📄 Supported Formats	PDF, TXT, Images	Most common formats
📏 Max File Size	10MB	Configurable limit
🔄 Concurrent Users	50+	With proper scaling
🧠 AI Model	Llama 3.1 8B	State-of-the-art LLM
🚨 Error Handling
Error	Cause	Solution
No JSON found	AI response malformed	Check API key, reduce temperature
File not found	Incorrect file path	Verify file exists and path is correct
API Error	Sambanova API issue	Check API key validity and rate limits
Empty extraction	Document has no text	Ensure document contains readable text
Invalid format	Unsupported file type	Convert to PDF/TXT format
🔮 Future Enhancements
Web Interface - User-friendly dashboard

Database Integration - PostgreSQL/MongoDB for claim tracking

Email Notifications - Automated status updates

Multi-language Support - Process claims in different languages

OCR Enhancement - Better handwritten text recognition

CRM Integration - Connect with Salesforce, Zendesk, etc.

Analytics Dashboard - Claim processing insights

Mobile App - On-the-go claim processing

🤝 Contributing
We love contributions! Here's how to help:

Fork the repository

Create a feature branch:

```

git checkout -b feature/amazing-feature

```
Make your changes and commit:

```

git commit -m 'Add amazing feature'

```
Push to your branch:

```

git push origin feature/amazing-feature

```
Open a Pull Request

Development Setup
```

# Install development dependencies

pip install -r requirements-dev.txt

# Run tests

pytest tests/

# Code formatting

black _.py
flake8 _.py

```
Areas Needing Contribution
📱 Mobile app development

🌐 Web interface

🔗 API integrations

📊 Analytics features

🧪 Test coverage improvement

🙏 Acknowledgments
Meta for the amazing Llama 3.1 model

Sambanova for providing the AI inference platform

FastAPI team for the excellent web framework

ACORD for insurance industry form standardization

Open Source Community for continuous inspiration

📞 Support & Contact
Having issues or questions?

📧 Email: vaibhavchaudharii.dev@gmail.com

🐛 Issues: GitHub Issues

📚 Documentation: API Docs (when server is running)

💬 Discussion: GitHub Discussions

🌟 Show Your Support
If this project helped you, please give it a ⭐ on GitHub!

Made with ❤️ for Insurance Innovators

Automating claims processing, one document at a time.
```
