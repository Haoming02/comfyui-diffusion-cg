import comfy
import latent_preview

rc_strength = 0.0
LUTs = []

ORIGINAL_SAMPLE = comfy.sample.sample
ORIGINAL_SAMPLE_CUSTOM = comfy.sample.sample_custom

def hijack(SAMPLE):

    def sample_center(*args, **kwargs):
        original_callback = kwargs['callback']

        def hijack_callback(step, x0, x, total_steps):
            global rc_strength
            global LUTs

            if rc_strength == 0 or len(LUTs) == 0:
                return original_callback(step, x0, x, total_steps)

            batchSize = x.size(0)
            for b in range(batchSize):
                for c in range(len(LUTs)):
                    x[b][c] += (LUTs[c] - x[b][c].mean()) * rc_strength

            return original_callback(step, x0, x, total_steps)

        kwargs['callback'] = hijack_callback
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
                "strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0,
                                "step": 0.1, "round": 0.1, "display": "slider"}),
                "C": ("FLOAT", {"default": 0.01, "min": -1.00, "max": 1.00, "step": 0.01}),
                "M": ("FLOAT", {"default": 0.50, "min": -1.00, "max": 1.00, "step": 0.01}),
                "Y": ("FLOAT", {"default": -0.13, "min": -1.00, "max": 1.00, "step": 0.01}),
                "K": ("FLOAT", {"default": 0.00, "min": -1.00, "max": 1.00, "step": 0.01})
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "hook"
    CATEGORY = "latent"

    def hook(self, latent, strength, C, M, Y, K):
        global rc_strength
        rc_strength = strength
        global LUTs
        LUTs = [-K, -M, C, Y]

        return (latent,)


class RecenterXL:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT",),
                "strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0,
                                "step": 0.1, "round": 0.1, "display": "slider"}),
                "L": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05}),
                "a": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05}),
                "b": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05})
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "hook"
    CATEGORY = "latent"

    def hook(self, latent, strength, L, a, b):
        global rc_strength
        rc_strength = strength
        global LUTs
        LUTs = [L, -a, b]

        return (latent,)


def prepare_callback(orig_callback, LUTs):
    def callback(step, x0, x, total_steps):
        batchSize = x.size(0)
        for b in range(batchSize):
            for c in range(len(LUTs)):
                x[b][c] += (LUTs[c] - x[b][c].mean()) * rc_strength
            return orig_callback(step, x0, x, total_steps)
    return callback

class RecenteringKSampler:
    """
    This class is based upon ComfyUI's KSampler and common_ksampler.
    Copyright (C) 2023  comfyanonymous

    ComfyUI's KSampler and common_ksampler are free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ComfyUI's KSampler and common_ksampler are distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ComfyUI's KSampler and common_ksampler.  If not, see <https://www.gnu.org/licenses/>.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"model": ("MODEL",),
                    "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                    "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                    "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0, "step":0.1, "round": 0.01}),
                    "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
                    "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
                    "positive": ("CONDITIONING", ),
                    "negative": ("CONDITIONING", ),
                    "latent": ("LATENT", ),
                    "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                    "strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0,
                                "step": 0.1, "round": 0.1, "display": "slider"}),
                    "C": ("FLOAT", {"default": 0.01, "min": -1.00, "max": 1.00, "step": 0.01}),
                    "M": ("FLOAT", {"default": 0.50, "min": -1.00, "max": 1.00, "step": 0.01}),
                    "Y": ("FLOAT", {"default": -0.13, "min": -1.00, "max": 1.00, "step": 0.01}),
                    "K": ("FLOAT", {"default": 0.00, "min": -1.00, "max": 1.00, "step": 0.01})
                    }
                }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "sample"

    CATEGORY = "sampling"

    def sample(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent, denoise=1.0, strength=0.0, C=0.01, M=0.5, Y=-0.13, K=0.0):
        latent_image = latent["samples"]
       
        batch_inds = latent["batch_index"] if "batch_index" in latent else None
        noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)

        noise_mask = None
        if "noise_mask" in latent:
            noise_mask = latent["noise_mask"]

        callback = latent_preview.prepare_callback(model, steps)

        LUTs = [-K, -M, C, Y]
        
        if strength > 0:
            callback = prepare_callback(callback, LUTs)
        
        disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED
        samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                    denoise=denoise, disable_noise=False, start_step=None, last_step=None,
                                    force_full_denoise=False, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
        out = latent.copy()
        out["samples"] = samples
        return (out, )
    
class RecenteringXLKSampler:
    """
    This class is based upon ComfyUI's KSampler and common_ksampler.
    Copyright (C) 2023  comfyanonymous

    ComfyUI's KSampler and common_ksampler are free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ComfyUI's KSampler and common_ksampler are distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ComfyUI's KSampler and common_ksampler.  If not, see <https://www.gnu.org/licenses/>.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"model": ("MODEL",),
                    "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                    "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                    "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0, "step":0.1, "round": 0.01}),
                    "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
                    "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
                    "positive": ("CONDITIONING", ),
                    "negative": ("CONDITIONING", ),
                    "latent": ("LATENT", ),
                    "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                    "strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0,
                                "step": 0.1, "round": 0.1, "display": "slider"}),
                    "L": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05}),
                    "a": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05}),
                    "b": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05})                   
                    }
                }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "sample"

    CATEGORY = "sampling"

    def sample(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent, denoise=1.0, strength=0.0, L=0.0, a=0.0, b=-0.0):
        latent_image = latent["samples"]
       
        batch_inds = latent["batch_index"] if "batch_index" in latent else None
        noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)

        noise_mask = None
        if "noise_mask" in latent:
            noise_mask = latent["noise_mask"]

        callback = latent_preview.prepare_callback(model, steps)

        LUTs = [L, -a, b]
        
        if strength > 0:
            callback = prepare_callback(callback, LUTs)
        
        disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED
        samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                    denoise=denoise, disable_noise=False, start_step=None, last_step=None,
                                    force_full_denoise=False, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
        out = latent.copy()
        out["samples"] = samples
        return (out, )