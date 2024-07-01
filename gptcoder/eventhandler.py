from .client import client as openai_client
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta
from openai.types.beta.threads import Message, MessageDelta
from openai.types.beta.threads.runs import ToolCall, RunStep
from openai.types.beta import AssistantStreamEvent

class EventHandler(AssistantEventHandler):
    ANSI_RED = "\033[31m"
    ANSI_GREEN = "\033[32m"
    ANSI_YELLOW = "\033[33m"
    ANSI_BLUE = "\033[34m"
    ANSI_MAGENTA = "\033[35m"
    ANSI_CYAN = "\033[36m"
    ANSI_RESET = "\033[0m"

    def __init__(self, thread_id, assistant_id):
        super().__init__()
        self.thread_id = thread_id
        self.assistant_id = assistant_id
        self.run_id = None
        self.run_step = None
        self.arguments = ""
      
    @override
    def on_text_created(self, text) -> None:
        print(f"{self.ANSI_GREEN}assistant on_text_created > {self.ANSI_RESET}", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(f"{self.ANSI_CYAN}{delta.value}{self.ANSI_RESET}", end="")

    @override
    def on_end(self):
        print(f"{self.ANSI_RED}\n end assistant > {self.ANSI_RESET}", flush=True)

    @override
    def on_exception(self, exception: Exception) -> None:
        print(f"{self.ANSI_MAGENTA}\nassistant > {exception}{self.ANSI_RESET}\n", end="", flush=True)

    @override
    def on_message_created(self, message: Message) -> None:
        print(f"{self.ANSI_YELLOW}\nassistant on_message_created > {message}{self.ANSI_RESET}\n", end="", flush=True)

    @override
    def on_message_done(self, message: Message) -> None:
        print(f"{self.ANSI_BLUE}\nassistant on_message_done > {message}{self.ANSI_RESET}\n", end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"{self.ANSI_GREEN}\nassistant on_tool_call_created > {tool_call}{self.ANSI_RESET}")

    @override
    def on_tool_call_done(self, tool_call: ToolCall) -> None:
        print(f"{self.ANSI_BLUE}\nDONE STATUS: {self.run_step.status}{self.ANSI_RESET}")

    @override
    def on_run_step_created(self, run_step: RunStep) -> None:
        print(f"{self.ANSI_YELLOW}on_run_step_created{self.ANSI_RESET}")
        self.run_id = run_step.run_id
        self.run_step = run_step

    @override
    def on_run_step_done(self, run_step: RunStep) -> None:
        print(f"{self.ANSI_GREEN}\n run step done assistant {self.ANSI_RESET} > {self.ANSI_RED}{run_step}{self.ANSI_RESET}\n", flush=True)

    # def on_tool_call_delta(self, delta, snapshot):
    #     print(self.ANSI_CYAN)
    #     super().on_tool_call_delta(delta, snapshot)
    #     print(self.ANSI_RESET)

    @override
    def on_event(self, event: AssistantStreamEvent) -> None:
        # print(f"{self.ANSI_MAGENTA}\nEvent: {event.event}{self.ANSI_RESET}", flush=True)
        if event.event == "thread.run.requires_action":
            print("\nthread.run.requires_action > submit tool call")
            print(f"ARGS: {self.arguments}")