import math
from typing import List
from job_hunter.models import BasePortalPlugin, JobLead, SearchConfig

# Handle optional jobspy import
try:
    from jobspy import scrape_jobs
except ImportError:
    scrape_jobs = None

class JobSpyPortalPlugin(BasePortalPlugin):
    @property
    def name(self) -> str:
        return "JobSpy (LinkedIn/Indeed)"

    def fetch_leads(self, config: SearchConfig) -> List[JobLead]:
        if not scrape_jobs:
            print(f"[!] {self.name}: python-jobspy not installed.")
            return []

        print(f"[*] Plugin {self.name}: Scouting for {config.job_titles}...")
        results = []
        neg_string = " ".join([f"-{kw}" for kw in config.negative_keywords])
        sites = ["indeed", "linkedin"]
        
        for title in config.job_titles:
            query = f'"{title}" {neg_string}'
            try:
                # Local Search
                df = scrape_jobs(
                    site_name=sites,
                    search_term=query,
                    location=config.location,
                    distance=config.radius_km,
                    results_wanted=15,
                    country_indeed='germany'
                )
                results.extend(self._parse_df(df))

                # Global Remote
                if config.remote_flexibility:
                    df_remote = scrape_jobs(
                        site_name=sites,
                        search_term=query,
                        location="Germany",
                        is_remote=True,
                        results_wanted=10,
                        country_indeed='germany'
                    )
                    results.extend(self._parse_df(df_remote))
            except Exception as e:
                print(f"[!] {self.name} error: {e}")
        return results

    def _parse_df(self, df) -> List[JobLead]:
        parsed = []
        if df is None or df.empty:
            return parsed
        for _, row in df.iterrows():
            clean = {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in row.items()}
            parsed.append(JobLead(
                title=clean.get('title') or 'Unknown',
                company=clean.get('company') or 'Unknown',
                location=clean.get('location') or 'Unknown',
                is_remote=bool(clean.get('is_remote')),
                source=clean.get('site') or 'JobSpy',
                url=clean.get('job_url') or 'N/A',
                date_posted=str(clean.get('date_posted')) if clean.get('date_posted') else None
            ))
        return parsed
