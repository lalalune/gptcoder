import time
import numpy
import numpy as np

from gptcoder.eventhandler import EventHandler

from .client import client, claude, assistant, train_challenge

def test_solution(problem_id, data):
    solved = True
    test_results = []
    print(f"Testing problem ID: {problem_id}")
    solver = None
    f = open(f"solves/solution_{problem_id}.py")
    code = f.read()
    
    for i, pair in enumerate(data["train"]):
        input_grid = pair["input"]
        expected_output = pair["output"]
        try:
            exec(code)
            solver = locals()["solve"]
            output = solver(input_grid)
            test_results.append({
                "input": input_grid,
                "output": output,
                "expected_output": expected_output
            })
            if output != expected_output:
                print(f"Test {i + 1} failed")
                solved = False
        except Exception as e:
            print(f"Error calling solve function: {e}")
            solved = False
            return False, test_results, str(e)
        
        print("Output:")
        print(output)
        print("Expected output:")
        print(expected_output)

    return solved, test_results, None


def solve_problem(thread, context):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=context,
    )
    
    print("Starting the run")

    # Start the run
    with client.beta.threads.runs.create_and_stream(
        thread_id=thread.id, assistant_id=assistant.id, event_handler=EventHandler(thread.id, assistant.id),
    ) as stream:
        stream.until_done()

    # Retrieve all messages and find the last message
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    # Assuming the last message contains the assistant's response
    messages = messages.data
    first_message = messages[0]
    content = first_message.content[0].text.value
    return content

def ask_claude(context, content):
    claude_prompt = f"Here is the problem description:\n{context}\n\n---\n\nHere is the latest unsuccessful attempt at solving it:\n{content}\n\n---\n\nCan you suggest a different approach to solve this problem?"
    
    print("CLAUDE PROMPT")
    print(claude_prompt)
    
    messages = [{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": claude_prompt
            }
        ]
    }]
    print("Asking Claude for some insight...")
    claude_response = claude.messages.create(model="claude-3-opus-20240229", max_tokens=4096, messages=messages).content
    return "This was the response that I got from Claude:\n" + claude_response[0].text + "\n\n---\n\nPlease try to verify these results with code interpreter, and try the problem again."

def extract_solution(content):
    lines = content.split("\n")
    start = None
    end = None
    for i, line in enumerate(lines):
        if "```" in line:
            if start is None:
                start = i
            else:
                end = i
                break

    if start is None or end is None:
        return content
            
    return "\n".join(lines[start + 1 : end])

import time

def test_test_solution():
    print("Testing 'test_solution' function...")

    items = train_challenge.items()
    problem_id, data = next(iter(items))
    
    solve_string = """\
def solve(input_matrix):
    n = 3
    res = [[0] * (n * 3) for _ in range(n * 3)]

    # Define transformation mappings accurately
    def get_pattern(val):
        if val == 0:
            return [[0] * 3 for _ in range(3)]
        elif val == 7:
            return [[0, 7, 7], [7, 7, 7], [0, 7, 7]]
        elif val == 4:
            return [[4, 0, 4], [0, 0, 0], [0, 4, 0]]
        elif val == 2:
            return [[2, 2, 2], [0, 0, 0], [0, 2, 2]]  # Adjusted pattern here
        elif val == 6:
            return [[6, 6, 0], [6, 0, 0], [0, 6, 6]]
        else:
            return [[val, 0, val], [0, 0, 0], [0, val, 0]]
    
    for i in range(n):
        for j in range(n):
            pattern = get_pattern(input_matrix[i][j])
            for pi in range(3):
                for pj in range(3):
                    res[3 * i + pi][3 * j + pj] = pattern[pi][pj]
    
    return res"""
    
    # save solve_string to solves/solution_test.py
    with open("solves/solution_test.py", "w") as f:
        f.write(solve_string)
    
    
    # Define a problem ID and dummy data
    problem_id = "test"
    
    # save to solves/solution_test.py
    # Call the function with the dummy data
    solved, test_results, error = test_solution(problem_id, data)
    # Check results
    if solved and error is None:
        print("test_solution passed.")
    else:
        print("test_solution failed.")
    print()

def test_solve_problem():
    print("Testing 'solve_problem' function...")
    # Setting up a dummy thread; replace this with actual thread creation if possible
    thread = client.beta.threads.create()
    context = "Dummy context for solving a problem: Please provide python code for a simple mathematical operation for addition of two numbers."
    # Attempting to solve the problem using the real function
    try:
        response = solve_problem(thread, context)
        print("Received response from solve_problem function:")
        print(response)
        print("test_solve_problem passed.")
    except Exception as e:
        print(f"test_solve_problem failed with an exception: {e}")
    print()

def test_ask_claude():
    print("Testing 'ask_claude' function...")
    context = "Dummy problem description: Find the sum of two numbers."
    content = "Previous unsuccessful attempt involved incorrect function structure."
    # Attempting to ask Claude using the real function
    try:
        response = ask_claude(context, content)
        print("Received response from Claude:")
        print(response)
        print("test_ask_claude passed.")
    except Exception as e:
        print(f"test_ask_claude failed with an exception: {e}")
    print()

def test_extract_solution():
    print("Testing 'extract_solution' function...")
    # Create a string with code block
    content = "Here is some text\n```\ndef solve(x):\n    return x * x\n```\nSome more text"
    # Extract the code block
    code = extract_solution(content)
    # Check if the extracted code matches expected output
    expected_code = "def solve(x):\n    return x * x"
    if code.strip() == expected_code:
        print("extract_solution passed.")
    else:
        print("extract_solution failed.")

if __name__ == "__main__":
    test_test_solution()
    test_solve_problem()
    test_ask_claude()
    test_extract_solution()
