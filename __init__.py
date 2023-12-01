from .normalization import Normalization, NormalizationXL
from .recenter import CKSampler
from .recenter_xl import CKSamplerXL
from .tensor_debug import Debug

NODE_CLASS_MAPPINGS = {
    "Tensor Debug": Debug,
    "Normalization": Normalization,
    "NormalizationXL": NormalizationXL,
    "Center Sampler": CKSampler,
    "Center Sampler XL": CKSamplerXL
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Tensor Debug": "Tensor Debug",
    "Normalization": "Normalization",
    "NormalizationXL": "NormalizationXL",
    "Center Sampler": "KSampler (Recenter)",
    "Center Sampler XL": "KSampler XL (Recenter)"
}
