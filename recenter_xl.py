import latent_preview
import comfy
import torch

def center_ksampler(LUTs, strength, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent, denoise=1.0, disable_noise=False, start_step=None, last_step=None, force_full_denoise=False):
    latent_image = latent["samples"]

    if disable_noise:
        noise = torch.zeros(latent_image.size(), dtype=latent_image.dtype, layout=latent_image.layout, device="cpu")
    else:
        batch_inds = latent["batch_index"] if "batch_index" in latent else None
        noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)

    noise_mask = None
    if "noise_mask" in latent:
        noise_mask = latent["noise_mask"]

    original_callback = latent_preview.prepare_callback(model, steps)

    def hijack_callback(step, x0, x, total_steps):

        batches = x.size(0)

        for b in range(batches):
            for c in range(3):
                x[b][c] += (LUTs[c] - x[b][c].mean()) * strength

        return original_callback(step, x0, x, total_steps)

    disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=hijack_callback, disable_pbar=disable_pbar, seed=seed)

    out = latent.copy()
    out["samples"] = samples
    return (out,)

class CKSamplerXL:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0, "step":0.1, "round": 0.01}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
                "positive": ("CONDITIONING", ),
                "negative": ("CONDITIONING", ),
                "latent_image": ("LATENT", ),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.1,
                                        "round": 0.1, "display": "slider"}),
                "L": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05, "round": False}),
                "a": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05, "round": False}),
                "b": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05, "round": False})
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "sample"
    CATEGORY = "sampling"

    def sample(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise, strength, L, a, b):
        return center_ksampler([L, -a, b], strength, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)
