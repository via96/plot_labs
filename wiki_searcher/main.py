import wikipedia
import subprocess
import recognizer

def get_word(voice_mod: bool):
    if voice_mod:
        return recognizer.listen()
    else:
        return input('Введите слово:')

def read_text(text: str):
    print(text)
    speaker = subprocess.Popen("espeak -vru -s 60 '" + text + "'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    speaker.communicate()

if __name__ == '__main__':
    wikipedia.set_lang("ru")
    sent_amount = 4
    while True:
        word = ''
        word = get_word(True)
        if word == '': continue
        if word == 'выход':
            break
        if word.__contains__('количество предложений'):
            sent_amount = str(word.split(' ')[-1])
            read_text('Количество выводимых предложений: ' + str(sent_amount))
            continue
        try:
            if word == 'exit':
                break
            response_list = wikipedia.search(word)
            if len(response_list) == 0:
                read_text("Введенное слово неверно или определение не найдено.")
                print('\n----------------------------------------------------------------------------\n')
                continue
        except:
            read_text("Введенное слово неверно или определение не найдено.")
            print('\n----------------------------------------------------------------------------\n')
            continue
        try:
            text = wikipedia.summary(response_list[0], sentences=sent_amount)
        except wikipedia.exceptions.DisambiguationError:
            text = wikipedia.summary(response_list[1], sentences=sent_amount)
        read_text(text)
        print('\n----------------------------------------------------------------------------\n')
    read_text('До свидания.')