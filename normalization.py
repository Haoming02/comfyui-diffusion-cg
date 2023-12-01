DYNAMIC_RANGE = [19.75, 14.275, 14.275, 14.275]
DYNAMIC_RANGE_XL = [27.62, 19.96, 19.96]

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
                xmin = abs(float(latent['samples'][b][c].min()))
                xmax = abs(float(latent['samples'][b][c].max()))

                r = DYNAMIC_RANGE[c] / max(xmin, xmax)
                ratio = max(0.95, r)

                latent['samples'][b][c] *= ratio

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
                xmin = abs(float(latent['samples'][b][c].min()))
                xmax = abs(float(latent['samples'][b][c].max()))

                r = DYNAMIC_RANGE_XL[c] / max(xmin, xmax)
                ratio = max(0.95, r)

                latent['samples'][b][c] *= ratio

        return (latent,)
