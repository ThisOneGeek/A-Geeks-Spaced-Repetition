import pandas as pd
from pandas import DataFrame
import datetime

'''
cardFronts = ["What is datatype is the Python package 'Pandas' known for?"]
cardBacks = ["Dataframes"]
repNumber = [0]
repDate = [datetime.datetime.today().date()]
repDataFrame = DataFrame({'Front of Card': cardFronts, 'Back of Card': cardBacks, 'Date of Next Rep': repDate, 'Repetition Number': repNumber})
print(repDataFrame)

repDataFrame.to_excel('Repetition.xlsx', sheet_name='sheet1', index=False)
a = pd.read_excel('Repetition.xlsx', sheet_name='sheet1')
print(a['Back of Card'].to_list())
'''

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

    def startup(self):
        try:
            self.repDataFrame = pd.read_excel('Repetition.xlsx', sheet_name='sheet1', converters={'Front of Card':str, 'Back of Card':str, 'Date of Next Rep':datetime.datetime.date, 'Repetition Number':int})
        except FileNotFoundError:
            self.repDataFrame =  pd.DataFrame(columns = ['Front of Card', 'Back of Card', 'Date of Next Rep', 'Repetition Number'])

        for i in range(0, len(self.repDataFrame)):
            #print((self.repDataFrame["Date of Next Rep"][i] - datetime.datetime.today().date()).days)
            if self.repDataFrame["Date of Next Rep"][i] == datetime.datetime.today().date() or (self.repDataFrame["Date of Next Rep"][i] - datetime.datetime.today().date()).days < 0:
                self.cardsToRedoIndex.append(i)
        self.cardsLeft = len(self.cardsToRedoIndex)
        #self.cardsToRedoIndex = list(range(0, len(self.repDataFrame)))
        #self.repDataFrame["Date of Next Rep"].to_pydatetime()

    def cardRight(self, indexNum):
        #if self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Repetition Number"] < 8:
            #print("Yo")
        self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Repetition Number"] += 1
        self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Date of Next Rep"] = datetime.datetime.today().date() + datetime.timedelta(days = 2**int(self.repDataFrame["Repetition Number"][self.cardsToRedoIndex[indexNum]]))

        #if self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Repetition Number"] >= 8:
            #self.cardsFullFinishedIndex.append(self.cardsToRedoIndex[indexNum])

        #print(self.isReviewing)
        if self.currentCard < (len(self.cardsToRedoIndex) - 1) and self.cardsLeft > 0:# and not self.isReviewing:
            self.cardsSucceeded += 1
            self.cardsLeft -= 1
            #self.currentCard += 1
        #elif self.isReviewing and self.cardsToRedoIndex.index(self.currentCard) < (len(self.cardsToRedoIndex) - 1):
            #print(self.cardsToRedoIndex.index(self.currentCard) + 1)
            self.currentCard += 1
        elif len(self.cardsToRedoIndex) == 0:
            self.cardsSucceeded += 1
            self.cardsLeft -= 1
            print("You Won")
        else:
            self.cardsSucceeded += 1
            self.cardsLeft -= 1
            self.finishSet()
    def cardWrong(self, indexNum):
        self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Date of Next Rep"] = datetime.datetime.today().date()
        self.repDataFrame.loc[self.cardsToRedoIndex[indexNum], "Repetition Number"] = 0
        self.cardsFailedIndex.append(self.cardsToRedoIndex[indexNum])

        #print(self.currentCard)
        #print(len(self.repDataFrame) - 1)
        #print(self.cardsFailed)

        #print(self.isReviewing)
        if self.currentCard < (len(self.cardsToRedoIndex) - 1) and self.cardsLeft > 0:# and not self.isReviewing:
            self.cardsFailed += 1
            self.cardsLeft -= 1
            #self.currentCard += 1
        #elif self.isReviewing and self.cardsToRedoIndex.index(self.currentCard) < (len(self.cardsToRedoIndex)):
            #print(self.cardsToRedoIndex.index(self.currentCard) + 1)
            self.currentCard += 1
        else:
            self.cardsFailed += 1
            self.cardsLeft -= 1
            #print(self.cardsToRedoIndex.index(self.currentCard) < (len(self.cardsToRedoIndex) - 1))
            self.finishSet()


    def getCard(self, indexNum):
        return self.repDataFrame["Front of Card"][self.cardsToRedoIndex[indexNum]], self.repDataFrame["Back of Card"][self.cardsToRedoIndex[indexNum]]

    def getDeckSize(self):
        return len(self.repDataFrame)

    def addCard(self, cFront, cBack):
        newDF = DataFrame({'Front of Card': [cFront], 'Back of Card': [cBack], 'Date of Next Rep': [datetime.datetime.today().date()], 'Repetition Number': [0]})
        self.repDataFrame = pd.concat([self.repDataFrame, newDF], ignore_index=True)

    def removeCard(self, indexNum):
        self.repDataFrame.drop(self.repDataFrame.index[self.cardsToRedoIndex[indexNum]], inplace=True)

    def finishSet(self):
        self.cardsLeft = self.cardsFailed
        self.cardsFailed = 0
        #print(self.cardsToRedoIndex)
        #print(self.cardsFailedIndex)
        self.cardsToRedoIndex = self.cardsFailedIndex
        self.cardsFailedIndex = []
        #print(self.cardsToRedoIndex)
        self.currentCard = 0
        #if len(self.cardsToRedoIndex) > 0:
            #self.isReviewing = True

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
    reps.addCard("Canada", "Oh Canada", datetime.datetime.today().date())
    print(reps.repDataFrame.iloc[0])
    print(reps.repDataFrame.iloc[1])
    reps.allDone()
    #reps.removeCard(1)
    #print(reps.repDataFrame)
