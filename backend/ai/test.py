from orchestrator import Orchestrator

agent = Orchestrator()

while True:
    user_input = input("User: ")
    print("Agent:", agent.handle_message(user_input))
