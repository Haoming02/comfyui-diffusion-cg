from functools import wraps
from math import pi, sin
from typing import Callable

import torch

import latent_preview

RECENTER: float = 0.0
NORMALIZATION: float = 0.0


def disable_all():
    global RECENTER
    RECENTER = 0.0
    global NORMALIZATION
    NORMALIZATION = 0.0


_prepare_callback: Callable = latent_preview.prepare_callback


@wraps(_prepare_callback)
def hijack_prepare(*args, **kwargs):
    original_callback: Callable = _prepare_callback(*args, **kwargs)

    @torch.inference_mode()
    @wraps(original_callback)
    def hijack_callback(step, x0, x, total_steps):
        original_callback(step, x0, x, total_steps)

        ratio: float = step / total_steps
        strength: float = 1.0 - sin(ratio * pi / 2.0)
        latent: torch.Tensor = x0.detach().clone()

        batches: int = latent.shape[0]
        channels: int = latent.shape[1]

        for b in range(batches):
            _std: float = latent[b].std()

            for c in range(channels):
                bias: float = latent[b][c].std() / _std * strength
                x0[b][c] += (0.0 - latent[b][c].mean()) * bias * RECENTER

                magnitude = float(latent[b][c].max() - latent[b][c].min())
                factor = 1.0 / 0.13025
                scale = max(factor / magnitude - 1.0, 0.0)
                x0[b][c] *= scale * NORMALIZATION * strength + 1.0

    return hijack_callback


latent_preview.prepare_callback = hijack_prepare


class DiffusionCG:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT",),
                "recenter": (
                    "FLOAT",
                    {"default": 0.00, "min": 0.00, "max": 1.00, "step": 0.05},
                ),
                "normalization": (
                    "FLOAT",
                    {"default": 0.00, "min": 0.00, "max": 1.00, "step": 0.05},
                ),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "hook"
    CATEGORY = "sampling"

    def hook(self, latent, recenter: float, normalization: float):
        global RECENTER
        RECENTER = recenter
        global NORMALIZATION
        NORMALIZATION = normalization
        return (latent,)


class DisableCG:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT",),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "hook"
    CATEGORY = "sampling"

    def hook(self, latent):
        disable_all()
        return (latent,)
