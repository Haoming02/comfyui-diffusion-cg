# ComfyUI Diffusion Color Grading
This is an Extension for [ComfyUI](https://github.com/comfyanonymous/ComfyUI), which is the joint research between me and <ins>TimothyAlexisVass</ins>.
For more information, check out the original [Extension](https://github.com/Haoming02/sd-webui-diffusion-cg) for **Automatic1111**.

## Nodes
Some example workflows are included~

- **Hook Recenter:** For **SD 1.5**. Hooks the callback to achieve the centering effect.
  - Comes with `Effect Strength` slider and `CMYK` color settings
- **Hook Recenter XL:** For **SDXL**. Hooks the callback to achieve the centering effect.
  - Comes with `Effect Strength` slider and `Lab` color settings
- **Unhook Recenter** (Optional)**:** Unhook the callback to disable the effects completely.
  - If used, put near the end of the workflow
- **Normalization:** For **SD 1.5**. Use before the `VAE Decode` node to achieve the normalization effect.
- **NormalizationXL:** For **SDXL**. Use before the `VAE Decode` node to achieve the normalization effect.

#### Important:
- Toggle `custom_sampler` if you're using the **SamplerCustom** node.
- In a single workflow, you only need to hook the callback once. The simplest way is to add it between the `Positive Prompt` and the `Sampler`.
- Due to how `ComfyUI` works, if you also add **Unhook Recenter**, the effect may not work sometimes unless you also change the prompt.

> ComfyUI doesn't go through a node unless it needs to be updated, so if you unhook the callback and the parameters didn't change *(**eg.** you're only iterating throguh seeds)*, then the callback will not be hooked again. Easiest way to solve this is just adding a space to the positive prompt, or just don't unhook the callback.

## Samples

<p align="center">
<b>SD 1.5</b><br>
<img src="samples\1.5_off.jpg" width=384>
<img src="workflows\1.5_on.png" width=384>
<br><code>Off | On</code><br>
</p>

<p align="center">
<b>SDXL</b><br>
<img src="samples\xl_off.jpg" width=384>
<img src="workflows\xl_on.png" width=384>
<br><code>Off | On</code><br>
</p>

## Known Issue
- Doesn't really work with `LCM` Sampler

<hr>

##### Checkpoints Used:
- [UHD-23](https://civitai.com/models/22371/uhd-23)
- [Juggernaut XL](https://civitai.com/models/133005/juggernaut-xl)
