import comfy

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
