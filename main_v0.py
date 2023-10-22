class IncremantalModel:
    def __init__(self):
        self.questions_and_answers = {
              "What is Capital of egypt?": "cairo.",
              "How are you?": "I'm fine.",
              "What is the computer science specailization?": "computer science and software engineering",
        }
    def get_response(self, user_input):
        if user_input in self.questions_and_answers:
            return self.questions_and_answers[user_input]
        else:
            return "I don't know the answer to that question."
if __name__ == "__main__":
    my_bot = IncremantalModel()
    print("Chatbot: Hello! Ask me a question or type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        response = my_bot.get_response(user_input)
        print("Chatbot:", response)
