import subprocess
import sys

models = [
    "llama3.2",
    "llama3.1", 
    "mistral",
    "gemma3",
    "phi4",
    "qwen2.5",
    "deepseek-r1"
]

for model in models:
    print(f"\n{'='*50}")
    print(f"Starting run: {model}")
    print(f"{'='*50}")
    
    # Update simulation.py with current model
    with open("environment/simulation.py", "r") as f:
        content = f.read()
    
    # Replace the last line
    lines = content.rsplit("\n", 2)
    new_last_line = f'    run_simulation(model="{model}", rounds=50)'
    content = "\n".join(lines[:-2]) + "\n" + new_last_line + "\n"
    
    with open("environment/simulation.py", "w") as f:
        f.write(content)
    
    # Run simulation
    result = subprocess.run(
        [sys.executable, "environment/simulation.py"],
        capture_output=False
    )
    
    print(f"\nCompleted: {model}")

print("\n ALL 7 MODELS COMPLETE!")
print("Run py analysis/gini.py to see results")
