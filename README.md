# ComfyUI Diffusion Color Grading
This is an Extension for [ComfyUI](https://github.com/comfyanonymous/ComfyUI), which is the joint research between me and <ins>TimothyAlexisVass</ins>.

For more information, check out the original [Extension](https://github.com/Haoming02/sd-webui-diffusion-cg) for **Automatic1111** Webui.

## How to Use
> An example workflow is included~

- Attach the **Recenter** or **RecenterXL** node between `Empty Latent` and `KSampler` nodes
    - Adjust the **strength** and **color** sliders as needed
- Attach the **Normalization** node between `KSampler` and `VAE Decode` nodes

### Important:
- The **Recenter** effect is "global." If you want to disable it during other parts of the workflow *(**eg.** during `Hires. Fix`)*, you have to add another **Recenter** node with its `strength` set to `0.0`.

## Examples

<p align="center">
<img src="examples/off.jpg" width=384>
<img src="examples/on.png" width=384><br>
<code>Off | On</code>
</p>

## Known Issue
- Does not work with certain Samplers
