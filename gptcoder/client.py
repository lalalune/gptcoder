import json
import os
from anthropic import Anthropic
from openai import OpenAI

client = OpenAI()
claude = Anthropic(
    api_key=os.environ["CLAUDE_API_KEY"]
)

instructions = "You are solving the ARC AGI challenge by writing python programs which correctly transform all inputs to all outputs for the examples. The examples are in the form of an input grid and output grid. The goal is to figure out the function that successfully maps all inputs to otheir corresponding outputs, such that a new output could be guessed from a new input. You should use code interpreter to test the python code that you create and verify that it works on all of the input and output examples. It should assert an error if it doesn't."

# Create the assistant
assistant = client.beta.assistants.create(
    name="ARC AGI Solver",
    tools=[{"type": "code_interpreter"}],
    instructions=instructions,
    model="gpt-4",
)

def load_data(file_path):
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

def sort_key(item):
    challenge_id, data = item
    input_grid = data[0]['train'][0]['input']  # Assumes the structure includes a 'train' list with 'input'
    output_grid = data[0]['train'][0]['output']
    return (len(input_grid) * len(input_grid[0]), len(output_grid) *  len(output_grid[0]))

# Load the training challenge and solutions
train_challenge = load_data("arc-prize-2024/arc-agi_training_challenges.json")
train_solution = load_data("arc-prize-2024/arc-agi_training_solutions.json")

# Pair the challenges with their solutions using the challenge ID
paired_data = [(challenge_id, (data, train_solution[challenge_id])) for challenge_id, data in train_challenge.items()]

# Sort the data by the dimensions of the input and output grids
sorted_data = sorted(paired_data, key=sort_key)

# Unpack the sorted data back into challenges and solutions
sorted_train_challenge = {item[0]: item[1][0] for item in sorted_data}
sorted_train_solution = {item[0]: item[1][1] for item in sorted_data}

# Overwrite the original variables
train_challenge = sorted_train_challenge
train_solution = sorted_train_solution

first_key = list(train_challenge.keys())[0]
last_key = list(train_challenge.keys())[-1]

print("Dimensions of the first input grid:")
print(len(train_challenge[first_key]['train'][0]['input']), len(train_challenge[first_key]['train'][0]['input'][0]))
print("Dimensions of the first output grid:")
print(len(train_challenge[first_key]['train'][0]['output']), len(train_challenge[first_key]['train'][0]['output'][0]))

# print the last
print("Dimensions of the last input grid:")
print(len(train_challenge[last_key]['train'][0]['input']), len(train_challenge[last_key]['train'][0]['input'][0]))
print("Dimensions of the last output grid:")
print(len(train_challenge[last_key]['train'][0]['output']), len(train_challenge[last_key]['train'][0]['output'][0]))

