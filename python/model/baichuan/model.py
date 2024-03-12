import torch
import datetime

from modelscope import snapshot_download, AutoModelForCausalLM, AutoTokenizer,GenerationConfig

model_dir = snapshot_download("baichuan-inc/Baichuan2-7B-Chat", revision='v1.0.5')
tokenizer = AutoTokenizer.from_pretrained(model_dir, device_map="auto", 
                              trust_remote_code=True, torch_dtype=torch.float16)
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", offload_folder='/Users/elevenzhan/workspace/python/nlp-tutorial/model/baichuan/offload_folder',
                              trust_remote_code=True, torch_dtype=torch.float16)
model.generation_config = GenerationConfig.from_pretrained(model_dir)

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '讲解一下“温故而知新”')
messages = []
messages.append({"role": "user", "content": "讲解一下“温故而知新”"})
response = model.chat(tokenizer, messages)
print(response)

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '背诵一下将进酒')
# messages.append({'role': 'assistant', 'content': response})
messages = []
messages.append({"role": "user", "content": "背诵一下将进酒"})
response = model.chat(tokenizer, messages)
print(response)

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '介绍一下 transformer 的实现原理')
# messages.append({'role': 'assistant', 'content': response})
messages = []
messages.append({"role": "user", "content": "介绍一下 transformer 的实现原理"})
response = model.chat(tokenizer, messages)
print(response)

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "finish")
