import json
import datetime
import os

def generate_md():
    input_file = 'job_leads_filtered.json'
    config_file = 'hunter_config.json'
    output_file = 'job_leads.md'

    if not os.path.exists(input_file):
        print(f"[!] {input_file} not found. Skip report.")
        return

    with open(input_file, 'r') as f:
        data = json.load(f)
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    search = config.get("search", {})
    filters = config.get("filters", {})

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 🔍 Job Scouting Report: {search.get('location', 'Global')}\n\n")
        f.write(f"> **Generated:** {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
        f.write(f"> **Criteria:** {', '.join(search.get('job_titles', []))} | > {filters.get('min_salary_eur', 0)//1000}k€\n\n")
        
        if not data:
            f.write("## ⚠️ No matches found\n")
            f.write("Try adjusting your `hunter_config.json` or expanding the search radius.\n")
            return

        f.write("## 🎯 Top Recommendations\n")
        f.write("Select a lead and paste its description into `job_ad.txt` to proceed with the application.\n\n")
        
        for i, j in enumerate(data[:15]): # Top 15 leads
            score = j.get('fit_score', 0)
            # Badge logic
            if score >= 0.85: badge = "🟢 **Excellent Match**"
            elif score >= 0.7: badge = "🟡 **Good Match**"
            else: badge = "⚪ **Fair Match**"
            
            f.write(f"### {i+1}. {j.get('ai_summary_title') or j['title']} @ {j['company']}\n")
            f.write(f"- **Score:** {score} | {badge}\n")
            f.write(f"- **Location:** {j['location']} | **Remote:** {'Yes' if j.get('is_remote') else 'No'}\n")
            f.write(f"- **Reasoning:** {j.get('fit_reasoning', 'N/A')}\n")
            f.write(f"- **Tags:** {', '.join([f'`{t}`' for t in j.get('tags', [])])}\n")
            f.write(f"- **Action:** [View Original Posting]({j['url']})\n\n")
            f.write("---\n\n")

        f.write("\n## ⚙️ Search Configuration Summary\n")
        f.write(f"- **Titles:** {', '.join(search.get('job_titles', []))}\n")
        f.write(f"- **Negative Keywords:** {', '.join(search.get('negative_keywords', []))}\n")
        f.write(f"- **Min Salary:** {filters.get('min_salary_eur', 0)} €\n")

    print(f"[+] High-fidelity report generated: {output_file}")

if __name__ == '__main__':
    generate_md()
