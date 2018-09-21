import wikipedia
import subprocess

def read_text(text: str):
    print(text)
    speaker = subprocess.Popen("espeak -vru -s 60 '" + text + "'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    speaker.communicate()

if __name__ == '__main__':
    wikipedia.set_lang("ru")
    while True:
        word = input('Введите слово:')
        try:
            if word == 'exit':
                break
            response_list = wikipedia.search(word, results=2)
            if len(response_list) == 0:
                read_text("Введенное слово неверно или определение не найдено.")
                print('\n----------------------------------------------------------------------------\n')
                continue
        except:
            read_text("Введенное слово неверно или определение не найдено.")
            print('\n----------------------------------------------------------------------------\n')
            continue
        try:
            text = wikipedia.summary(response_list[0], sentences=4)
        except wikipedia.exceptions.DisambiguationError:
            text = wikipedia.summary(response_list[1], sentences=4)
        read_text(text)
        print('\n----------------------------------------------------------------------------\n')