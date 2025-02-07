check_plan_fittable_prompt = """
                    You are an expert in natural language understanding and semantic analysis. Your task is to compare two intents or evaluate whether a proposed solution fulfills a given intent.

                    Input:

                    1. Intent A/Requirement Description: {Intent A/Requirement Description}
                    2. Intent B and Proposed Solution: {Intent B/Proposed Solution}
                    Analyze the relationship between the two inputs and output your findings in the following structured JSON format:
                    {
                    "intent_match": {
                        "result": true/false,
                        "reason": "Brief explanation of whether Intent A and Intent B match or not."
                    }
                    "solution_sufficient": {
                        "result": true/false,
                        "reason": "Brief explanation of whether the proposed solution satisfies Intent A."
                    }
                    }          
                    """
