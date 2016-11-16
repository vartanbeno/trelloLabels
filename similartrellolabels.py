#!/usr/bin/env python

"""
Scans a Trello project for its cards, pulls their label names, and puts them in a list.
Detects similarly named labels via a user input.
Saves the user input, deletes the label names similar to it from the list,
but doesn't modify any Trello data.
"""

import difflib			# provides classes and functions for comparing sequences/files
# import Trello API
from trello import TrelloApi, Boards, Cards

__author__ = "Vartan Benohanian"
__version__ = "1.0.0"
__maintainer__ = "Vartan Benohanian"
__email__ = "vartanbeno@gmail.com"

def search(labels, lowercase_labels, good_labels, word):
	"""
	Look for label names in the labels that are similar to word.

	Args:
		word (str): string we want words exact/similar to.
		labels (list): list containing label names from the Trello project, as they are.
		lowercase_labels (list): list containing label names from the Trello project, all lowercase letters.
		good_labels (list): originally empty list, in which we will add word.
	Returns:
		None.
	"""

	similar_words = difflib.get_close_matches(word.lower(), lowercase_labels, n = 10, cutoff = 0.5)
	# using the lowercase list to compare with the word on an even field
	# optional parameter n is the max number of matches it looks for, 3 by default
	# optional parameter cutoff, range [0,1], is the min value of similarity for a word to be included, 0.6 by default, 0.5 here for better detection
	if len(similar_words) > 0:				# only add label to new_list if similar words were found
		print("The following labels' names are exact/similar to \"%s\":" % word)
		for x in similar_words:
			print(labels[lowercase_labels.index(x)])
			del labels[lowercase_labels.index(x)]				# delete bad label name from list...
			del lowercase_labels[lowercase_labels.index(x)]		# ...and from lowercase list...
		good_labels.append((word.lower()).capitalize())			# ...and add word (with capital 1st letter) to new_list
	else:
		print("Try another label name.")

	print("\n")

app_key = "b7f9422ee3cf641e1d9321a0aca2a3f8"
trello = TrelloApi(app_key)					# dev's API key

boardId = "5829187a5e792f5951a9363c"		# ID of the board we're working on

print("Copy/paste the following link in your web browser to get a new token.")
print(trello.get_token_url("Similar Label Detector", expires="30days", write_access=True))
# visit site to get 64-character token
# token given by website
auth_token = "744be46a0777522b10e26f42a819274dcbdc490bfc6d927960dc555d0fdb94b7"
trello.set_token(auth_token)

cards = Cards(app_key, auth_token)
boards = Boards(app_key, auth_token)

cardIds = []			# empty list where we will store card ID's
label_names = []		# empty list where we will store unmodified label names
label_names_lc = []		# empty list where we will store lowercase label names

print("List of cards, their respective ID's, and their respectiev label names:")

for x in range(0, len(boards.get_card(boardId))):			# 0 to 9, because 10 cards
	y = boards.get_card(boardId)[x]							# get every individual card's info
	card = y["name"]										# get card's description
	card_id = y["shortLink"]								# get card's ID
	# exception handling: some cards have no label whatsoever, so the "name" key doesn't exist in the "label section"
	try:
		label = cards.get(card_id)["labels"][0]["name"]		# get label name
		# "labels" in the JSON essentially consists of 1 library constaining a few (key, value) pairs. That's why index = 0
	except IndexError:
		label = ""
	print("%-34s || %-5s || %14s" % (card, card_id, label))		# formatting
	cardIds.append(card_id)										# add card ID's to list
	if label != "":								# if label doesn't have a name, don't do anything with it
		label_names.append(label)				# add label names to list
		label_names_lc.append(label.lower())	# add lowercase label names to list
	# label names all set to lowercase to help with comparison later on

# remove the 'u' that's part of the unicode, for better presentation
label_names = [str(label_names[x]) for x in range(0, len(label_names))]					# 1st argument in search()
label_names_lc = [str(label_names_lc[x]) for x in range(0, len(label_names_lc))]		# 2nd argument in search()
print("\nHere are the labels used in the Trello project. There are most likely some that are similar. The app will find similar ones based on your input, delete those, and preserve the input.")
print(label_names)
print("\n")

new_list = []			# 3rd argument in search(), empty list where we will store new label names

# let user input desired label names into application
while len(label_names) != 0:		# loop will stop as soon as no other label left to correct
	word = raw_input("What label name would you like to test? To terminate the program, don't input anything and simply press the enter key.\n")
	# 4th argument in search()
	if word == "":
		break
	search(label_names, label_names_lc, new_list, word)

# reprint label_names, this time with new, well-spelled label names
print("\nHere's the modified, shortened list of the label names:")
print(new_list)

if len(label_names) != 0:
	print("\nHere are the leftover label names from the original bunch:")
	print(label_names)
else:
	print("\nGreat! There aren't any label names left from the original bunch.")