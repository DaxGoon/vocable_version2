# vocable_version2
Vocable version 2 game in Python 3.

This is the current version of the vocable game in Python developed using version 3.6. 
This repository contains the whole virtual environment and external libraries.

Vocable is a multiplayer game of words. 

Here are some rules of the game:

    --------------------------------
    1. Start with spelling a valid unique word in your chosen language
    2. Your opponent must spell a word starting with the end character of your word
    3. The game continues in a loop
    4. If you enter an invalid word or used word, 1 pass will be taken from your account
    5. You have 3 passes, when the 3rd is taken, you're out of the game
    6. Last remaining person wins the game

Current version of the game supports words in:
    1. US English
    2. UK English
    3. French
    4. German

*The spell checking is done in this game via pyenchant library which is also used in office suite software such as OpenOffice.*
