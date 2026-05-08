import requests
import json
import os
import argparse
import time
from typing import List, Dict
from job_hunter.models import JobLead

class JobExtractor:
    def __init__(self, leads_file: str, output_file: str):
        self.leads_file = leads_file
        self.output_file = output_file
        self.enriched_leads = []

    def load_leads(self) -> List[JobLead]:
        if not os.path.exists(self.leads_file):
            print(f"[!] Leads file {self.leads_file} not found.")
            return []
        with open(self.leads_file, 'r') as f:
            data = json.load(f)
            return [JobLead(**item) for item in data]

    def extract_content(self, limit: int = 20):
        leads = self.load_leads()
        if not leads: return

        print(f"[*] Extracting content for {min(len(leads), limit)} leads...")
        count = 0
        for lead in leads:
            if count >= limit: break
            if not lead.url or lead.url == "N/A": continue

            print(f"    [{count+1}] Crawling: {lead.title} @ {lead.company}...")
            lead.description = self._fetch_url(lead.url)
            self.enriched_leads.append(lead)
            count += 1
            time.sleep(1)

        self.save_results()

    def _fetch_url(self, url: str) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                for s in soup(['script', 'style']): s.decompose()
                return soup.get_text(separator=' ', strip=True)
            return f"Error: {response.status_code}"
        except Exception as e:
            return str(e)

    def save_results(self):
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump([l.model_dump() for l in self.enriched_leads], f, indent=4, ensure_ascii=False)
        print(f"[+] Saved enriched leads to {self.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Job Content Extractor")
    parser.add_argument("--input", default="job_leads.json")
    parser.add_argument("--output", default="job_leads_enriched.json")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    extractor = JobExtractor(args.input, args.output)
    extractor.extract_content(limit=args.limit)
