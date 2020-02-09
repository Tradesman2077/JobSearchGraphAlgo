import networkx as nx
import matplotlib.pyplot as plt
import json
import operator

with open('data/test_user.json', 'r') as infile:
    users_array = json.load(infile)


#function taken from main program with the networkx elements taken out

def user_skill_finder(users_array):
	soft_skills = []
	for obj in users_array:
		user = obj['username']
		if 'soft_skills' in obj:
			for key, value in obj['soft_skills'].items():
				soft_skills.append(key)
		
	return soft_skills



def test(users_array):
	#tests test_user.json

    #arrange
	test_check = ['communication', 'problem-solving']

    #assert
	if user_skill_finder(users_array)==test_check:
        #act
		print('Pass')
	else:
		print('Fail')


test(users_array)