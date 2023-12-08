from .normalization import Normalization, NormalizationXL
from .recenter import HookCallback, HookCallbackXL, UnhookCallback
# from .tensor_debug import Debug

NODE_CLASS_MAPPINGS = {
    "Normalization": Normalization,
    "NormalizationXL": NormalizationXL,
    "Hook Recenter": HookCallback,
    "Hook Recenter XL": HookCallbackXL,
    "Unhook Recenter": UnhookCallback,
  # "Tensor Debug": Debug,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Normalization": "Normalization",
    "NormalizationXL": "NormalizationXL",
    "Hook Recenter": "Hook Recenter",
    "Hook Recenter XL": "Hook Recenter XL",
    "Unhook Recenter": "Unhook Recenter",
  # "Tensor Debug": "Tensor Debug",
}
