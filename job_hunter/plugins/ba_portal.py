import requests
from typing import List
from job_hunter.models import BasePortalPlugin, JobLead, SearchConfig

class BAPortalPlugin(BasePortalPlugin):
    @property
    def name(self) -> str:
        return "BA-Jobbörse"

    def fetch_leads(self, config: SearchConfig) -> List[JobLead]:
        print(f"[*] Plugin {self.name}: Scouting for {config.job_titles}...")
        results = []
        url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
        headers = {
            "X-API-Key": "jobboerse-jobsuche",
            "User-Agent": "Mozilla/5.0"
        }
        
        for title in config.job_titles:
            params = {"was": title, "wo": config.location, "page": "1", "size": "20"}
            try:
                resp = requests.get(url, headers=headers, params=params, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    for job in data.get("stellenangebote", []):
                        job_id = job.get("hashID") or job.get("refnr")
                        results.append(JobLead(
                            title=job.get("beruf") or "Unknown",
                            company=job.get("arbeitgeber") or "Unknown",
                            location=job.get("arbeitsort", {}).get("ort") or config.location,
                            source=self.name,
                            url=f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{job_id}" if job_id else "N/A",
                            date_posted=job.get("veroeffentlichtAm")
                        ))
            except Exception as e:
                print(f"[!] {self.name} error: {e}")
        return results
