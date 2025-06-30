import json
import csv
from dotenv import load_dotenv
import os

load_dotenv()
os.makedirs("outputs/diffs", exist_ok=True)

IGNORED_FIELDS = {"id", "created_at", "updated_at", "space_id", "schema_id", "uuid"}

space_1 = os.getenv("SPACE_ID")
space_2 = os.getenv("SPACE_ID_2")
output_file = "outputs/component_comparison.csv"

with open(f"outputs/components_{space_1}.json", "r", encoding="utf-8") as f:
    comps1 = json.load(f)
comps1 = {comp["name"]: comp for comp in comps1["components"]}
with open(f"outputs/components_{space_2}.json", "r", encoding="utf-8") as f:
    comps2 = json.load(f)
comps2 = {comp["name"]: comp for comp in comps2["components"]}


all_names = set(comps1.keys()) | set(comps2.keys())
results = []

for name in sorted(all_names):
    space_1_comps = comps1.get(name)
    space_2_comps = comps2.get(name)

    if space_1_comps and not space_2_comps:
        results.append([name, f"Only in {space_1}", ""])
    elif space_2_comps and not space_1_comps:
        results.append([name, f"Only in {space_2}", ""])
    else:
        diffs = []
        for key in set(space_1_comps.keys()) | set(space_2_comps.keys()):
            if key in IGNORED_FIELDS:
                continue
            v1 = space_1_comps.get(key)
            v2 = space_2_comps.get(key)
            if v1 != v2:
                diffs.append({
            "problematic_field": key,
            f"{space_1}_value": v1,
            f"{space_2}_value": v2
        })
        if diffs:
            summary = f"{len(diffs)} mismatched field(s): " + ", ".join(d['problematic_field'] for d in diffs)
            results.append([
                name,
                "Field mismatch",
                summary
            ])
            with open(f"outputs/diffs/{name}_diff.json", "w", encoding="utf-8") as f:
                json.dump(diffs, f, indent=2, ensure_ascii=False)

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Component Name", "Issue", "Details"])
    writer.writerows(results)

print(f"Comparison done. Results saved to {output_file}")
