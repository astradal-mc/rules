import json
from collections import defaultdict

# Correct path pointing to the main folder
with open("main/rules.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Preserve the order categories appear in the JSON
category_order = []
rules_by_category = defaultdict(list)

for rule in data["rules"]:
    category = rule["category"]
    if category not in category_order:
        category_order.append(category)
    rules_by_category[category].append(rule)

# Build README content
lines = []
lines.append("# Astradal Rules\n")
lines.append("_These rules are automatically generated from `rules.json`._\n\n")

# Use category_order instead of sorted keys
for category in category_order:
    lines.append(f"## {category} Rules\n\n")
    for rule in sorted(rules_by_category[category], key=lambda r: r["id"]):
        severity = rule["severity"].capitalize()
        lines.append(f"### {rule['id']}. {rule['title']}\n")
        lines.append(f"**Severity:** `{severity}`\n\n")
        lines.append(f"{rule['description']}\n\n")

# Render punishment tiers
lines.append("---\n")
lines.append("## Punishments by Severity\n\n")

for severity, punishments in data["punishments"].items():
    lines.append(f"### {severity.capitalize()}\n")
    for p in punishments:
        lines.append(f"- {p}")
    lines.append("")  # Blank line

# Render warning limits
limits = data["warningLimits"]
lines.append("---\n")
lines.append("## Global Warning Policy\n\n")
lines.append(f"- Maximum warnings before punishment: **{limits['maxWarnings']}**")

# Added the expiration check so it renders the new 6-month rule
if "expiration" in limits:
    lines.append(f"- Warning Expiration: **{limits['expiration']}**")

lines.append(f"- Consequence after max warnings: **{limits['consequence']}**")
lines.append(f"- After appeal ban: **{limits['otherwise']}**\n")

# Write to README.md at the root of the repo
with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("README.md updated successfully.")
