import json


def extract_json_from_str(json_str):
    try:
        if "```json" in json_str:
            start = json_str.find("```json") + len("```json")
            end = json_str.find("```", start)
            json_str = json_str[start:end].strip()
            return json.loads(json_str)
        elif ">" in json_str:
            start = json_str.rfind(">") + len(">")
            json_str = json_str[start : len(json_str)].strip()
            return json.loads(json_str)
        else:
            return json.loads(json_str)
    except:
        return eval(json_str)
