from engine.flow.executor.transform_code_llm import transformation_code_llm

def transform_code(plan_steps,next_step_reply, user_id, ch_id):
    if next_step_reply.get("extracted_arguments", {}).get("required_arguments", {}) == {}:
        return next_step_reply
    for arg_name, arg_info in next_step_reply["extracted_arguments"]["required_arguments"].items():
        if arg_info["method"] == "code":
            arg_value = arg_info["value"]
            arg_source = arg_info["source"]
            source_value = next(step for step in plan_steps if step["step"] == arg_source)["tool_executed_result"]
            print(source_value)
            print(arg_value)
            code = transformation_code_llm(source_value, arg_value, user_id, ch_id)
            print(f"code: {code}")
            next_step_reply["extracted_arguments"]["required_arguments"][arg_name]["method"] = {"method_parameter": code}

    return next_step_reply
