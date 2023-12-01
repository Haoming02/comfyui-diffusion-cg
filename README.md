# ComfyUI Diffusion Color Grading
<h4 align = "right"><i>Beta</i></h4>

This is the ComfyUI port of the joint research between me and <ins>TimothyAlexisVass</ins>.
For more information, check out the original [Extension](https://github.com/Haoming02/sd-webui-diffusion-cg) for **Automatic1111**.

## Nodes
Some example workflows are included~

#### Sampling
- **KSampler (Recenter):** For **SD 1.5**. Use this instead of the normal `KSampler` node to achieve the centering effect.
  - Comes with `Effect Strength` slider and `CMYK` color settings
- **KSampler XL (Recenter):** For **SDXL**. Use this instead of the normal `KSampler` node to achieve the centering effect.
  - Comes with `Effect Strength` slider and `Lab` color settings

#### Latent
- **Normalization:** For **SD 1.5**. Use before the `VAE Decode` to achieve the normalization effect.
- **NormalizationXL:** For **SDXL**. Use before the `VAE Decode` to achieve the normalization effect.
- **Tensor Debug:** *For development only...*

## Samples

<p align="center">
<b>SD 1.5</b><br>
<img src="samples\1.5_off.jpg" width=256>
<img src="samples\1.5_on.jpg" width=256>
<br><code>Off | On</code><br>
</p>

<p align="center">
<b>SDXL</b><br>
<img src="samples\xl_off.jpg" width=384>
<img src="samples\xl_on.jpg" width=384>
<br><code>Off | On</code><br>
</p>

<hr>

##### Checkpoints Used:
- [UHD-23](https://civitai.com/models/22371/uhd-23)
- [SDXL Base 1.0 w/ 0.9 VAE](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/tree/main)
