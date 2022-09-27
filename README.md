# OpenAI Whisper - CPU

## About

Experiments applying quantization methods to OpenAI Whisper ASR model
to improve the inference speed and throughput on CPU-based deployments.
This is motivated by the fact that, although the Whisper model greatly
improves the accessibility of SOTA ASR and doesn't require depending
on the cloud for high quality transcription, many end users can not
run this model out-of-the-box as most consumer computers only contain
CPUs and do not contain high performance GPUs.

## Results

The below results are for performing inference on 30 seconds of audio.

| Model | Inference |
| --- | ----------- |
| fp32 | 19.1 |
| qint8 | 6.9 |