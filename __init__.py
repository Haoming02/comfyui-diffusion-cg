from .normalization import Normalization, NormalizationXL
from .recenter import Recenter, RecenterXL, RecenteringKSampler, RecenteringXLKSampler

NODE_CLASS_MAPPINGS = {
    "Normalization": Normalization,
    "NormalizationXL": NormalizationXL,
    "Recenter": Recenter,
    "Recenter XL": RecenterXL,
    "RecenteringKSampler": RecenteringKSampler,
    "RecenteringXLKSampler": RecenteringXLKSampler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Normalization": "Normalization",
    "NormalizationXL": "NormalizationXL",
    "Recenter": "Recenter",
    "Recenter XL": "RecenterXL",
    "RecenteringKSampler": "RecenteringKSampler",
    "RecenteringXLKSampler": "RecenteringXLKSampler"
}
