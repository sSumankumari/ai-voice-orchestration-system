import os
from ai.orchestrator import Orchestrator

# Pre-check
if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError(
        "GROQ_API_KEY not set.\n"
        "Run: set GROQ_API_KEY=your_key_here (Windows)\n"
        "or: export GROQ_API_KEY=your_key_here (Linux/Mac)"
    )

# Test config
SESSION_ID = "test-session-001"

USER_PROMPT = (
    "You are a financial advisor helping graduate students "
    "plan education loans responsibly."
)

TEST_MESSAGES = [
    "Hi",
    "I want advice on education loans",
    "Which loan should I prioritize first?",
    "How should I plan repayment?"
]

# Test runner
def run_test():
    orchestrator = Orchestrator()

    print("\nStarting AI Orchestration Test\n")

    for idx, user_message in enumerate(TEST_MESSAGES, 1):
        print(f"User ({idx}): {user_message}")

        response, intent = orchestrator.handle_message(
            session_id=SESSION_ID,
            user_message=user_message,
            user_prompt=USER_PROMPT
        )

        print(f"Detected Intent: {intent}")
        print(f"Agent Response:\n{response}\n")

    print("AI pipeline test completed successfully\n")


if __name__ == "__main__":
    run_test()
