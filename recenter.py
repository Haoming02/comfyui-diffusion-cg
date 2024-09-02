from functools import wraps
import datetime
import comfy
import torch

RECENTER: float = 0.0
LUTS: list[float] = None


def disable_recenter():
    global RECENTER
    RECENTER = 0.0
    global LUTS
    LUTS = None


ORIGINAL_SAMPLE = comfy.sample.sample
ORIGINAL_SAMPLE_CUSTOM = comfy.sample.sample_custom


def hijack(SAMPLE):

    @wraps(SAMPLE)
    def sample_center(*args, **kwargs):
        original_callback = kwargs["callback"]

        @torch.inference_mode()
        @wraps(original_callback)
        def hijack_callback(step, x0, x, total_steps):

            if (not RECENTER) or (not LUTS):
                return original_callback(step, x0, x, total_steps)

            X = x.detach().clone()
            batchSize: int = X.size(0)
            channels: int = len(LUTS)

            for b in range(batchSize):
                for c in range(channels):
                    x[b][c] += (LUTS[c] - X[b][c].mean()) * RECENTER

            return original_callback(step, x0, x, total_steps)

        kwargs["callback"] = hijack_callback
        return SAMPLE(*args, **kwargs)

    return sample_center


comfy.sample.sample = hijack(ORIGINAL_SAMPLE)
comfy.sample.sample_custom = hijack(ORIGINAL_SAMPLE_CUSTOM)


class Recenter:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT",),
                "strength": (
                    "FLOAT",
                    {"default": 0.00, "min": 0.00, "max": 1.00, "step": 0.05},
                ),
                "C": (
                    "FLOAT",
                    {"default": 0.00, "min": -1.00, "max": 1.00, "step": 0.05},
                ),
                "M": (
                    "FLOAT",
                    {"default": 0.00, "min": -1.00, "max": 1.00, "step": 0.05},
                ),
                "Y": (
                    "FLOAT",
                    {"default": 0.00, "min": -1.00, "max": 1.00, "step": 0.05},
                ),
                "K": (
                    "FLOAT",
                    {"default": 0.00, "min": -1.00, "max": 1.00, "step": 0.05},
                ),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "hook"
    CATEGORY = "latent"

    def hook(self, latent, strength: float, C: float, M: float, Y: float, K: float):
        global RECENTER
        RECENTER = strength
        global LUTS
        LUTS = [-K, -M, C, Y]

        return (latent,)

    @classmethod
    def IS_CHANGED(*args, **kwargs):
        return str(datetime.datetime.now())


class RecenterXL:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT",),
                "strength": (
                    "FLOAT",
                    {"default": 0.00, "min": 0.00, "max": 1.00, "step": 0.05},
                ),
                "Y": (
                    "FLOAT",
                    {"default": 0.00, "min": -1.00, "max": 1.00, "step": 0.05},
                ),
                "Cb": (
                    "FLOAT",
                    {"default": 0.00, "min": -1.00, "max": 1.00, "step": 0.05},
                ),
                "Cr": (
                    "FLOAT",
                    {"default": 0.00, "min": -1.00, "max": 1.00, "step": 0.05},
                ),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "hook"
    CATEGORY = "latent"

    def hook(self, latent, strength: float, Y: float, Cb: float, Cr: float):
        global RECENTER
        RECENTER = strength
        global LUTS
        LUTS = [Y, -Cr, -Cb]

        return (latent,)

    @classmethod
    def IS_CHANGED(*args, **kwargs):
        return str(datetime.datetime.now())
