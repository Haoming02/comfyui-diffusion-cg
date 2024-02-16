from .normalization import Normalization, NormalizationXL
from .recenter import Recenter, RecenterXL

NODE_CLASS_MAPPINGS = {
    "Normalization": Normalization,
    "NormalizationXL": NormalizationXL,
    "Recenter": Recenter,
    "Recenter XL": RecenterXL
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Normalization": "Normalization",
    "NormalizationXL": "NormalizationXL",
    "Recenter": "Recenter",
    "Recenter XL": "RecenterXL"
}
