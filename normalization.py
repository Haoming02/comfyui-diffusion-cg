import torch

DYNAMIC_RANGE: float = 1.0 / 0.18215 / 0.13025


def normalize_tensor(x: torch.Tensor, r: float) -> torch.Tensor:
    ratio = r / max(abs(float(x.min())), abs(float(x.max())))
    return x * max(ratio, 1.0)


def clone_latent(latent: dict) -> dict:
    return {"samples": latent["samples"].detach().clone()}


class Normalization:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent": ("LATENT",),
                "sdxl": ("BOOLEAN",),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "normalize"
    CATEGORY = "latent"

    @torch.inference_mode()
    def normalize(self, latent: dict, sdxl: bool):
        norm_latent = clone_latent(latent)

        batchSize: int = latent["samples"].size(0)
        channels: int = 3 if sdxl else 4

        for b in range(batchSize):
            for c in range(channels):
                norm_latent["samples"][b][c] = normalize_tensor(
                    norm_latent["samples"][b][c], DYNAMIC_RANGE / 2.5
                )

        return (norm_latent,)
