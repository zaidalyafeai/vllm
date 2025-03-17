#!/bin/bash

# Set Hugging Face token for authentication
# Replace "your_huggingface_token" with your actual token or use $HF_TOKEN if already set

for model in 4 12; do
    for num_prompts in 4 8 16 32; do
        echo "Running benchmark with ${num_prompts} prompts..."
        python benchmark_throughput.py \
            --output-json "results/gemma/throughput_${model}_${num_prompts}.json" \
            --num-prompts ${num_prompts} \
            --model google/gemma-3-${model}b-it \
            --backend vllm \
            --hf-subset default \
            --hf-split train \
            --dataset-name hf \
            --dataset HuggingFaceFW/fineweb-edu \
            --output results/gemma/outputs_${model}_${num_prompts}.json
    done
done