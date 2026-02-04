# pubmed_evidence_summary_final.py

import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import re
import time

# --------------------------- PubMed API Core --------------------------- #

def fetch_pubmed_ids(query, retries=3, delay=2):
    """Fetch PubMed IDs for a given query with retry logic."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmax": 10, "retmode": "xml"}

    for attempt in range(retries):
        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            return [elem.text for elem in ET.fromstring(response.text).findall(".//Id")]
        except Exception as e:
            print(f"⚠️ PubMed search failed (attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)
    return []


def fetch_pubmed_summaries(pmids, retries=3, delay=2):
    """Fetch summaries (titles, sources, dates) for a list of PubMed IDs."""
    if not pmids:
        return []

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            summaries = []
            root = ET.fromstring(response.text)
            for docsum in root.findall(".//DocSum"):
                title = docsum.findtext(".//Item[@Name='Title']")
                source = docsum.findtext(".//Item[@Name='Source']")
                pubdate = docsum.findtext(".//Item[@Name='PubDate']")
                if title:
                    summaries.append({
                        "title": title.strip(),
                        "source": source or "Unknown",
                        "pubdate": pubdate or "N/A"
                    })
            return summaries
        except Exception as e:
            print(f"⚠️ Summary fetch failed (attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)
    return []


def refine_keywords(summaries):
    """Extract frequent non-trivial keywords to refine searches."""
    text = " ".join([s["title"] for s in summaries]).lower()
    words = re.findall(r"\b[a-z]{5,}\b", text)
    common = {}
    for w in words:
        common[w] = common.get(w, 0) + 1
    top_words = sorted(common, key=common.get, reverse=True)[:5]
    return top_words


# --------------------------- Evidence Generator --------------------------- #

def generate_evidence_summary(clinical_input):
    """Perform hybrid PubMed search focusing only on symptoms."""
    patient = clinical_input.patient
    symptoms = clinical_input.symptoms or []

    if not symptoms:
        print("⚠️ No symptoms provided — skipping PubMed search.")
        return {
            "patient_id": patient.id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query": "",
            "top_articles": [],
            "snippet": "No symptoms provided — no PubMed query executed."
        }

    # Step 1: Run a separate query for each symptom
    all_summaries = []
    print(f"\n🔍 Starting hybrid PubMed search for patient {patient.id}...")

    for symptom in symptoms:
        query = f"{symptom} AND treatment"
        print(f"   ↳ Searching: {query}")
        pmids = fetch_pubmed_ids(query)
        summaries = fetch_pubmed_summaries(pmids)
        all_summaries.extend(summaries)
        time.sleep(0.5)

    if not all_summaries:
        return {
            "patient_id": patient.id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query": "No relevant data found.",
            "top_articles": [],
            "snippet": "No relevant clinical literature found for the given symptoms."
        }

    # Step 2: Extract frequent terms and refine with a single combined query
    keywords = refine_keywords(all_summaries)
    refined_query = f"({' OR '.join(symptoms)}) AND ({' OR '.join(keywords)}) AND treatment"
    print(f"   🧠 Extracted keywords: {', '.join(keywords)}")
    print(f"   🎯 Running refined query: {refined_query}")

    pmids = fetch_pubmed_ids(refined_query)
    refined_summaries = fetch_pubmed_summaries(pmids)

    # Combine results
    combined = refined_summaries[:10] or all_summaries[:10]
    snippet_lines = [
        f"• {a['title']} ({a['source']}, {a['pubdate']})"
        for a in combined
    ]
    snippet = "\n".join(snippet_lines)

    # Step 3: Return structured summary (OCI-readable)
    return {
        "patient_id": patient.id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": refined_query,
        "top_articles": combined,
        "snippet": snippet
    }
