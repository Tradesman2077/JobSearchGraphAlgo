import networkx as nx
import matplotlib.pyplot as plt
import json
import operator
from datetime import datetime
#Search that uses networkx nodes and edges to rank jobs based on specific set skills
#class for result_nodes
class Result(object):
    def __init__(self, title, text, edges, job_score, skills):
        self.title = title
        self.text = text
        self.edges = edges
        self.job_score = job_score
        self.skills = skills

#function that checks how much the skill is weighted and returns the score.
def Score_finder(skill):
    score = 0
    if (user, skill) in weights:
        score+=weights[(user, skill)]
    return score
###take user input for name and soft skills first 
username_input= input('Please enter your username: ')
soft_skills_input= {}
hard_skills_input= {}
exit =False
while exit == False:
    skill=input('Enter a soft skill, or type "skip" when finished: ')
    if skill != 'skip':
        weight=input('Enter a weighting between one and ten: ')
        try:
            soft_skills_input[skill]=int(weight)
        except:
            print('invalid entry')
            continue         
    else:
        exit = True
#then hard skills
exit =False
while exit == False:
    skill=input('Enter a hard skill, type "skip" when finished: ')
    if skill != 'skip':
        weight=input('Enter a weighting between one and ten: ')
        try:
            hard_skills_input[skill]=int(weight)
        except:
            print('invalid entry')
            continue
    else:
        exit = True
##start timing how long for execution  of code
startTime = datetime.now()
###assign input data to json file
with open('data/single_user.json') as f:
    data = f.read()
d = json.loads(data)
d[0]["username"] = username_input
d[0]["soft_skills"] = soft_skills_input
d[0]["hard_skills"] = hard_skills_input
with open('data/single_user.json', 'w') as f:
    f.write(json.dumps(d, sort_keys=True, indent=4, separators=(',', ': ')))
with open('data/jobs.json', 'r')as infile:
    jobs_array = json.load(infile)
with open('data/single_user.json', 'r') as infile:
    users_array = json.load(infile)
#create graph
G =nx.Graph()
soft_skills = []
hard_skills = []
#add user node and look for skills and add nodes and edges for each
for obj in users_array:
    G.add_node(obj['username'], node_type='user')
    user = obj['username']
    # if user has soft skills
    if 'soft_skills' in obj:
        for key, value in obj['soft_skills'].items():
            #add node
            G.add_node(key, color='r')
            soft_skills.append(key)              
            # add edge
            G.add_edge(obj['username'], key, weight =obj['soft_skills'][key])
#add hard skills
    if 'hard_skills' in obj:
            for key, value in obj['hard_skills'].items():
                #add node
                G.add_node(key, color='g')
                hard_skills.append(key)
                # add an edge
                G.add_edge(obj['username'], key, weight =obj['hard_skills'][key])

#list of all skills found from user
full_skills = soft_skills + hard_skills
#print(full_skills)
# list of weighted skills
weights = (nx.get_edge_attributes(G, 'weight'))

for obj in jobs_array:
    # each job is a node if matched
    job_score = 0
    for skill in full_skills:
        if skill in obj['text']:
            #check the value of weighted skill
            job_score += Score_finder(skill)
            if not G.has_node(obj['title']):                
                G.add_node(obj['title'], text=obj['text'],title = obj['title'], color = 'b')              
            G.nodes[obj['title']]['job_score']= job_score
            G.add_edge(obj['title'], skill)

if nx.get_node_attributes(G,'text') == False:
        print('no match')
#put nodes into lists for drawing
color_list = nx.get_node_attributes(G,'color')
red_skills = [ key for key, value in color_list.items() if value == 'r' ]
green_skills = [ key for key, value in color_list.items() if value == 'g' ]
jobs = nx.get_node_attributes(G,'text')
users = nx.get_node_attributes(G,'node_type')
pos=nx.spring_layout(G)
#draw nodes
nx.draw_networkx_nodes(G, pos, 
            nodelist=red_skills, 
            node_color='r', 
            node_size=20,           
            with_labels=True, 
            font_weight='normal')
nx.draw_networkx_nodes(G, pos, 
            nodelist=green_skills, 
            node_color='g', 
            node_size=20,   
            with_labels=True, 
            font_weight='normal')
nx.draw_networkx_nodes(G, pos, 
            nodelist=users, 
            node_color='m', 
            node_size=40, 
            with_labels=True, 
            font_weight='normal')
nx.draw_networkx_nodes(G, pos, 
            nodelist=jobs, 
            node_color='b', 
            node_size=30, 
            with_labels=True, 
            font_weight='normal')
#draw edges
nx.draw_networkx_edges(G, pos, edge_color='gray')
#create a list of node objects that contain matched nodes and the number of edges and scores
results_nodes =[]
for i in jobs:
    x = Result(G.nodes[i]['title'], G.nodes[i]['text'], len(G.edges(i)), G.nodes[i]['job_score'], [n for n in G.neighbors(i)])    
    results_nodes.append(x)
#sort by job score
results_nodes.sort(key=lambda x: x.job_score, reverse=True)
print('Here are the results: \n')
print('Time taken for search: '+ str(datetime.now() - startTime)+'\n')
#display the results
for i in results_nodes:    
    print(f'/// Job-Title : {i.title}///\n')
    print(f'Job-Text : {i.text}')
    print(f'Job-Score : {i.job_score}')
    print(f'Matched skills : {i.skills}')
    print(f'Number of Edges : {i.edges}\n')
if len(results_nodes) == 0:
    print('No match')
plt.savefig("single_user.png") # save as png
plt.show() # display

    