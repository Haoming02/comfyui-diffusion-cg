from .normalization import Normalization, NormalizationXL
from .recenter import Recenter, RecenterXL, reset_str
import execution

NODE_CLASS_MAPPINGS = {
    "Normalization": Normalization,
    "NormalizationXL": NormalizationXL,
    "Recenter": Recenter,
    "Recenter XL": RecenterXL,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Normalization": "Normalization",
    "NormalizationXL": "NormalizationXL",
    "Recenter": "Recenter",
    "Recenter XL": "RecenterXL",
}


def find_node(prompt: dict) -> bool:
    """Find any ReCenter Node"""

    for k, v in prompt.items():
        if v["class_type"] in ("Recenter", "Recenter XL"):
            return True

    return False


original_validate = execution.validate_prompt


def hijack_validate(prompt):

    if not find_node(prompt):
        reset_str()

    return original_validate(prompt)


execution.validate_prompt = hijack_validate
