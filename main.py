from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
import Repetition
import os
LabelBase.register(name='Pixel',
                   fn_regular='DePixelHalbfett.ttf')

class Flashcards(Widget):
    cardFront = ObjectProperty(None)
    cardBack = ObjectProperty(None)
    cardsCompleted = ObjectProperty(None)
    cardsMissed = ObjectProperty(None)
    cardsRemaining = ObjectProperty(None)
    repObj = Repetition.repetitionClass()
    isShowFront = True
    cardFS = 30

    def startup(self):
        self.repObj.startup()
        self.cardFront.fs = self.cardFS
        self.cardBack.fs = 0
    def update(self):
        #print(self.repObj.currentCard)
        #print(self.repObj.repDataFrame)
        if len(self.repObj.cardsToRedoIndex) > 0:
            self.cardFront.text = self.repObj.repDataFrame["Front of Card"][self.repObj.cardsToRedoIndex[self.repObj.currentCard]]
            self.cardBack.text = self.repObj.repDataFrame["Back of Card"][self.repObj.cardsToRedoIndex[self.repObj.currentCard]]
        else:
            self.cardFront.text = "All Done!"
            self.cardBack.text = "All Done!!!!"
            self.repObj.allDone()
        self.cardsCompleted.text = str(self.repObj.cardsSucceeded)
        self.cardsMissed.text = str(self.repObj.cardsFailed)
        self.cardsRemaining.text = str(self.repObj.cardsLeft)
        self.cardFront.fs = self.cardFS
        self.cardBack.fs = 0
        self.isShowFront = True


    def dontKnowClicked(self):
        if len(self.repObj.cardsToRedoIndex) > 0:
            self.repObj.cardWrong(self.repObj.currentCard)
            if self.repObj.cardsLeft == 0:
                self.repObj.finishSet()
        self.update()
    def KnowClicked(self):
        if len(self.repObj.cardsToRedoIndex) > 0:
            self.repObj.cardRight(self.repObj.currentCard)
            if self.repObj.cardsLeft == 0:
                self.repObj.finishSet()
        self.update()

    def cardToggled(self):
        #print(self.isShowFront)
        if self.isShowFront:
            self.cardFront.fs = 0
            self.cardBack.fs = self.cardFS
        else:
            self.cardFront.fs = self.cardFS
            self.cardBack.fs = 0
        self.isShowFront = not self.isShowFront

    def addCardButton(self):
       self.show_popup()

    def show_popup(self):
        show = addCardPop(self.repObj)
        pop = Popup(title="Add new Cards!", content=show, size_hint=(.6, .6), title_font="Pixel")
        pop.bind(on_dismiss=self.popUpClosed)
        pop.open()

    def popUpClosed(self, instance):
        self.repObj.startup()
        self.update()


class CardText(Widget):
    text = StringProperty("")
    fs = NumericProperty(0)

class CardsLeft(Widget):
    text = StringProperty("0")

class addCardPop(FloatLayout):
    #repObj = []
    #cardFrontInput = ObjectProperty(None)
    #cardBackInput = ObjectProperty(None)
    def __init__(self, repObj):
        super().__init__()
        self.repObj = repObj
    def addANewCard(self):
        #print(len(self.ids.card_front_input.text))
        #print(self.ids.card_back_input.text)
        if len(self.ids.card_front_input.text) > 0 and len(self.ids.card_back_input.text) > 0:
            self.repObj.addCard(self.ids.card_front_input.text, self.ids.card_back_input.text)
            self.ids.card_front_input.text = ""
            self.ids.card_back_input.text = ""
        self.repObj.allDone()





class SpacedRepetitionApp(App):
    def build(self):
        study = Flashcards()
        study.startup()
        study.update()
        #print("hi")   Proof that it only plays everything up to the return once.
        return study

if __name__ == '__main__':
    SpacedRepetitionApp().run()

