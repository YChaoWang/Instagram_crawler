# save_data.py
import json
import os


def save_to_json(data, filename):
    """將字典保存為 JSON 文件"""
    # 確保 result 資料夾存在
    os.makedirs("result", exist_ok=True)  # 如果資料夾不存在則創建

    # 定義完整的文件路徑
    file_path = os.path.join("result", filename)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)  # 存儲為 JSON 格式
    print(f"數據已成功保存到 {file_path}")
