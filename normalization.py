DYNAMIC_RANGE = [18, 14, 14, 14]
DYNAMIC_RANGE_XL = [20, 16, 16]

def normalize_tensor(x, r):
    ratio = r / max(abs(float(x.min())), abs(float(x.max())))
    x *= max(ratio, 0.99)

    return x

class Normalization:
    @classmethod
    def INPUT_TYPES(s):
        return { "required": { "latent": ("LATENT",) } }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "normalize"
    CATEGORY = "latent"

    def normalize(self, latent):
        batches = latent['samples'].size(0)
        for b in range(batches):
            for c in range(4):
                latent['samples'][b][c] = normalize_tensor(latent['samples'][b][c], DYNAMIC_RANGE[c])

        return (latent,)

class NormalizationXL:
    @classmethod
    def INPUT_TYPES(s):
        return { "required": { "latent": ("LATENT",) } }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "normalize"
    CATEGORY = "latent"

    def normalize(self, latent):
        batches = latent['samples'].size(0)
        for b in range(batches):
            for c in range(3):
                latent['samples'][b][c] = normalize_tensor(latent['samples'][b][c], DYNAMIC_RANGE_XL[c])

        return (latent,)
