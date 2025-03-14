planner_output_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["step", "tool", "intent", "description", "reason"],
        "properties": {
            "step": {
                "type": "string",
                "pattern": "^step [0-9]+$",
                "description": "A numbered step indicator (e.g., 'step 1', 'step 2')"
            },
            "tool": {
                "type": "string",
                "description": "The specific external tool or resource required for this step"
            },
            "intent": {
                "type": "string",
                "description": "A brief description of the purpose of this step"
            },
            "description": {
                "type": "string",
                "description": "A general overview of the objective to be achieved by this tool"
            },
            "reason": {
                "type": "string",
                "description": "An explanation of why this step is necessary and requires the specified tool"
            }
        },
        "additionalProperties": False
    },
    "minItems": 1
}