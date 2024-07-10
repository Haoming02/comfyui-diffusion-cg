# ComfyUI Diffusion Color Grading
This is an Extension for [ComfyUI](https://github.com/comfyanonymous/ComfyUI), which is the joint research between me and <ins>TimothyAlexisVass</ins>.

For more information, check out the original [Extension](https://github.com/Haoming02/sd-webui-diffusion-cg) for **Automatic1111**.

## How to Use
> Example workflows are included~

- Attach the **Recenter** or **RecenterXL** node between `Empty Latent` and `KSampler` nodes
    - Adjust the **strength** and **color** sliders as needed
- Attach the **Normalization** or **NormalizationXL** node between `KSampler` and `VAE Decode` nodes

### Important:
- The **Recenter** is "global." If you want to disable it during later part of the workflow *(**eg.** during `Hires. Fix`)*, you have to add another **Recenter** node and set its `strength` to `0.0`.

## Examples

<p align="center">
<b>SD 1.5</b><br>
<img src="examples/1.5_off.jpg" width=384>
<img src="examples/1.5_on.png" width=384>
<br><code>Off | On</code>
</p>

<p align="center">
<b>SDXL</b><br>
<img src="examples/xl_off.jpg" width=384>
<img src="examples/xl_on.png" width=384>
<br><code>Off | On</code>
</p>

## Known Issue
- Doesn't work with some of the Samplers
