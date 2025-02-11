def check_plan_fittable_prompt(intent_a: str, intent_b: str, proposed_solution: str):
    system_prompt = "You are an expert in natural language understanding and semantic analysis."
    user_prompt = f"""
Intent A/Requirement Description: {intent_a}
Intent B and Proposed Solution: {intent_b}
proposed solution: {proposed_solution}
Your task is to compare two intents and evaluate whether a proposed solution fulfills intent A.

You need to analyze the information with following steps:
1. Analyze the relationship between Intent A and Intent B, are they doing the same thing?
2. Evaluate whether the proposed solution is sufficient to fulfill Intent A.

Output your findings in the following structured JSON format:
{{
    "intent_match": {{
        "result": "true or false",
        "reason": "Brief explanation of whether Intent A and Intent B match or not."
    }},
    "solution_sufficient": {{
        "result": "true or false", 
        "reason": "Brief explanation of whether the proposed solution satisfies Intent A."
    }}
}}
"""
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    return prompt