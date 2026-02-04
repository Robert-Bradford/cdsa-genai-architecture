import requests
import xml.etree.ElementTree as ET

# Define a sample clinical query
query = "obesity AND hypertension AND treatment"

# PubMed API endpoint (E-utilities)
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# Search PubMed for the top 5 relevant article IDs
params = {
    "db": "pubmed",
    "term": query,
    "retmax": 5,  # Limit to 5 results
    "retmode": "xml"
}

# Add User-Agent to avoid NCBI blocking
headers = {"User-Agent": "Python PubMed API Client (user@example.com)"}

response = requests.get(base_url, params=params, headers=headers)

# Check if the response looks like XML
if not response.text.strip().startswith("<"):
    print("Error: Received invalid response from PubMed:")
    print(response.text)
    exit(1)

root = ET.fromstring(response.text)

# Extract the PubMed IDs (PMIDs)
pmids = [id_elem.text for id_elem in root.findall(".//Id")]

print(f"Found {len(pmids)} results for query: '{query}'")
print("PMIDs:", pmids)

# Fetch article summaries using ESummary
if pmids:
    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    summary_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }

    summary_resp = requests.get(summary_url, params=summary_params, headers=headers)

    # Check if the response is valid XML
    if not summary_resp.text.strip().startswith("<"):
        print("Error: Received invalid response from PubMed summary:")
        print(summary_resp.text)
        exit(1)

    summary_root = ET.fromstring(summary_resp.text)

    for docsum in summary_root.findall(".//DocSum"):
        title = docsum.findtext(".//Item[@Name='Title']")
        source = docsum.findtext(".//Item[@Name='Source']")
        pubdate = docsum.findtext(".//Item[@Name='PubDate']")
        print("\n🧠", title)
        print(f"📘 Source: {source} ({pubdate})")
