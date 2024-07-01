import json
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

from .client import client, train_challenge, train_solution, assistant
from .functions import test_solution, solve_problem, extract_solution, ask_claude

if not os.path.exists("conversation_threads"):
    os.makedirs("conversation_threads", exist_ok=True)


max_loop_count = 25

# Get the list of problem IDs from train_challenge
problem_ids = list(train_challenge.keys())

def solve_challenge(problem_id, data):
    thread = client.beta.threads.create()
    init_context = ""
    if os.path.exists(f"final_solves/solution_{problem_id}.py"):
        print(f"Problem {problem_id} already solved")
        solved, test_results, error = test_solution(problem_id, data)
        if solved:
            print(f"Problem {problem_id} was correctly solved")
            return
        else:
            print(f"Problem {problem_id} was not solved correct. Re-solving...")

        init_context = "It seems that the solution for this problem is not correct. Let's try to solve it again. Here are the results from the last attempt:\n"
        for i, result in enumerate(test_results):
            init_context += f"Test {i + 1}:\nInput:\n" + '\n'.join(map(str, result["input"])) + "\nOutput:\n" + '\n'.join(map(str, result["output"])) + "\nExpected Output:\n" + '\n'.join(map(str, result["expected_output"])) + "\n\n"

        if error:
            init_context += f"Run Error: {error}"

        init_context += "\nHere's the current code that produced these results:\n"
        init_context += "\n```python\n"
        with open(f"solves/solution_{problem_id}.py") as f:
            init_context += f.read()
        init_context += "```\n"

        init_context += "\n"

    print(f"Processing problem {problem_id}")

    if problem_id not in train_solution:
        print(f"Problem {problem_id} has no solution")
        return

    # Format the prompt
    context = init_context + "We are solving the ARC AGI Challenge. Here are the input and output pairs for the problem:\n"
    for i, pair in enumerate(data["train"]):
        context += f"Input {i + 1}:\n" + '\n'.join(map(str, pair['input'])) + "\n" + f"Output {i + 1}:\n" + '\n'.join(map(str, pair['output'])) + "\n\n"

    context_added = "\nFind a generalized solution that correctly transforms all inputs to all outputs for the examples and will also work on further unseen examples. Verify your results with code interpreter. Keep working on it until you have the correct function. Ideally the function is named solve, takes one matrix input and one matrix output."

    loop_count = 0
    while loop_count < max_loop_count:
        print(f"SOLVING PROBLEM {problem_id} - Loop {loop_count + 1}")

        models = ["gpt-4o", "gpt-4o-turbo"]
        # randomly choose one model
        model = np.random.choice(models)
        print("Using model:", model)
        assistant.model = model

        content = solve_problem(thread, context + "\n" + context_added)

        new_context = "Please now output the final solution for the problem in a single block of code, wrapped in a ```python``` block. Do not include any commentary or explanation in your response. The final solution should be a complete function called 'solve' that takes in a single matrix argument for input and outputs a single matrix argument for output. If you aren't sure of the best possible solution yet, just make your best guess for the program. Please only use numpy as an external dependency for your solution."
        content = solve_problem(thread, new_context)

        solution = extract_solution(content)
        print(f"Solution found for problem {problem_id}")

        with open(f"solves/solution_{problem_id}.py", "w") as f:
            f.write(solution)
        print(f"Solution saved to solves/solution_{problem_id}.py")
        solved, results, error = test_solution(problem_id, data)

        messages = client.beta.threads.messages.list(thread_id=thread.id)

        with open(f"conversation_threads/thread_{problem_id}.json", "w") as f:
            j = messages.json()
            json.dump(j, f, indent=2)

        if solved:
            print(f"Problem {problem_id} solved")

            # make a "final_solves" directory and copy the problem to it
            os.makedirs("final_solves", exist_ok=True)
            with open(f"final_solves/solution_{problem_id}.py", "w") as f:
                f.write(solution)
            break
        else:
            print(f"Problem {problem_id} was unsuccessful")

            # Ask Claude for help 25% of the time - basically to unstuck the bot
            if np.random.random() < 0.25:
                claude_context = context
                for result in results:
                    claude_context += f"Test:\nInput:\n" + '\n'.join(map(str, result["input"])) + "\nOutput:\n" + '\n'.join(map(str, result["output"])) + "\nExpected Output:\n" + '\n'.join(map(str, result["expected_output"])) + "\n\n"

                claude_context += f"Error: {error}"

                claude_context += "\nHere's the current code that produced these results:\n"
                claude_context += "\n```python\n"
                with open(f"solves/solution_{problem_id}.py") as f:
                    claude_context += f.read()
                claude_context += "```\n"

                response = ask_claude(context, content)

                message = client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=response,
                )

            loop_count += 1

        print(f"Problem {problem_id} was unsuccessful. Continuing loop...")
    if loop_count == max_loop_count:
        print(f"Problem {problem_id} was unsuccessful after 10 loops. Moving to the next problem.")

# Process 10 challenges at a time
with ThreadPoolExecutor() as executor:
    futures = []
    for batch_start in range(0, len(problem_ids), 10):
        batch_end = min(batch_start + 10, len(problem_ids))
        batch_ids = problem_ids[batch_start:batch_end]

        for problem_id in batch_ids:
            data = train_challenge[problem_id]
            future = executor.submit(solve_challenge, problem_id, data)
            futures.append(future)

    for future in as_completed(futures):
        future.result()