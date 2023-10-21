from kivy.app import App
from kivy.event import EventDispatcher
from kivy.uix.label import Label
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
import threading

tokenizer = AutoTokenizer.from_pretrained("gpt2")

model = AutoModelForCausalLM.from_pretrained(
    "gpt2", device_map="auto", load_in_4bit=True, pad_token_id=tokenizer.eos_token_id
)


def get_bot_response(text: str, dispatcher: EventDispatcher, app: App):
    model_inputs = tokenizer([text], return_tensors="pt").to("cuda")
    generated_ids = model.generate(**model_inputs, 
                                   max_new_tokens=70, 
                                   num_beams=7, 
                                   no_repeat_ngram_size=2,
                                   early_stopping=True,
                                   )
    bot_response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    dispatcher.dispatch('on_bot_responded', bot_response, app)

class ChatMessage(Label):
    pass

class BotEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_bot_responded')
        super(EventDispatcher, self).__init__(**kwargs)

    def on_bot_responded(self, *args):
        text_arr = args[0].split(' ')
        text = ''
        for i, piece in enumerate(text_arr):
            if i > 0 and i % 15 == 0:
                text += '\n'
            text += f'{piece} '

        app = args[1]
        app.root.ids['chat'].data.append({'text': f'Bot: {text}'})
        print(f'Bot Response:-\n\n{args[0]}\n\n')

class MainApp(App):

    bot_dispatcher = BotEventDispatcher()
    
    def on_message_received(self, text):
        self.root.ids['chat'].data.append({'text': f'User: {text}'})
        
        bot_thread = threading.Thread(target=get_bot_response, args=(text, MainApp.bot_dispatcher, self))
        bot_thread.start()


if __name__ == '__main__':
    MainApp().run()


