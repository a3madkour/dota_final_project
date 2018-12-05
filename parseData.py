import json

if __name__ == '__main__':

    with open('gameConstants/heroes.json') as inputFile:
        heroes = json.load(inputFile)    

    print(heroes)
