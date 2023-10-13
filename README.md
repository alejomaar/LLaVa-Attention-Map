# 🌋 LLaVA: Large Language and Vision Assistant

*Visual instruction tuning towards large language and vision models with GPT-4 level capabilities.*

## Windows Install

1. Clone this repository and navigate to LLaVA folder
```
git clone https://github.com/natlamir/LLaVA-Windows.git llava
cd llava
```

2. Create environment and install dependencies
```
conda create -n llava python=3.10
conda activate llava
pip install -r requirements.txt
```

3. Install PyTorch from [Pytorch Website](https://pytorch.org/get-started/locally/)
```
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

4. Downgrade pydantic to fix the model queue infinite load issue
```
pip install pydantic==1.10.9
```

5. Install bitsandbytes for windows to be able to run quantized model
```
install bitsandbytes-windows: pip install git+https://github.com/Keith-Hon/bitsandbytes-windows.git
```

### Manually Download Model (Optional)
The models are located in the [Model Zoo](https://github.com/haotian-liu/LLaVA/blob/main/docs/MODEL_ZOO.md). For this example, I will use the "liuhaotian/llava-v1.5-7b" model.
1. Create a folder called "models" within the "llava" install folder

2. cd into the "models" folder from a prompt

3. Download 7b model from hugging face into the models folder
```
git lfs install
git clone https://huggingface.co/liuhaotian/llava-v1.5-7b
```

### Usage
1. Lanuch 3 anaconda prompts. For each one: Activate llava environment, and cd into the llava install folder.

2. Launch the controller in 1st anaconda prompt
```
python -m llava.serve.controller --host 0.0.0.0 --port 10000
```

3. Launch the model worker using 8-bit quantized model

Using the model card (this will also download the model first)
```
python -m llava.serve.model_worker --host "0.0.0.0" --controller-address "http://localhost:10000" --port 40000 --worker-address "http://localhost:40000" --model-path "liuhaotian/llava-v1.5-7b" --load-8bit
```

Or: this is using the manually installed model that should be in the models folder from the previous optional step
```
python -m llava.serve.model_worker --host "0.0.0.0" --controller-address "http://localhost:10000" --port 40000 --worker-address "http://localhost:40000" --model-path "models/llava-v1.5-7b" --load-8bit
```

4. Launch the Gradio Web UI
```
python -m llava.serve.gradio_web_server --controller http://localhost:10000 --model-list-mode reload
```

5. Open a browser and navigate to ```http://127.0.0.1```


## Citation

If you find LLaVA useful for your research and applications, please cite using this BibTeX:
```bibtex

@misc{liu2023improvedllava,
      title={Improved Baselines with Visual Instruction Tuning}, 
      author={Liu, Haotian and Li, Chunyuan and Li, Yuheng and Lee, Yong Jae},
      publisher={arXiv:2310.03744},
      year={2023},
}

@misc{liu2023llava,
      title={Visual Instruction Tuning}, 
      author={Liu, Haotian and Li, Chunyuan and Wu, Qingyang and Lee, Yong Jae},
      publisher={arXiv:2304.08485},
      year={2023},
}
```

## Acknowledgement

- [Vicuna](https://github.com/lm-sys/FastChat): the codebase we built upon, and our base model Vicuna-13B that has the amazing language capabilities!

## Related Projects

- [Instruction Tuning with GPT-4](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM)
- [LLaVA-Med: Training a Large Language-and-Vision Assistant for Biomedicine in One Day](https://github.com/microsoft/LLaVA-Med)
- [Otter: In-Context Multi-Modal Instruction Tuning](https://github.com/Luodian/Otter)

For future project ideas, please check out:
- [SEEM: Segment Everything Everywhere All at Once](https://github.com/UX-Decoder/Segment-Everything-Everywhere-All-At-Once)
- [Grounded-Segment-Anything](https://github.com/IDEA-Research/Grounded-Segment-Anything) to detect, segment, and generate anything by marrying [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO) and [Segment-Anything](https://github.com/facebookresearch/segment-anything).
