# VeryfiTest 
## Invoice Data Extraction System with Veryfi OCR API  

This Python project automates the extraction of structured data from invoices using Veryfi's OCR API. The system processes scanned invoices to retrieve key fields and line items, outputting the results in JSON format.  

## Features  
- **OCR Integration**: Connects with Veryfi's API to extract raw text from invoices  
- **Structured Data Extraction**: Parses and validates:  
  - Vendor details (name, address)  
  - Client information (bill-to name)  
  - Invoice metadata (number, date)  
  - Line items (SKU, description, quantity, tax, price, total)  
- **Format Validation**: Only processes documents matching expected invoice templates  
- **Unit Testing**: Includes pytest validation for core functions  

## Setup  
1. **Prerequisites**:  
   - Python 3.8+  (pip included)
   - Veryfi OCR API account in (https://hub.veryfi.com/signup/)
  
2. **Installation**:  
```bash

pip install veryfi pandas pytest python-dotenv
pip install --upgrade veryfi
pip install -r requirements.txt
python main.py
