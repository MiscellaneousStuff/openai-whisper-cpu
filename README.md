# OpenAI Whisper - CPU

## About

Experiments applying quantization methods to OpenAI Whisper ASR model
to improve the inference speed and throughput on CPU-based deployments.
This is motivated by the fact that, although the Whisper model greatly
improves the accessibility of SOTA ASR and doesn't require depending
on the cloud for high quality transcription, many end users can not
run this model out-of-the-box as most consumer computers only contain
CPUs and do not contain high performance GPUs.

This could lead to allowing the larger Whisper models to faster
on laptops without a GPU.

## Results

Test audio is the first 30 seconds of: \
https://www.youtube.com/watch?v=oKOtzIo-uYw

| Device | Whisper Model | Data Type | Linear Layer | Inference Time |
| --- | --- | ----------- | --- | --- |
| GPU | tiny | fp32 | Linear | 0.5 |
| CPU | tiny  | fp32 | nn.Linear | 2.3 |
| CPU | tiny  | qint8 (quant) | nn.Linear | 3.1 (0.74x slowdown) |

| Device | Whisper Model | Data Type | Linear Layer | Inference Time |
| --- | --- | ----------- | --- | --- |
| GPU | base | fp32 | Linear | 0.6 |
| CPU | base  | fp32 | nn.Linear | 5.2 |
| CPU | base  | qint8 (quant) | nn.Linear | 3.2 (1.62x speedup) |

| Device | Whisper Model | Data Type | Linear Layer | Inference Time |
| --- | --- | ----------- | --- | --- |
| GPU | small | fp32 | Linear | 0.7 |
| CPU | small | fp32 | nn.Linear | 19.1s |
| CPU | small | qint8 (quant) | nn.Linear | 6.9s (2.76x speedup) |

| Device | Whisper Model | Data Type | Linear Layer | Inference Time |
| --- | --- | ----------- | --- | --- 
| GPU | medium | fp32 | Linear | 1.7s |
| CPU | medium | fp32 | nn.Linear | 60.7 |
| CPU | medium | qint8 (quant) | nn.Linear | 23.1 (2.62x speedup) |