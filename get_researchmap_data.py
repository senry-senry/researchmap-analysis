import requests
import csv
import os
import json

# 保存先ディレクトリ
os.makedirs('researcher_data', exist_ok=True)

def get_researchmap_data(permalink):
    url = f"https://api.researchmap.jp/{permalink}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f'Error fetching {permalink}: {e}')
        return

    # 名前情報を抽出
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
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"researchmap_{permalink}_filtered.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f'Saved: {output_path}')


if __name__ == "__main__":
    with open('permalinks.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            permalink = row['Permalink']
            get_researchmap_data(permalink)