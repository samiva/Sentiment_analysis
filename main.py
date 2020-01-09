import kivy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from termcolor import colored
import webbrowser
# tokenizer
from tokenizier import GetFreqMat

names_fi_sw = ['Finland#liigaUsersIDData', 'Finland#VeikkausliigaUsersIDData',
               'Sweden#AllsvenskanUsersIDData', 'Sweden#SHLUsersIDData']
names_dk_no = ['Denmark#sldkUsersIDData',
               'Norway#getligaenUsersIDData', 'Norway#eliteserienUsersIDData']


class MyCustomBoxLayout(TabbedPanel):
    def finland_ice_token_freq(self):
        print(colored("Liiga - ice hockey", 'blue'))
        GetFreqMat('./data/' + names_fi_sw[0] + '.csv')

    def finland_football_token_freq(self):
        print(colored("Veikkausliiga - football", 'blue'))
        GetFreqMat('./data/' + names_fi_sw[1] + '.csv')

    def sweden_football_token_freq(self):
        print(colored('Allsvenskan - football', 'blue'))
        GetFreqMat('./data/' + names_fi_sw[2] + '.csv')

    def sweden_ice_token_freq(self):
        print(colored('Allsvenskan - football', 'blue'))
        GetFreqMat('./data/' + names_fi_sw[3] + '.csv')

    def denmark_football_token_freq(self):
        print(colored('Super League - football', 'blue'))
        GetFreqMat('./data/' + names_dk_no[0] + '.csv')

    def norway_football_token_freq(self):
        print(colored('Eliteserien - football', 'blue'))
        GetFreqMat('./data/' + names_dk_no[2] + '.csv')

    def norway_ice_token_freq(self):
        print(colored('GET-ligaen - ice', 'blue'))
        GetFreqMat('./data/' + names_dk_no[1] + '.csv')

    def finland_ice_lda(self):
        webbrowser.open('.\data\Finland#liigaUsersIDData.html')

    def finland_football_lda(self):
        webbrowser.open('.\data\Finland#VeikkausliigaUsersIDData.html')

    def sweden_ice_lda(self):
        webbrowser.open('.\data\Sweden#SHLUsersIDData.html')

    def sweden_football_lda(self):
        webbrowser.open('.\data\Sweden#AllsvenskanUsersIDData.html')

    def denmark_football_lda(self):
        webbrowser.open('.\data\Denmark#sldkUsersIDData.html')

    def norway_football_lda(self):
        webbrowser.open('.\\data\\Norway#eliteserienUsersIDData.html')

    def norway_ice_lda(self):
        webbrowser.open('.\\data\\Norway#getligaenUsersIDData.html')


class MyApp(App):
    def build(self):
        return Builder.load_file('main.kv')


if __name__ == '__main__':
    MyApp().run()
