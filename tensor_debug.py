class Debug:
    @classmethod
    def INPUT_TYPES(s):
        return { "required": { "latent": ("LATENT",) } }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "debug"
    CATEGORY = "latent"

    def debug(self, latent):

        print('\n')
        for c in range(4):
            print(f'(min: {latent["samples"][0][c].min()}, max: {latent["samples"][0][c].max()}, mean: {latent["samples"][0][c].mean()})')
        print('\n')

        return (latent,)
