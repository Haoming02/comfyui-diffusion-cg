# ComfyUI Diffusion Color Grading
This is a Custom Node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI), which performs "Color Grading" during the generation, producing a more **neutral** and **balanced**, but also **vibrant** and **contrasty** color.

> For more information, check out the original [Extension](https://github.com/Haoming02/sd-webui-diffusion-cg) for **Automatic1111** Webui

## How to Use
- Attach the **Diffusion CG** node between `Empty Latent` and `KSampler` nodes
- Adjust the **recenter** and **normalization** sliders as needed

> [!Important]
> The effects are "global." If you want to disable it during other parts of the workflow *(**e.g.** during `Hires. Fix`)*, you can add the **Disable CG** node to reset the parameters back to `0.0`

## Examples

<p align="center">
<img src="examples/off.jpg" width=384>
<img src="examples/on.png" width=384>
<br><code>Off | On</code>
</p>

> [!Tip]
> The `on.png` contains Workflow

## Known Issue
- Does not work with certain Samplers
