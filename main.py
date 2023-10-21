from kivy.app import App


from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "gpt2", device_map="auto", load_in_4bit=True
)


tokenizer = AutoTokenizer.from_pretrained("gpt2")

class MainApp(App):
    
    def on_message_received(self, text):
        model_inputs = tokenizer([text], return_tensors="pt").to("cuda")

        generated_ids = model.generate(**model_inputs, max_new_tokens=30)
        bot_response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        self.root.ids['chat'].data.append({'text': f'User: {text}'})
        self.root.ids['chat'].data.append({'text': f'bot: {bot_response}'})

        


if __name__ == '__main__':
    MainApp().run()


