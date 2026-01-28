import requests
import json

def get_researchmap_data(permalink):
    url = f"https://api.researchmap.jp/{permalink}"

    data = requests.get(url).json()   # dict として取得

    #名前情報を抽出
    name = {
        "family_name": data.get("family_name"),
        "given_name": data.get("given_name")
    }

    # 学歴情報を抽出
    education = None
    for item in data.get("@graph", []):
        if item.get("@type") == "education":
            education = item.get("items")
            break

    result = {
        "name": name,
        "education": education
    }

    output_dir = "researcher_data"
    import os
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"researchmap_{permalink}_filtered.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


permalink = "senr1"
get_researchmap_data(permalink)