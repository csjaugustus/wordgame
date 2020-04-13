#coding: utf-8
from random import shuffle,sample,choice
import json

class Player():
    def __init__(self,score=0,words=[]):
        self.words = words
        self.score = score
        self.total_questions = len(db.wordlist)
    
    def show_score(self):
        accuracy = "{:.1%}".format(self.score/(50-len(self.words)))
        print("Words guessed: {}\nScore: {}/50.\nAccuracy: {}".format(50-len(self.words),self.score, accuracy))

class Database():
    def __init__(self, filename):
        self.filename = filename
        self.wordlist = []
        self.words = []
        self.load_words()
        self.load_data()
        
    def load_words(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            self.wordlist = [i.strip().split("$") for i in f]
        print("Loading 50 words from your file...")
        print("File {} loaded.".format(self.filename))
        print("\n")
        
    def load_data(self):
        #Created empty saved file if it does not exist
        try:
            with open("data.json") as f:
                pass
        except:
            with open("data.json", "w") as f:
                json.dump({}, f)
        #Load saved data
        with open("data.json") as f:
            data_dict = json.load(f)
            for key, value in data_dict.items():
                self.score = int(key)
                self.words = value
        if self.words:
            print("Saved data found.")
            accuracy = "{:.1%}".format(self.score/(50-len(self.words)))
            print("Words guessed: {}/50\nScore: {}/50\nAccuracy: {}".format(50-len(self.words),self.score,accuracy))
            print("\n")
        else:
            print("No data found. New game.\n")

def shuffle_word(word):
    lst = list(word)
    shuffle(lst)
    return "".join(lst)

def after_game(current_list):
    player.show_score()
    if not current_list:
        print("Game over.")
        exit()
    prompt = input("Type anything to continue.")
    print("\n")

def save_game(current_list):
    data_dict = {player.score : current_list}
    with open("data.json", "w") as f:
        json.dump(data_dict,f)

def game():
    while True:
        #pick a word from 50
        random_word_pair = choice(current_list)
        random_word = random_word_pair[0]
        random_word_meaning = random_word_pair[1]
        shuffled_word = shuffle_word(random_word)
        letters_shown = 1   #initial value
        tries = 2    #initial value
        
        while True:
            if display == "with chinese":
                print("Your word: {} {}".format(shuffled_word,random_word_pair[1]))
            elif display == "without chinese":
                print("Your word: {}".format(shuffled_word))
            if letters_shown == 1:
                print("The first letter is {}.".format(random_word[0]))
            else:
                print("The first {} letters are {}.".format(letters_shown,"".join(random_word[:letters_shown])))
            guess = input()
            print("\n")
            
            if not guess.isalpha():
                print("Enter letters only!")
                continue
            elif guess == "h":
                if letters_shown == 4:
                    print("You have no more hints left.")
                    continue
                letters_shown += 1
                print("You have {} hints left.".format(4-letters_shown))
                continue
            elif guess == "s":
                print("The answer was {}.".format(" ".join(random_word_pair)))
            elif guess == random_word:
                print("Correct!")
                print(" ".join(random_word_pair))
                player.score += 1
            else:
                if tries == 0:
                    print("Wrong. The answer was: {}.".format(" ".join(random_word_pair)))
                else:
                    print("Wrong. {} more tries.".format(tries))
                    tries -= 1
                    continue
                
            current_list.remove(random_word_pair)
            player.words = current_list
            save_game(current_list)
            after_game(current_list)
            break

db = Database("newconc1.txt")

#pick 50 words from file, exit program if file does not have 50 words
try:
    current_list = sample(db.wordlist, 50)
except:
    print("Not enough words in your list. Add at least 50 words.")
    exit()
    
#load data
if not db.words:
    player = Player()
else:
    while True:
        pchoice = input("'r' - Resume game.\n'n' - Clear data, start new game.\n")
        print("\n")
        
        if pchoice == "r":
            player = Player(db.score, db.words)
            current_list = db.words
            print("Data loaded. Resuming game.\n")
            break
        elif pchoice == "n":
            player = Player()
            with open("data.json", "w") as f:
                json.dump({},f)
            print("Data cleared. Starting new game.\n")
            break
        else:
            print("Enter 'r' or 'n' only.\n")
            continue

print("'h' - Hint (maximum 3).\n's' - Show answer.\n")
#choose mode
while True:
    modechoice = input("Show Chinese meaning beside scrambled word?\n'y' - Yes\n'n' - No\n")
    if modechoice == "y":
        display = "with chinese"
        break
    elif modechoice == "n":
        display = "without chinese"
        break
    else:
        continue
print("\n")
game()
