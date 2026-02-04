# CDSA GenAI Architecture

A Clinical Decision Support (CDS) system that integrates patient data with evidence-based medical literature from PubMed to assist healthcare providers in making informed clinical decisions.

## Overview

This project provides a pipeline for processing patient clinical data and generating evidence summaries from PubMed literature. The system is designed to work with Oracle Cloud Infrastructure (OCI) and other CDS models to provide clinical recommendations based on patient symptoms, vitals, and lab results.

## Features

- **Patient Data Management**: Structured input handling for patient demographics, vitals, labs, and symptoms
- **Input Validation**: Prevents Protected Health Information (PHI) leakage with name detection and format validation
- **Hybrid PubMed Search**: 
  - Individual symptom-based queries
  - Keyword extraction and refinement
  - Combined refined search for comprehensive results
- **Evidence Summarization**: Generates structured JSON summaries with top relevant articles
- **BMI Calculation**: Automatic BMI computation from height and weight
- **Visual Workflows**: Diagram generation for pipeline visualization

## Project Structure

```
cdsa-genai-architecture/
├── cdsa-genai-public/
│   ├── schema_model.py              # Pydantic models for patient data
│   ├── pubmed_evidence_summary_final.py  # PubMed API integration & evidence generation
│   ├── test_user_input.py           # Interactive CLI for patient input
│   ├── utils.py                      # Utility functions (height parsing, etc.)
│   ├── cdsa_pipeline_diagram.py     # Pipeline workflow diagram generator
│   ├── pubmed_api_test.py           # Simple PubMed API test script
│   └── patient_evidence_summaries.json  # Sample output data
├── pubmed_search_flow_diagram.py    # PubMed search flow visualization
├── cds_pipeline_workflow            # Generated workflow diagram
└── README.md                        # This file
```

## Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Dependencies

Install required packages:

```bash
pip install requests pydantic graphviz
```

**Note**: For Graphviz diagrams, you may also need to install Graphviz system package:
- **Windows**: Download from [Graphviz website](https://graphviz.org/download/)
- **macOS**: `brew install graphviz`
- **Linux**: `sudo apt-get install graphviz` or `sudo yum install graphviz`

## Usage

### Interactive Patient Input

Run the main interactive script to enter patient data and generate evidence summaries:

```bash
cd cdsa-genai-public
python test_user_input.py
```

The script will prompt you for:
- Patient ID (alphanumeric, must contain at least one number)
- Age, Sex, Height (e.g., 5'9), Weight (lbs)
- Optional: Blood pressure, Heart rate, HBA1C, LDL
- Symptoms (comma-separated)
- Additional notes

### Programmatic Usage

```python
from schema_model import ClinicalInput, Patient, Vitals, Labs
from pubmed_evidence_summary_final import generate_evidence_summary
from datetime import datetime, timezone

# Create patient data
patient = Patient(
    id="P12345",
    age=45,
    sex="male",
    height_in=70,  # 5'10"
    weight_lb=180
)

clinical_input = ClinicalInput(
    patient=patient,
    vitals=Vitals(blood_pressure="140/90", heart_rate=85),
    labs=Labs(hba1c=7.2, ldl=150),
    symptoms=["chest pain", "shortness of breath"],
    notes="Patient reports exercise intolerance",
    timestamp=datetime.now(timezone.utc)
)

# Generate evidence summary
summary = generate_evidence_summary(clinical_input)
print(summary["snippet"])
```

### Generate Workflow Diagrams

```bash
# Generate CDS pipeline workflow diagram
python cdsa-genai-public/cdsa_pipeline_diagram.py

# Generate PubMed search flow diagram
python pubmed_search_flow_diagram.py
```

## How It Works

### 1. Input Validation
- Validates patient ID format (alphanumeric with at least one number)
- Checks for potential name leakage in symptoms and notes
- Validates data formats (blood pressure, height, etc.)

### 2. PubMed Evidence Search (Hybrid Approach)

**Phase 1: Individual Symptom Queries**
- For each symptom, runs a query: `{symptom} AND treatment`
- Collects article summaries (title, source, publication date)

**Phase 2: Keyword Extraction & Refinement**
- Extracts frequent keywords from initial results
- Builds refined query: `(symptom1 OR symptom2) AND (keyword1 OR keyword2) AND treatment`
- Fetches top articles from refined search

**Phase 3: Summary Generation**
- Combines and deduplicates results
- Returns top 10 articles with structured metadata
- Generates human-readable snippet for display

### 3. Output Format

The evidence summary returns a JSON structure:

```json
{
  "patient_id": "P12345",
  "timestamp": "2026-02-04T12:00:00Z",
  "query": "refined PubMed query string",
  "top_articles": [
    {
      "title": "Article Title",
      "source": "Journal Name",
      "pubdate": "2024 Jan"
    }
  ],
  "snippet": "Formatted text summary of articles"
}
```

## Integration with CDS Models

The output is designed to be consumed by Clinical Decision Support models (e.g., on OCI) that:
1. Read patient data (vitals, labs, BMI, symptoms)
2. Cross-reference with PubMed evidence summaries
3. Generate clinical assessments and recommendations
4. Display results in EHR systems

## Data Models

### Patient
- `id`: Patient identifier (alphanumeric)
- `age`: Age in years
- `sex`: "male" or "female"
- `height_in`: Height in inches
- `weight_lb`: Weight in pounds
- `bmi`: Calculated BMI (property)

### ClinicalInput
- `patient`: Patient object
- `vitals`: Optional Vitals object (BP, heart rate)
- `labs`: Optional Labs object (HBA1C, LDL)
- `symptoms`: Optional list of symptom strings
- `notes`: Optional clinical notes
- `timestamp`: DateTime of input

## Privacy & Security

- **PHI Protection**: Input validation prevents full names from being entered
- **Patient ID Format**: Enforces alphanumeric IDs (no full names)
- **No Data Storage**: Patient data is processed but not persisted locally
- **API Rate Limiting**: Built-in retry logic and delays for PubMed API calls

## API Reference

### PubMed Functions

- `fetch_pubmed_ids(query, retries=3, delay=2)`: Search PubMed and return article IDs
- `fetch_pubmed_summaries(pmids, retries=3, delay=2)`: Fetch article summaries by IDs
- `refine_keywords(summaries)`: Extract frequent keywords from summaries
- `generate_evidence_summary(clinical_input)`: Main function to generate evidence summary

### Utility Functions

- `parse_height(height_str)`: Convert height string (e.g., "5'9") to inches

## Testing

Test PubMed API connectivity:

```bash
python cdsa-genai-public/pubmed_api_test.py
```

## Limitations

- PubMed API rate limits apply (3 requests/second recommended)
- Requires internet connection for PubMed queries
- Results depend on PubMed database coverage
- No full-text article access (only metadata)

## Future Enhancements

- Integration with full-text article APIs
- Caching mechanism for repeated queries
- Enhanced keyword extraction using NLP
- Support for additional lab values and vitals
- Web-based UI for clinical input
- Database integration for patient data storage

## Contact

For questions or issues, please open an issue on GitHub.

---

**Note**: This project is for **research purposes only** and is designed to explore how Generative AI can serve as a tool in heavily regulated industries, such as healthcare. This system is intended for clinical decision support research and should be used in conjunction with professional medical judgment. It does not replace clinical expertise or direct patient care, and is not intended for production use in clinical settings without appropriate regulatory review and approval.
