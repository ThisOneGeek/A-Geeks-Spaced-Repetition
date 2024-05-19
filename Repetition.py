import pandas as pd
from pandas import DataFrame
import datetime


#Class to hold Card information.
class repetitionClass():
    repDataFrame = []
    cardsFailedIndex = []
    cardsToRedoIndex = []
    cardsFullFinishedIndex = []
    isReviewing = False
    cardsLeft = 0
    cardsSucceeded = 0
    cardsFailed = 0
    currentCard = 0

    #Run on startup to allow Dataframe setup.
    def startup(self):
        try:
            self.repDataFrame = pd.read_excel('Repetition.xlsx', sheet_name='sheet1', converters={'Front of Card': str, 'Back of Card': str, 'Date of Next Rep': datetime.datetime.date, 'Repetition Number': int})
        except FileNotFoundError:
            self.repDataFrame = pd.DataFrame(columns=['Front of Card', 'Back of Card', 'Date of Next Rep', 'Repetition Number'])

        for i in range(0, len(self.repDataFrame)):
            if self.repDataFrame["Date of Next Rep"][i] == datetime.datetime.today().date() or (self.repDataFrame["Date of Next Rep"][i] - datetime.datetime.today().date()).days < 0:
                self.cardsToRedoIndex.append(i)
        self.cardsLeft = len(self.cardsToRedoIndex)

    #Adjusts the date and repetition number for cards known.
    def cardRight(self, indexNum):
        #if self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Repetition Number"] < 8:
            #print("Yo")
        self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Repetition Number"] += 1
        self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Date of Next Rep"] = datetime.datetime.today().date() + datetime.timedelta(days=2**int(self.repDataFrame["Repetition Number"][self.cardsToRedoIndex[indexNum]]))

        #if self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Repetition Number"] >= 8:
            #self.cardsFullFinishedIndex.append(self.cardsToRedoIndex[indexNum])


        if self.currentCard < (len(self.cardsToRedoIndex) - 1) and self.cardsLeft > 0:
            self.cardsSucceeded += 1
            self.cardsLeft -= 1
            self.currentCard += 1
        elif len(self.cardsToRedoIndex) == 0:
            self.cardsSucceeded += 1
            self.cardsLeft -= 1
            print("You Won")
        else:
            self.cardsSucceeded += 1
            self.cardsLeft -= 1
            self.finishSet()

    #Adjusts the repetition number for cards not known.
    def cardWrong(self, indexNum):
        self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Date of Next Rep"] = datetime.datetime.today().date()
        self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Repetition Number"] = 0
        self.cardsFailedIndex.append(self.cardsToRedoIndex[indexNum])

        if self.currentCard < (len(self.cardsToRedoIndex) - 1) and self.cardsLeft > 0:
            self.cardsFailed += 1
            self.cardsLeft -= 1
            self.currentCard += 1
        else:
            self.cardsFailed += 1
            self.cardsLeft -= 1
            self.finishSet()

    #Get current card text. Unused currently. May be removed if unneeded.
    def getCard(self, indexNum):
        return self.repDataFrame["Front of Card"][self.cardsToRedoIndex[indexNum]], self.repDataFrame["Back of Card"][self.cardsToRedoIndex[indexNum]]

    #Gets current size of card deck. Unused currently. May be removed if unneeded.
    def getDeckSize(self):
        return len(self.repDataFrame)

    #Adds card to the deck.
    def addCard(self, cFront, cBack):
        newDF = DataFrame({'Front of Card': [cFront], 'Back of Card': [cBack], 'Date of Next Rep': [datetime.datetime.today().date()], 'Repetition Number': [0]})
        self.repDataFrame = pd.concat([self.repDataFrame, newDF], ignore_index=True)

    #Removes card from deck. Currently unused.
    def removeCard(self, indexNum):
        self.repDataFrame.drop(self.repDataFrame.index[self.cardsToRedoIndex[indexNum]], inplace=True)

    #Resets cards to allow for missed cards to be seen again.
    def finishSet(self):
        self.cardsLeft = self.cardsFailed
        self.cardsFailed = 0
        self.cardsToRedoIndex = self.cardsFailedIndex
        self.cardsFailedIndex = []
        self.currentCard = 0

    #Shuffles and saves deck into an excel file.
    def allDone(self):
        self.repDataFrame = self.repDataFrame.sample(frac=1).reset_index(drop=True)
        self.repDataFrame.to_excel('Repetition.xlsx', sheet_name='sheet1', index=False)
        self.cardsToRedoIndex = []




if __name__ == '__main__':
    reps = repetitionClass()
    reps.startup()
    print(reps.repDataFrame["Date of Next Rep"][0])
    reps.cardRight(0)
    print(reps.repDataFrame["Date of Next Rep"][0])
    reps.allDone()
    print(reps.getDeckSize())
    print(reps.getCard(0))
    #reps.addCard("Apple", "Banana", datetime.datetime.today().date())
    reps.addCard("Canada", "Oh Canada")
    print(reps.repDataFrame.iloc[0])
    print(reps.repDataFrame.iloc[1])
    reps.allDone()
    #reps.removeCard(1)
    #print(reps.repDataFrame)
