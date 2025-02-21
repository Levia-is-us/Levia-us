import json


def extract_json_from_str(json_str):
    if not isinstance(json_str, str):
        return json_str   
    
    try:
        if "```json" in json_str:
            start = json_str.find("```json") + len("```json")
            end = json_str.find("```", start)
            json_str = json_str[start:end].strip()
            try:
                return json.loads(json_str)
            except:
                return eval(json_str)
        elif ">" in json_str:
            start = json_str.rfind(">") + len(">")
            json_str = json_str[start : len(json_str)].strip()
            return json.loads(json_str)
        else:
            return json.loads(json_str)
    except:
        try:
            cleaned_str = json_str.strip().replace('\n', '').replace('    ', '')
            return json.loads(cleaned_str)
        except:
            raise Exception("Failed to parse JSON string")




def extract_code_breakdown_from_doc(doc):
    start = doc.find("<code_breakdown>") + len("<code_breakdown>")
    end = doc.find("</code_breakdown>", start)
    return doc[start:end].strip()


def extract_str_from_doc(doc):
    if ">" in doc:
        start = doc.rfind(">") + len(">")
        doc = doc[start : len(doc)].strip()
        return doc
    else:
        return doc
