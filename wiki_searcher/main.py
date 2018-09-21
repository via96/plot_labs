import wikipedia
import subprocess

if __name__ == '__main__':
    wikipedia.set_lang("ru")
    while True:
        word = input('Введите слово:')
        try:
            if word == 'exit':
                break
            response_list = wikipedia.search(word)
            amount = len(response_list)
            if amount == 1:
                text = wikipedia.summary(response_list[0], sentences=4)
            else:
                try:
                    text = wikipedia.summary(response_list[0], sentences=4)
                except:
                    text = wikipedia.summary(response_list[1], sentences=4)
            print(text)
            # subprocess.call("espeak -vru -s 60 '" + text + "'", shell=True)
        except:
            print("Введенное слово неверно или определение не найдено.")
        print('\n----------------------------------------------------------------------------\n')