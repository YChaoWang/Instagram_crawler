import re


def convert_post_count_to_int(post_count_str):
    # 使用正則表達式匹配數字和單位
    match = re.search(r"(\d+(?:\.\d+)?)([萬千百]?)", post_count_str)

    if match:
        num_value = float(match.group(1))  # 提取數字部分，允許浮點數
        unit = match.group(2)  # 提取單位部分

        # 根據單位詞乘以相應的倍數
        if unit == "萬":
            return int(num_value * 10000)
        elif unit == "千":
            return int(num_value * 1000)
        elif unit == "百":
            return int(num_value * 100)
        else:
            return int(num_value)  # 沒有單位時直接返回數字
    else:
        # 嘗試處理像 "6.245 objav" 的情況
        num_match = re.search(r"(\d+(?:\.\d+)?)", post_count_str)
        if num_match:
            return int(float(num_match.group(1)))  # 返回整數部分
        return 0  # 若未匹配到數字，返回 0
