from functools import wraps

import execution

from .normalization import Normalization
from .recenter import Recenter, RecenterXL, disable_recenter

NODE_CLASS_MAPPINGS = {
    "Normalization": Normalization,
    "Recenter": Recenter,
    "Recenter XL": RecenterXL,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Normalization": "Normalization",
    "Recenter": "Recenter",
    "Recenter XL": "RecenterXL",
}


def find_node(prompt: dict) -> bool:
    """Find any ReCenter Node"""

    for node in prompt.values():
        if node.get("class_type", None) in ("Recenter", "Recenter XL"):
            return True

    return False


original_validate = execution.validate_prompt


@wraps(original_validate)
async def hijack_validate(*args):
    for arg in args:
        if isinstance(arg, dict):
            prompt = arg
            break

    if not find_node(prompt):
        disable_recenter()

    return await original_validate(*args)


execution.validate_prompt = hijack_validate
