# Stable Diffusion with OpenVINO

Implementation of Text-To-Image generation using Stable Diffusion on Intel CPU or GPU.
https://github.com/TVR28/Computer-Vision/blob/main/OpenVino-StableDiffusion/data/title.png?raw=true

## Requirements

- Operating Systems: Linux, Windows, MacOS
- Python version: <= 3.9.0
- A CPU or GPU compatible with OpenVINO.

## Installation

1. Set up and update PIP to the highest version:
    ```bash
    python -m pip install --upgrade pip
    ```

2. Install OpenVINO™ Development Tools 2022.3.0 release with PyPI:
    ```bash
    pip install openvino-dev[onnx,pytorch]==2022.3.0
    ```

3. Install additional requirements:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Generate image from text description using the `demo.py` script:

``` 
usage: demo.py [-h] [--model MODEL] [--device DEVICE] [--seed SEED] [--beta-start BETA_START] [--beta-end BETA_END] [--beta-schedule BETA_SCHEDULE]
[--num-inference-steps NUM_INFERENCE_STEPS] [--guidance-scale GUIDANCE_SCALE] [--eta ETA] [--tokenizer TOKENIZER] [--prompt PROMPT]
[--params-from PARAMS_FROM] [--init-image INIT_IMAGE] [--strength STRENGTH] [--mask MASK] [--output OUTPUT]

optional arguments:
-h, --help show this help message and exit
--model MODEL model name
--device DEVICE inference device [CPU, GPU]
--seed SEED random seed for generating consistent images per prompt
--beta-start BETA_START
LMSDiscreteScheduler::beta_start
--beta-end BETA_END LMSDiscreteScheduler::beta_end
--beta-schedule BETA_SCHEDULE
LMSDiscreteScheduler::beta_schedule
--num-inference-steps NUM_INFERENCE_STEPS
number of inference steps
--guidance-scale GUIDANCE_SCALE
guidance scale
--eta ETA eta
--tokenizer TOKENIZER
tokenizer
--prompt PROMPT prompt
--params-from PARAMS_FROM
Extract parameters from a previously generated image.
--init-image INIT_IMAGE
path to initial image
--strength STRENGTH how strong the initial image should be noised [0.0, 1.0]
--mask MASK mask of the region to inpaint on the initial image
--output OUTPUT output image name
```


### Examples

- **Text-To-Image:**
    ```bash
    python demo.py --prompt "Street-art painting of Emilia Clarke in style of Banksy, photorealism"
    ```

- **Image-To-Image:**
    ```bash
    python demo.py --prompt "Photo of Emilia Clarke with bright red hair" --init-image ./data/input.png --strength 0.5
    ```

- **Inpainting:**
    ```bash
    python demo.py --prompt "Photo of Emilia Clarke with bright red hair" --init-image ./data/input.png --mask ./data/mask.png --strength 0.5
    ```

## Acknowledgements

- Original implementation of Stable Diffusion: [CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion)
- diffusers library: [huggingface/diffusers](https://github.com/huggingface/diffusers)

## Disclaimer

The authors are not responsible for the content generated using this project. Please do not use this project to produce illegal, harmful, offensive, or otherwise objectionable content.


