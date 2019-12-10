from googletrans import Translator

text = 'pippeli oli puutarhassa'
translator = Translator()
if __name__=="__main__":
    print(translator.translate(text))    