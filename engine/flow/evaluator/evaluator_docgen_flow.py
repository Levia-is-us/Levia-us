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

def extract_code_breakdown_from_doc(doc):
    start = doc.find("<code_breakdown>") + len("<code_breakdown>")
    end = doc.find("</code_breakdown>", start)
    return doc[start:end].strip()
