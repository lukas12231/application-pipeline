import json
import os
import argparse
import pkgutil
import importlib
from typing import List
from job_hunter.models import JobLead, SearchConfig, BasePortalPlugin

class HunterRegistry:
    def __init__(self):
        self.plugins: List[BasePortalPlugin] = []
        self._load_plugins()

    def _load_plugins(self):
        """Dynamically loads all plugins from the plugins sub-package."""
        import job_hunter.plugins as plugins_pkg
        path = os.path.dirname(plugins_pkg.__file__)
        for loader, module_name, is_pkg in pkgutil.iter_modules([path]):
            full_module_name = f"job_hunter.plugins.{module_name}"
            module = importlib.import_module(full_module_name)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BasePortalPlugin) and 
                    attr is not BasePortalPlugin):
                    self.plugins.append(attr())

    def execute_all(self, config: SearchConfig) -> List[JobLead]:
        all_leads = []
        for plugin in self.plugins:
            try:
                leads = plugin.fetch_leads(config)
                all_leads.extend(leads)
            except Exception as e:
                print(f"[!] Error in plugin {plugin.name}: {e}")
        return all_leads

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plugin-Based Job Scouting Engine")
    parser.add_argument("--config", default="hunter_config.json", help="Path to config")
    parser.add_argument("--output", default="job_leads.json", help="Output file")
    args = parser.parse_args()

    # Load Config
    with open(args.config, 'r') as f:
        raw_config = json.load(f)
    
    config = SearchConfig(
        job_titles=raw_config["search"]["job_titles"],
        location=raw_config["search"]["location"],
        radius_km=raw_config["search"]["radius_km"],
        negative_keywords=raw_config["search"].get("negative_keywords", []),
        remote_flexibility=raw_config["filters"].get("remote_flexibility", True)
    )

    registry = HunterRegistry()
    leads = registry.execute_all(config)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump([l.model_dump() for l in leads], f, indent=4, ensure_ascii=False)
    
    print(f"[+] Scouting complete. Found {len(leads)} leads across {len(registry.plugins)} plugins.")
