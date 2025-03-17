import json
import glob
import matplotlib.pyplot as plt
import numpy as np
import re
import argparse
args = argparse.ArgumentParser()
args.add_argument("--model", type=str, default="qwen")
args = args.parse_args()

# Find all result files
result_files = glob.glob(f'results/{args.model}/throughput_*_*.json')

# Dictionary to store data by model
models_data = {}

# Read each result file
for file in sorted(result_files):
    with open(file, 'r') as f:
        data = json.load(f)
        
        # Extract model and num_prompts from filename pattern "throughput_MODEL_NUMPROMPTS.json"
        match = re.search(r'throughput_(\d+)_(\d+)\.json', file)
        if match:
            model_size = match.group(1)
            num_prompts = match.group(2)
            model_name = f"Qwen2.5-{model_size}B"
            
            if model_name not in models_data:
                models_data[model_name] = {
                    'tokens': [],
                    'throughputs': [],
                    'latencies': []
                }
            
            models_data[model_name]['tokens'].append(data['total_num_tokens'])
            models_data[model_name]['throughputs'].append(data['tokens_per_second'])
            models_data[model_name]['latencies'].append(data['elapsed_time'])

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Colors for different models
colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']

# Plot throughput and latency for each model
for i, (model_name, model_data) in enumerate(models_data.items()):
    color = colors[i % len(colors)]
    marker = 'o'
    
    # Sort data points by token count
    sorted_data = sorted(zip(model_data['tokens'], model_data['throughputs'], model_data['latencies']))
    tokens = [item[0] for item in sorted_data]
    throughputs = [item[1] for item in sorted_data]
    latencies = [item[2] for item in sorted_data]
    
    # Plot throughput
    ax1.semilogx(tokens, throughputs, marker=marker, color=color, linestyle='-', label=model_name)
    
    # Plot latency
    ax2.semilogx(tokens, latencies, marker=marker, color=color, linestyle='-', label=model_name)

# Set labels and titles
ax1.set_xlabel('Number of Tokens')
ax1.set_ylabel('Throughput (tokens/sec)')
ax1.set_title('Throughput vs Number of Tokens')
ax1.grid(True)
ax1.legend()

ax2.set_xlabel('Number of Tokens')
ax2.set_ylabel('Average Latency (sec)')
ax2.set_title('Latency vs Number of Tokens')
ax2.grid(True)
ax2.legend()

# Adjust layout and save
plt.tight_layout()
plt.savefig('results/qwen/benchmark_results.png')
plt.close()

# Print numerical results
print("\nNumerical Results:")
print("Model\tTokens\tThroughput\tLatency")
print("-" * 50)
for model_name, model_data in models_data.items():
    for t, tp, l in zip(model_data['tokens'], model_data['throughputs'], model_data['latencies']):
        print(f"{model_name}\t{t}\t{tp:.2f}\t\t{l:.3f}")
