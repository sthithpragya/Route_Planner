
# QUESTION 1
# Assuming the inputs and anagrams of t are single or a collection of multiple words made of alphabets only 
# Assuming case-sensitivity is important 
def question1(s, t):
	# case of invalid input
	if s == '' or t == '' or isinstance(s,str) == False or isinstance(t,str) == False:
		return 'invalid input'
	
	# Dealing with multi-word strings (assuming a single space between words), no space at beginning or end of string
	# total alphabets in s
	s_wo_space = s.replace(' ','')

	# total alphabets in t
	t_wo_space = t.replace(' ','')

	s_char_len = len(s_wo_space)
	t_char_len = len(t_wo_space)

	# case of invalid input when no substring of s can be of sufficient length for t
	if t_char_len > s_char_len:
		return 'invalid input'

	# spaces in s and t (incase of multiword string)
	spaces_in_s = s.count(' ')
	spaces_in_t = t.count(' ')

	# compensating for the spaces in t since an anagram of a single word maybe multiple words eg. funeral ~ real fun
	# assumed that a sub-string of s can also contain spaces eg. 'i am happy' can have a substring 'i a' which can return True if t = 'ai'
	if spaces_in_s > spaces_in_t:
		t = t + ' '*(spaces_in_s-spaces_in_t)

	s_len = len(s)
	t_len = len(t)
	num_of_iter = max(s_len - t_len, t_len - s_len) + 1
	1
	# finding the output (True or False)
	for i in range(num_of_iter):
		test_string = s[i:i+t_len]
		test_string_correct_substring = True
		T = t
		for char in test_string:
			char_in_t = False
			for j in range(len(T)):
				if char == T[j]:
					char_in_t = True
					# Removing the common element (b/w substring and t) to avoid repetition
					T = T[:j] + T[j+1:]
					break
			if char_in_t == False:
				test_string_correct_substring = False
				break

		if test_string_correct_substring == True:
			return True

	return False		

# Test case                                 #Output

print question1('happy',2) 					#invalid input
print question1('happy','') 				#invalid input
print question1('happy','app') 				#True
print question1('happy','sad') 				#False
print question1('ha ap py','s p p') 		#False
print question1('funEral','rEal fun') 		#True
print question1('forty five','over fifty')	#True
print question1('store scum','customers') 	#True
print '--------------------end of question1--------------------'

#----------------------End of question 1------------------------------------------------------------------------------------

# QUESTION 2
def question2(a):
	# case of invalid input
	if a == '' or isinstance(a,str) == False:
		return 'invalid input'

	# finding the longest substring to serve as a
	for i in range(len(a),0,-1):
		for j in range(len(a)-i+1):
			test_string_simple = a[j:j+i].lower().replace(' ','')
			reverse = test_string_simple[::-1]
			if test_string_simple == reverse:
				return a[j:j+i]


# Test case                                 #Output 

print question2('alole')					#'lol'
print question2(2)							#invalid input
print question2(None)						#invalid input
print question2('mark')						#m
print question2('A car a man a maraca')		#A car a man a maraca
print '--------------------end of question2--------------------'

#----------------------End of question 2------------------------------------------------------------------------------------

#QUESTION 3 (assuming the given input has all elements connected)

from operator import itemgetter
def question3(inp):

	if inp == {} or inp == None:
		return 'Invalid input'

	key_list = sorted(inp.keys()) 
	
	out = {} # dictionary to store output graph
	for vertex in key_list:
		out[vertex] = []
	
	edge_list = [] # list of edges contained in the graph (no repetition)
	for keys in key_list:
		tuple_list = inp[keys]

		i = 0
		if tuple_list[i][0] <= keys:
			while tuple_list[i][0] <= keys:
					i = i+1	
					if i == len(tuple_list):
						i = i-1
						break

		if tuple_list[i][0] > keys:	
			for tuples in tuple_list[i:]:
				edge_list.append((keys,tuples[0],tuples[1])) #(node1, node2, edge-length)

	#tuples of edge data sorted as per ascending order of edge-length		
	edge_list_asc = sorted(edge_list,key=itemgetter(2))

	final_edges = 0 # counter to track the edges in the output graph
	connection = [] # list to keep track of different sub-graphs to avoid formation of cycles. Each item of the list is a list containing the vertices of a single sub-graph

	def cycle_check(v1,v2,vertex_list):
	# helper function to check if cycle is being formed
	# vertex list is a list of subgraphs wherein each subgraph is represented via a list of vertices in it
	# v1_list - subgraph in which node1 or vertex1 'v1' is present
		if len(vertex_list) == 0: 
			return (0,0,0)
		else:
			v1_list = -1
			v2_list = -1
			for i in range(len(vertex_list)):
				if v1 in vertex_list[i]:
					v1_list = i 
					break
			for i in range(len(vertex_list)):
				if v2 in vertex_list[i]:
					v2_list = i
					break
			
			if v1_list == v2_list:
				if v1_list == -1:
					return (0,v1_list,v2_list) # the edge is independent since both its vertices don't belong to any sub-graph
				else:
					return (3,v1_list,v2_list) # the edge forms a closed cycle since both vertices belong to same sub-graph
			else:
				if v1_list == -1 and v2_list != -1: # one vertex is present in a subgraph whereas other isn't present in any
					return (1,v1_list,v2_list)
				elif v1_list != -1 and v2_list == -1: # one vertex is present in a subgraph whereas other isn't present in any
					return (2,v1_list,v2_list)
				else:
					return (4,v1_list,v2_list)  # both vertices present in different sub-graphs	

		
	def connection_add(v1,v2,vertex_list,n,v1_list,v2_list): #helper function to alter the connection list
		if n == 0: #making a new sub-graph of vertices v1 and v2 and adding it to list
			vertex_list.append([v1,v2])
		elif n == 1:
			vertex_list[v2_list].append(v1) #adding vertex v1 to subgraph containing v2
		elif n == 2:
			vertex_list[v1_list].append(v2) #adding vertex v2 to subgraph containing v1
		elif n == 4:
			vertex_list[v1_list] = vertex_list[v1_list] + vertex_list[v2_list] # joining together 2 subgraphs
			vertex_list = vertex_list[:v2_list] + vertex_list[v2_list+1:]
		else:
			pass

	while final_edges < len(key_list) - 1: #since in a MST, no of edges = no. of nodes - 1
		for i in range(len(edge_list_asc)):
			shortest_edge = edge_list_asc[i]

			node1 = shortest_edge[0]
			node2 = shortest_edge[1]

			check = cycle_check(node1,node2,connection)
			connection_add(node1,node2,connection,check[0],check[1],check[2])

			if check[0] != 3: # no cycles formed
				#adding edges to output graph
				out[node1].append((node2,shortest_edge[2])) 
				out[node2].append((node1,shortest_edge[2]))
				
				edge_list_asc = edge_list_asc[:i] + edge_list_asc[i+1:]
				
				final_edges = final_edges + 1
				break			

	return sorted(out.iteritems())

# Test case 1 
graph1 = {}
print question3(graph1)
#Output - "invalid input"

# Test case 2 
graph2 = {}
graph2['A'] = [('B',2)]
graph2['B'] = [('A',2),('C',5)]
graph2['C'] = [('B',5)]
print question3(graph2)
# Output - {'A': [('B', 2)], 'C': [('B', 5)], 'B': [('A', 2)]}

# Test case 3 
graph3 = {}
graph3['A'] = [('B',1)]
graph3['B'] = [('A',1),('C',5)]
graph3['C'] = [('B',5),('D',2)]
graph3['D'] = [('C',2)]

print question3(graph3)
# Output - [('A', [('B', 1)]), ('B', [('A', 1), ('C', 5)]), ('C', [('D', 2), ('B', 5)]), ('D', [('C', 2)])]

# Test case 4 
graph4 = {}
graph4['A'] = [('B',7),('D',5)]
graph4['B'] = [('A',7),('C',8),('D',9),('E',7)]
graph4['C'] = [('B',8),('E',5)]
graph4['D'] = [('A',5),('B',9),('E',15),('F',6)]
graph4['E'] = [('B',7),('C',5),('D',15),('F',8),('G',9)]
graph4['F'] = [('D',6),('E',8),('G',11)]
graph4['G'] = [('E',9),('F',11)]

print question3(graph4)
# Output - [('A', [('D', 5), ('B', 7)]), ('B', [('A', 7), ('E', 7)]), ('C', [('E', 5)]), ('D', [('A', 5), ('F', 6)]), ('E', [('C', 5), ('B', 7), ('G', 9)]), ('F', [('D', 6)]), ('G', [('E', 9)])]
print '--------------------end of question3--------------------'

#----------------------End of question 3------------------------------------------------------------------------------------

#QUESTION 4
import numpy as np
def question4(T, r, n1, n2):

	if T == [] or T == None:
		return 'Invalid input'

	#finding ancestry of n1
	num_of_nodes = len(T)
	T = np.array(T)
	
	n1_anc = T[:,n1]
	n1_anc_list = [] #list of nodes from n1 leading to the root
	while np.array_equal(n1_anc,[0]*num_of_nodes) == False: #until we reach the root
		current_parent = np.nonzero(n1_anc)[0][0]
		n1_anc_list.append(current_parent)
		n1_anc = T[:,current_parent] 

	n2_anc = T[:,n2]
	n2_anc_list = [] #list of nodes from n2 leading to the root
	while np.array_equal(n2_anc,[0]*num_of_nodes) == False: #until we reach the root
		current_parent = np.nonzero(n2_anc)[0][0]
		n2_anc_list.append(current_parent)
		n2_anc = T[:,current_parent]

	n1_anc_list.reverse() #list from root to n1
	n2_anc_list.reverse() #list from root to n2

	len1 = len(n1_anc_list)
	len2 = len(n2_anc_list)

	if len1 > len2:
		n2_anc_list = n2_anc_list + (len1-len2)*[-1]
	else:
		n1_anc_list = n1_anc_list + (len2-len1)*[-1]

	common_anc_list = np.array(n1_anc_list) - np.array(n2_anc_list)
	common_anc_list = np.ndarray.tolist(common_anc_list)

	if cmp(common_anc_list, len(common_anc_list)*[0]) == 0: #returns root when both the ancestry lists are same
		return r

	lca_index = np.nonzero(common_anc_list)[-1][0] - 1 #last common element
	lca = n1_anc_list[lca_index] 
	return lca

#Test case 1	

print question4([[0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [1, 0, 0, 0, 1],
           [0, 0, 0, 0, 0]],
          3,
          1,
          4)
#Output - 3

#Test case 2
print question4([],3,1,4)
#Output - "invalid input"

#Test case 3
print question4([[0, 0, 0, 0, 0],
           [1, 0, 1, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 1, 0, 0, 1],
           [0, 0, 0, 0, 0]],
          3,
          1,
          4)
#Output - 3
print '--------------------end of question4--------------------'

#----------------------End of question 4------------------------------------------------------------------------------------

#QUESTION 5
class Node(object):
  def __init__(self, data):
    self.data = data
    self.next = None

def question5(ll, m):
	if ll == None:
		return 'invalid input'

	data_list = [] # list which stores the data value of nodes from head to tail
	current = ll
	while current.next != None:
		data_list.append(current.data)
		current = current.next
	
	data_list.append(current.data)

	if m <= 0 or m > len(data_list):
		return 'invalid input'
	else:	
		return data_list[len(data_list) - m]


#Test cases

class LinkedList(object):
    def __init__(self, head=None):
        self.head = head
        
    def app(self, new_element):
        current = self.head
        if self.head:
            while current.next:
                current = current.next
            current.next = new_element
        else:
            self.head = new_element


#Test case 1

e11 = Node(1)
e12 = Node(2)
e13 = Node(3)
e14 = Node(4)

L1 = LinkedList(e11)
L1.app(e12)
L1.app(e13)
L1.app(e14)

ll1 = L1.head
print question5(ll1,3)

# Output - 2

#Test case 2

e21 = None

L2 = LinkedList(e21)

ll2 = L2.head
print question5(ll2,1) 

# Output - 'invalid input'

#Test case 3

e31 = Node(1)
e32 = Node(2)
e33 = Node(3)
e34 = Node(4)
e35 = Node(5)
e36 = Node(6)
e37 = Node(7)
e38 = Node(8)

L3 = LinkedList(e31)
L3.app(e32)
L3.app(e33)
L3.app(e34)
L3.app(e35)
L3.app(e36)
L3.app(e37)
L3.app(e38)

ll3 = L3.head
print question5(ll3,11) 
print question5(ll3,2)
print question5(ll3,-3)
print question5(ll3,5)

# Output - 'invalid input', 7, 'invalid input', 4

print '--------------------end of question5--------------------'