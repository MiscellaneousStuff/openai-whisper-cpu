# OpenAI Whisper - CPU

## About

Experiments applying quantization methods to OpenAI Whisper ASR model
to improve the inference speed and throughput on CPU-based deployments.
This is motivated by the fact that, although the Whisper model greatly
improves the accessibility of SOTA ASR and doesn't require depending
on the cloud for high quality transcription, many end users can not
run this model out-of-the-box as most consumer computers only contain
CPUs and do not contain high performance GPUs.

This could lead to allowing the larger Whisper models run faster
on laptops without a GPU.

Hardware for experiments: \
CPU - AMD Ryzen 5 5600X \
RAM - 32GB DDR4 \
GPU - Nvidia GeForce RTX 3060 Ti \
HDD - M.2 SSD 

## Usage

Firstly, get the fork of the OpenAI Whisper repo with the
modifications needed for CPU dynamic quantization:

```bash
git submodule init
git submodule update
```

And then install the module using:

```bash
pip install -e ./whisper
```

### Explanation

Quantization of the Whisper model requires changing the `Linear()`
layers within the model to `nn.Linear()`. This is because you need
to specifiy which layer types to dynamically quantize, such as:

```python
quantized_model = torch.quantization.quantize_dynamic(
    model_fp32, {torch.nn.Linear}, dtype=torch.qint8
)
```

However the whisper model is designed to be adaptable, i.e.
it can run at different precisions, so the `Linear()` layer contains
custom code to account for this. However, this is not required for
the quantized model. You can either change the `Linear()` layers in
"/whisper/whisper/model.py" yourself, or you can just use the above
installation instructions.

## Results

Test audio is the first 30 seconds of: \
https://www.youtube.com/watch?v=oKOtzIo-uYw

| Device | Whisper Model | Data Type | Linear Layer | Inference Time |
| --- | --- | ----------- | --- | --- |
| GPU | tiny | fp32 | Linear | 0.5 |
| CPU | tiny  | fp32 | nn.Linear | 2.3 |
| CPU | tiny  | qint8 (quant) | nn.Linear | 3.1 (0.74x slowdown) |

Tiny quantized model is 9.67x faster than real time. \
Tiny quantized model is 0.74x slower than the original model.

| Device | Whisper Model | Data Type | Linear Layer | Inference Time |
| --- | --- | ----------- | --- | --- |
| GPU | base | fp32 | Linear | 0.6 |
| CPU | base  | fp32 | nn.Linear | 5.2 |
| CPU | base  | qint8 (quant) | nn.Linear | 3.2 (1.62x speedup) |

Base quantized model is 9.37x faster than real time. \
Base quantized model is 1.62x faster than the original model.

| Device | Whisper Model | Data Type | Linear Layer | Inference Time |
| --- | --- | ----------- | --- | --- |
| GPU | small | fp32 | Linear | 0.7 |
| CPU | small | fp32 | nn.Linear | 19.1s |
| CPU | small | qint8 (quant) | nn.Linear | 6.9s (2.76x speedup) |

Small quantized model is 4.34x faster than real time. \
Small quantized model is 2.76x faster than the original model.

| Device | Whisper Model | Data Type | Linear Layer | Inference Time |
| --- | --- | ----------- | --- | --- 
| GPU | medium | fp32 | Linear | 1.7s |
| CPU | medium | fp32 | nn.Linear | 60.7 |
| CPU | medium | qint8 (quant) | nn.Linear | 23.1 (2.62x speedup) |

Medium quantized model is 1.29x faster than real time. \
Medium quantized model is 2.62x faster than the original model.
