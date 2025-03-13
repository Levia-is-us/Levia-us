success_output_schema = {
    "type": "object",
    "required": ["status", "plan"],
    "properties": {
        "status": {"type": "string", "enum": ["success"]},
        "plan": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "step",
                    "tool",
                    "data",
                    "step purpose",
                    "description",
                ],
                "properties": {
                    "step": {"type": "string", "pattern": "^step [0-9]+"},
                    "tool": {"type": "string"},
                    "data": {
                        "type": "object",
                        "required": ["method", "inputs", "output"],
                        "properties": {
                            "method": {"type": "string"},
                            "inputs": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": [
                                        "name",
                                        "type",
                                        "required",
                                        "description",
                                        "source",
                                        "method",
                                    ],
                                    "properties": {
                                        "name": {"type": "string"},
                                        "type": {"type": "string"},
                                        "required": {"type": "boolean"},
                                        "description": {"type": "string"},
                                        "source": {"type": "string"},
                                        "method": {"type": "string"},
                                        "value": {
                                            "type": [
                                                "string",
                                                "array",
                                                "object",
                                                "number",
                                                "boolean",
                                                "null",
                                            ]
                                        },
                                    },
                                    "additionalProperties": False,
                                },
                            },
                            "output": {
                                "type": "object",
                                "required": ["description", "type"],
                                "properties": {
                                    "description": {"type": "string"},
                                    "type": {"type": "string"},
                                },
                            },
                        },
                        "additionalProperties": False,
                    },
                    "step purpose": {"type": "string"},
                    "description": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
}

missing_input_schema = {
    "type": "object",
    "required": ["status", "name"],
    "properties": {
        "status": {"type": "string", "enum": ["missing input"]},
        "name": {"type": "array", "items": {"type": "string"}},
    },
    "additionalProperties": False,
}

failed_output_schema = {
    "type": "object",
    "required": ["status", "reason"],
    "properties": {
        "status": {"type": "string", "enum": ["failed"]},
        "reason": {
            "type": "string",
            "description": "Explanation for why the plan failed or cannot be executed",
        },
    },
    "additionalProperties": False,
}
