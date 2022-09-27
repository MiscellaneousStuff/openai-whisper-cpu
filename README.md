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

Test audio is the first 30 seconds of: \
https://www.youtube.com/watch?v=oKOtzIo-uYw

The below results are for performing inference on 30 seconds of audio.

| Whisper Model | Model Type | Linear Layer | Inference Time |
| --- | --- | ----------- | --- |
| tiny  | fp32 | nn.Linear | 2.3 |
| tiny  | fp32 | Linear | 2.3 |
| tiny  | qint8 | nn.Linear | 3.1 |
| small | fp32 | nn.Linear | 19.1s |
| small | fp32 | Linear | 19.5s |
| small | qint8 | nn.Linear | 6.9s |