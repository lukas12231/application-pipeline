import json
import os
import argparse
import re
from typing import List, Dict
from job_hunter.models import JobLead, UserProfile

class SemanticFilter:
    def __init__(self, config_file: str, profile_file: str, enriched_leads_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        with open(profile_file, 'r') as f:
            self.profile = UserProfile(**json.load(f))
        with open(enriched_leads_file, 'r') as f:
            data = json.load(f)
            self.leads = [JobLead(**item) for item in data]
        
        self.min_salary = self.config["filters"].get("min_salary_eur", self.profile.min_salary)
        self.target_location = self.config["search"].get("location", "").lower()
        self.remote_allowed = self.config["filters"].get("remote_flexibility", True)
        self.filtered_results = []

        self.company_tiers = {
            "bwi": 1.0, "deloitte": 0.95, "telekom": 0.9, "t-systems": 0.9, 
            "zeiss": 0.95, "rohde & schwarz": 0.9, "porsche": 1.0, "bmw": 1.0,
            "mercedes": 1.0, "sap": 1.0, "amazon": 1.0, "microsoft": 1.0, 
            "google": 1.0, "accenture": 0.9, "capgemini": 0.85, "ferchau": 0.75, 
            "diva-e": 0.8
        }

    def run(self):
        print(f"[*] Analyzing {len(self.leads)} leads with profile: {self.profile.name}")
        for lead in self.leads:
            score_data = self._calculate_fit_score(lead)
            lead.fit_score = score_data["total"]
            lead.fit_reasoning = score_data["reasoning"]
            lead.ai_summary_title = self._llm_assisted_summary(lead)
            lead.tags = self._generate_tags(lead)

            # --- Logic check for "Professional Practices" ---
            # 1. Salary: Benefit of doubt for Tier-1 companies
            if score_data["salary_conflict"]:
                if self._get_company_pay_score(lead.company) < 0.9:
                    print(f"    [-] Dropping {lead.title} @ {lead.company}: Salary conflict.")
                    continue
            
            # 2. Inclusivity: "Soft Mismatch" handling
            # Instead of dropping on education mismatch, we just penalize the score
            # unless it's clearly for a junior/trainee role and we are senior
            if score_data["seniority_mismatch"]:
                print(f"    [-] Dropping {lead.title}: Seniority mismatch.")
                continue

            self.filtered_results.append(lead)

        self.filtered_results.sort(key=lambda x: x.fit_score, reverse=True)
        self.save_results()

    def _llm_assisted_summary(self, lead: JobLead) -> str:
        """
        Placeholder for real LLM integration. 
        Current implementation uses heuristic matching as fallback.
        """
        title = lead.title.lower()
        mapping = {
            "cloud": "Cloud Strategy & Engineering",
            "devops": "DevOps & Infrastructure",
            "sre": "Site Reliability Engineering",
            "system": "Systems Architecture"
        }
        for kw, readable in mapping.items():
            if kw in title: return readable
        return lead.title.split("(")[0].strip()

    def _generate_tags(self, lead: JobLead) -> List[str]:
        tags = []
        desc = (lead.description or "").lower()
        if any(kw in desc for kw in ["master", "m.sc.", "diplom"]): tags.append("Academic-Required")
        if "remote" in desc or "homeoffice" in desc or lead.is_remote: tags.append("Remote-Friendly")
        if any(hp in lead.company.lower() for hp in self.company_tiers): tags.append("Top-Tier-Pay")
        
        # Skill tags based on user profile
        for skill in self.profile.core_skills:
            if skill.lower() in desc: tags.append(skill)
        return list(set(tags))[:8]

    def _get_company_pay_score(self, company_name: str) -> float:
        name = company_name.lower()
        for firm, score in self.company_tiers.items():
            if firm in name: return score
        return 0.6

    def _calculate_fit_score(self, lead: JobLead) -> Dict:
        desc = (lead.description or "").lower()
        title = lead.title.lower()
        loc = lead.location.lower()
        comp = lead.company.lower()
        
        # Weights: Skill (40%), Salary/Company (25%), Location/Flex (20%), Education (15%)
        scores = {"salary": 0.5, "education": 0.5, "skills": 0, "flexibility": 0}
        reasoning = []
        salary_conflict = False
        seniority_mismatch = False

        # 1. Salary & Company
        salary_range = self._extract_salary_range(desc)
        found_salary = max(salary_range) if salary_range else None
        comp_pay_score = self._get_company_pay_score(comp)

        if found_salary:
            if found_salary >= (self.min_salary * 0.9):
                scores["salary"] = 1.0
                reasoning.append(f"Salary match (~{found_salary}€)")
            else:
                salary_conflict = True
                scores["salary"] = 0.3
        else:
            scores["salary"] = comp_pay_score
            if comp_pay_score >= 0.9: reasoning.append("High-pay tier company")

        # 2. Education & Seniority
        has_master_req = any(kw in desc for kw in ["master", "m.sc.", "diplom", "university", "hochschule"])
        is_junior = any(kw in title or kw in desc for kw in ["junior", "entry level", "berufseinsteiger", "ausbildung"])
        
        if self.profile.experience_level.lower().startswith("senior") and is_junior:
            seniority_mismatch = True
        
        scores["education"] = 1.0 if has_master_req else 0.7 # Soft penalty for missing education mention

        # 3. Skills (The most important)
        matches = [s for s in self.profile.core_skills if s.lower() in desc or s.lower() in title]
        scores["skills"] = len(matches) / max(len(self.profile.core_skills), 1)
        if matches: reasoning.append(f"Matched {len(matches)} core skills")

        # 4. Flexibility
        is_remote = lead.is_remote or any(kw in desc or kw in title for kw in ["remote", "homeoffice", "hybrid"])
        is_local = any(loc_pref.lower() in loc or loc_pref.lower() in desc for loc_pref in self.profile.preferred_locations)
        
        if is_local: 
            scores["flexibility"] = 1.0
            reasoning.append("Target location")
        elif is_remote: 
            scores["flexibility"] = 0.9
            reasoning.append("Remote flexibility")
        else: 
            scores["flexibility"] = 0.4

        total = (scores["salary"] * 0.25) + (scores["education"] * 0.15) + (scores["skills"] * 0.40) + (scores["flexibility"] * 0.20)
        return {
            "total": round(total, 2), 
            "reasoning": " | ".join(reasoning), 
            "salary_conflict": salary_conflict, 
            "seniority_mismatch": seniority_mismatch
        }

    def _extract_salary_range(self, text: str) -> List[int]:
        patterns = [r'(\d{2,3})[\.\s]?000\s?(?:€|eur|gehalt)', r'(\d{2,3})\s?k\s?(?:€|eur|gehalt)']
        found = []
        for p in patterns:
            matches = re.findall(p, text)
            for m in matches:
                val = int(m.replace('.', '').replace(' ', ''))
                if 40 <= val <= 250: found.append(val * 1000)
                elif 40000 <= val <= 250000: found.append(val)
        return sorted(list(set(found))) if found else None

    def save_results(self):
        output_path = "job_leads_filtered.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump([l.model_dump() for l in self.filtered_results], f, indent=4, ensure_ascii=False)
        print(f"[+] Saved {len(self.filtered_results)} leads to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="hunter_config.json")
    parser.add_argument("--profile", default="profile.json")
    parser.add_argument("--input", default="job_leads_enriched.json")
    args = parser.parse_args()
    filt = SemanticFilter(args.config, args.profile, args.input)
    filt.run()
