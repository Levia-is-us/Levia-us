tools_description = "[{\"tool\":\"get_current_location_tool\", \"method\": \"get_current_location\", \"desc\":\"Tool for getting location information\"},"
tools_description += "{\"tool\":\"send_tweet_tool\", \"method\": \"send_tweet\", \"desc\":\"Tool for post content on twitter\", \"arguments\": [\"tweet\", \"username\", \"password\"]},"
tools_description += "{\"tool\":\"website_scraper_tool\", \"method\": \"website_scraper\", \"desc\":\"Tool for scraping website\"}]"

system_message = f"""You are a helpful assistant with access to these tools: 

                            {tools_description}
                            Choose the appropriate tool based on the current step. If no tool is needed, reply directly.
                            
                            IMPORTANT: When you need to use a tool, you must ONLY respond with the exact JSON object format below, nothing else:
                            {{
                                "tool": "tool-name",
                                "method": "method-name",
                                "desc": "description of the tool execution",
                                "arguments": {{
                                    "argument-name": "value"
                                }}
                            }}
                            
                            After receiving a tool's response:
                            1. Transform the raw data into a natural, conversational response
                            2. Keep responses concise but informative
                            3. Focus on the most relevant information
                            4. Use appropriate context from the user's question
                            5. Avoid simply repeating the raw data
                            
                            Please use only the tools that are explicitly defined above."""

system_messagev2 = f"""You are a helpful assistant with access to these tools: 

                            {tools_description}
                            Choose the appropriate tool based on current step.

                            IMPORTANT: you must ONLY respond with the exact JSON object format below, nothing else:
                            {{
                                "tool": "tool-name",
                                "method": "method-name",
                                "desc": "description of the tool execution",
                                "arguments": {{
                                    "argument-name": "value"
                                }}
                            }}
                            If no such tool can be used to solve current step, output nothing.

                            Please use only the tools that are explicitly defined above."""

intents_system_prompt = f"""
                        When the user inputs a sentence, respond in the following JSON format:

                        1. If the input is a question or request that can be solved directly by a large language model, output:
                        {{
                            "type": "direct_answer",
                            "response": "[Your answer here]"
                        }}
                            make sure the response does not directly answer can not solve the problem.
                        2. If the input is a question or request that cannot be directly answered or fulfilled by a large language model (e.g., requires physical action, purchasing items, or actions beyond the model's capabilities), output a summary as short as possible:
                        {{
                            "type": "intent_summary",
                            "summary": "[Summarize the user's intent or goal here]"
                        }}
                        Ensure all responses strictly follow this JSON structure for consistent processing.
                    """

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

messages = []