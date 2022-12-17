import telebot
from document_processing import create_temp_name, document2text, preprocess_text
import os
import neuro

bot = telebot.TeleBot('5860937749:AAH0y9PTyWWvEvSWNuy8fsTWUH8sNrO7o6g')
model = neuro.init_model()
tokenizer = neuro.init_tokenizer()
print('Bot started')


@bot.message_handler(content_types=['document'])  # list relevant content types
def addfile(message):
    # ask person and give 2 buttons
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    name = create_temp_name()
    folder_path = os.path.join("temp", name)
    os.mkdir(folder_path)
    src = os.path.join(folder_path, file_name)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    # make prediction
    original_text = document2text(src)
    text = preprocess_text(original_text)
    prediction = neuro.predict(model, tokenizer, text)
    bot.send_message(message.chat.id, f'{prediction}'
                                      f'Я считаю, что документ "{file_name}" - {prediction}')


# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, "Привет, я бот, который поможет тебе разобраться с документами. "
                                "Просто отправь мне документ, и я скажу, что это за документ"
                                "Если хочешь узнать больше, напиши /help")


# Запускаем бота
bot.polling(none_stop=True, interval=0)
