from engine.flow.evaluator.evaluator_docgen_prompt import (
    create_evaluator_docgen_prompt,
)
from engine.llm_provider.llm import chat_completion
import json


def evaluator_docgen_flow(code):
    prompt = create_evaluator_docgen_prompt(code)
    result = chat_completion(
        prompt, model="o1-mini", config={"temperature": 0, "max_tokens": 4000}
    )
    return result


def extract_json_from_doc(doc):
    try:
        if "```json" in doc:
            start = doc.find("```json") + len("```json")
            end = doc.find("```", start)
            doc = doc[start:end].strip()
            return json.loads(doc)
        else:
            return eval(doc)
    except:
        return json.loads(doc)



def extract_code_breakdown_from_doc(doc):
    start = doc.find("<code_breakdown>") + len("<code_breakdown>")
    end = doc.find("</code_breakdown>", start)
    return doc[start:end].strip()
