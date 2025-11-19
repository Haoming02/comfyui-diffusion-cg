from functools import wraps

import execution

from .nodes import DiffusionCG, DisableCG, disable_all

NODE_CLASS_MAPPINGS = {
    "Diffusion CG": DiffusionCG,
    "Disable CG": DisableCG,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Diffusion CG": "Diffusion CG",
    "Disable CG": "Disable CG",
}


def find_node(prompt: dict) -> bool:
    return any(
        node.get("class_type", None) == "Diffusion CG" for node in prompt.values()
    )


original_validate = execution.validate_prompt


@wraps(original_validate)
async def hijack_validate(*args):
    for arg in args:
        if isinstance(arg, dict):
            prompt = arg
            break

    if not find_node(prompt):
        disable_all()

    return await original_validate(*args)


execution.validate_prompt = hijack_validate
