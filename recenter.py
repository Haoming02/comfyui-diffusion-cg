import comfy

ORIGINAL_SAMPLE = comfy.sample.sample
ORIGINAL_SAMPLE_CUSTOM = comfy.sample.sample_custom


def hijack(SAMPLE, LUTs:list, strength:float):

    def sample_center(*args, **kwargs):
        original_callback = kwargs['callback']

        def hijack_callback(step, x0, x, total_steps):

            batchSize = x.size(0)
            for b in range(batchSize):
                for c in range(len(LUTs)):
                    x[b][c] += (LUTs[c] - x[b][c].mean()) * strength

            return original_callback(step, x0, x, total_steps)

        kwargs['callback'] = hijack_callback
        return SAMPLE(*args, **kwargs)

    return sample_center


class UnhookCallback:
    @classmethod
    def INPUT_TYPES(s):
        return { "required": { "latent": ("LATENT", ) } }

    RETURN_TYPES = ("LATENT", )
    FUNCTION = "unhook"
    CATEGORY = "Diffusion CG"

    def unhook(self, latent):
        comfy.sample.sample_custom = ORIGINAL_SAMPLE_CUSTOM
        comfy.sample.sample = ORIGINAL_SAMPLE

        return (latent,)


class HookCallback:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("CONDITIONING",),
                "custom_sampler": ("BOOLEAN", {"default": False}),
                "strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0,
                                "step": 0.1, "round": 0.1, "display": "slider"}),
                "C": ("FLOAT", {"default": 0.01, "min": -1.00, "max": 1.00, "step": 0.01}),
                "M": ("FLOAT", {"default": 0.51, "min": -1.00, "max": 1.00, "step": 0.01}),
                "Y": ("FLOAT", {"default": -0.12, "min": -1.00, "max": 1.00, "step": 0.01}),
                "K": ("FLOAT", {"default": 0.00, "min": -1.00, "max": 1.00, "step": 0.01})
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "hook"
    CATEGORY = "Diffusion CG"

    def hook(self, prompt, custom_sampler, strength, C, M, Y, K):
        if custom_sampler:
            comfy.sample.sample_custom = hijack(ORIGINAL_SAMPLE_CUSTOM, [-K, -M, C, Y], strength)
        else:
            comfy.sample.sample = hijack(ORIGINAL_SAMPLE, [-K, -M, C, Y], strength)

        return (prompt,)


class HookCallbackXL:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("CONDITIONING",),
                "custom_sampler": ("BOOLEAN", {"default": False}),
                "strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0,
                                "step": 0.1, "round": 0.1, "display": "slider"}),
                "L": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05}),
                "a": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05}),
                "b": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.05})
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "hook"
    CATEGORY = "Diffusion CG"

    def hook(self, prompt, custom_sampler, strength, L, a, b):
        if custom_sampler:
            comfy.sample.sample_custom = hijack(ORIGINAL_SAMPLE_CUSTOM, [L, -a, b], strength)
        else:
            comfy.sample.sample = hijack(ORIGINAL_SAMPLE, [L, -a, b], strength)

        return (prompt,)
