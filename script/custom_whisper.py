#!/usr/bin/python3

import sys

#audio/Byron_Katie_Podcast/Byron_Katie_KICK_OFF_FINAL_MIX.mp3 --language English --model large
audio_path = str(sys.argv[1])
print ('Audio:', audio_path)
print ('Language Tag', str(sys.argv[2]))
language = str(sys.argv[3])
print ('Language:', language)
print ('Model Tag:', str(sys.argv[4]))
model_name = str(sys.argv[5])
print ('Model:', model_name)

import whisper
import torch


model_fp32 = whisper.load_model(
    name=model_name,
    device="cpu"
#   ,in_memory=True
)

print(torch.__version__)

quantized_model = torch.quantization.quantize_dynamic(
    model_fp32, {torch.nn.Linear}, dtype=torch.qint8
)

#print(quantized_model)
#print(model_fp32)

import os

def print_size_of_model(model):
    path = "temp.p"
    torch.save(model.state_dict(), path)
    size = os.path.getsize(path)/1e6
    print('Size (MB):', size)
    os.remove(path)
    return size

print_size_of_model(model_fp32)
print_size_of_model(quantized_model)

#audio = whisper.load_audio(audio_file)
#audio = whisper.pad_or_trim(audio)

#mel   = whisper.log_mel_spectrogram(audio).to(model_fp32.device)
#options = whisper.DecodingOptions(language=language,fp16=False)

# regular
#_, probs = model_fp32.detect_language(mel)
#print(f"Detected language: {max(probs, key=probs.get)}")

# quantized
#_, probs = quantized_model.detect_language(mel)
#print(f"Detected language: {max(probs, key=probs.get)}")

from pathlib import Path
from whisper.utils import write_srt
import json

import time
def time_model_evaluation(model,audio_file):
    eval_start_time = time.time()
    # result = whisper.decode(model, mel, options)
    result = whisper.transcribe(model, audio_file)
    eval_end_time = time.time()
    eval_duration_time = eval_end_time - eval_start_time

    # save SRT
    audio_basename = Path(audio_file).stem
    with open(Path("./script") / (audio_basename + ".srt"), "w", encoding="utf-8") as srt:
        write_srt(result["segments"], file=srt)
    # save JSON
    json_object = json.dumps(result, indent=4)
    with open(Path("./script") / (audio_basename + ".json"), "w", encoding="utf-8") as json:
        json.write(json_object)

    print("Evaluate total time (seconds): {0:.1f}".format(eval_duration_time))


# check if audio_path is a dir or a file
if os.path.exists(os.path.dirname(audio_path)):
    # is dir
    files = [f for f in os.listdir(audio_path) if os.path.isfile(os.path.join(audio_path, f))]
    for audio_file in files:
        time_model_evaluation(quantized_model,os.path.join(audio_path, audio_file))
else:
    # is file
    time_model_evaluation(quantized_model,audio_path)




# Evaluate the original FP32 BERT model
# time_model_evaluation(model_fp32, mel, options)

# Evaluate the INT8 BERT model after the dynamic quantization
#time_model_evaluation(quantized_model)

#torch.save(quantized_model.state_dict(), "./script/quantized_model.p")
