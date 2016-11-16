# similartrellolabels.py

This Python program detects similarly named labels from a Trello project. The user will be prompted to input a label name, which will be kept in a list. Based on the user inputted word, similar label names will be detected. [Used project in this example.](https://trello.com/b/xj18FzNH/new-project)

# Building

For the program to work, you must install the Python Trello API library found [here.](https://github.com/tghw/trello-py)

# Running

First, get your application key from here and paste it at the corresponding place in the Python program.

Next, go to your Trello project on your browser, add .json at the end of the link, press enter. Copy the ID of the board: ["actions"][0]["data"]["board"]["id"]. Paste it at the corresponding place in the Python program.

Next, run the program and copy/paste the link outputted. Once you allow the app to use your account, you will be granted a 64-character authorization key. Paste it at the corresponding place in the Pythong program. This is important if the project board is set to private.
