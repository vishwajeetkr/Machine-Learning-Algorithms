import numpy as np
import pdb

my_data = np.genfromtxt('data__1.csv', delimiter=',')
X_test = np.genfromtxt('data__2.csv', delimiter=',')

bool_list = []
list_num = 0
for i in range(my_data.shape[1]-1):
    bool_list.append(False)

parent_data = np.array(my_data)
current_data = parent_data
number_true_example = 0
number_false_example = 0
for i in range(my_data.shape[0]):
    if my_data[i][my_data.shape[1]-1] == 0:
        number_false_example += 1
    else:
        number_true_example += 1
parent_entropy = -(number_true_example/my_data.shape[0])*np.log(number_true_example/my_data.shape[0])-(number_false_example/my_data.shape[0])*np.log(number_false_example/my_data.shape[0])

def find_entropy(data, index):
    number_true = 0
    number_false = 0
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for i in range(data.shape[0]):
        if data[i][index] == 1:
            number_true += 1
            if data[i][data.shape[1]-1] == 1:
                true_positive +=1
            else:
                true_negative += 1
        else:
            number_false += 1
            if data[i][data.shape[1]-1] == 1:
                false_positive +=1
            else:
                false_negative += 1
    if true_positive == number_true or true_negative == number_true:
        true_entropy = 0
    else:
        true_entropy = -(true_positive/number_true)*np.log(true_positive/number_true)-(true_negative/number_true)*np.log(true_negative/number_true)
    if false_positive == number_false or false_negative == number_false:
        false_entropy = 0
    else:
        false_entropy = -(false_positive/number_false)*np.log(false_positive/number_false)-(false_negative/number_false)*np.log(false_negative/number_false)
    total_entropy = (number_true/data.shape[0])*true_entropy + (number_false/data.shape[0])*false_entropy
    return total_entropy


def check_bool_array(bool_list):
    flag = 0
    for i in range(len(bool_list)):
        if bool_list[i] == False:
            flag = 1
    if flag == 1:
        return True
    else:
        return False

def subtreeIndex(bool_list, current_data, parent_entropy):
    max_entropy_gain = 0
    root_index = -1
    current_entropy = 2.0
    for i in range(len(bool_list)):
        if bool_list[i] == False:
            temp = find_entropy(current_data, i)
            entropy_gain = parent_entropy - temp
            if entropy_gain > max_entropy_gain:
                max_entropy_gain = entropy_gain
                root_index = i
                current_entropy = parent_entropy - max_entropy_gain
    return (root_index, current_entropy)
root_index, parent_entropy = subtreeIndex(bool_list, current_data, parent_entropy)

def check_same(data):
    temp = data[0][data.shape[1]-1]
    for i in range(data.shape[0]):
        if temp != data[i][data.shape[1]-1]:
            return False
    return True

class Node:
    
    def __init__(self, num):
        self.data = num
        self.left = None
        self.right = None
        self.array_data = None
    

def find_max(node):
	index = node.data
	positive_example = 0
	negative_example = 0
	for i in node.array_data:
		if parent_data[i][parent_data.shape[1]-1] == 0:
			negative_example += 1
		else:
			positive_example += 1
	if positive_example > negative_example:
		return 1
	else:
		return 0
class BDT:
    
    def __init__(self, num):
        self.root = Node(num)
    def get_root(self):
        return self.root
    
    def draw_tree(self, bool_list, node, current_data, list_num, current_index_array):
        root_index = node.data
        #pdb.set_trace()
        while list_num < len(bool_list):
            flag = 0
            left_data = current_data[current_data[:,root_index]==0,:]
            left_index_array = []
            right_index_array = []
            for i in current_index_array:
            	if parent_data[i][root_index] == 0:
            		left_index_array.append(i)
            	else:
            		right_index_array.append(i)
            right_data = current_data[current_data[:,root_index]==1,:]
            
            if check_same(left_data):
                if left_data[0][left_data.shape[1]-1]==0:
                    node.left = False
                else:
                    node.left = True
            else:
                flag = 1
                left_child, left_entropy = subtreeIndex(bool_list, current_data, parent_entropy)
                bool_list[left_child] = True
                list_num += 1
                node.left = Node(left_child)
                node.left.array_data = left_index_array
                self.draw_tree(bool_list, node.left, left_data, list_num, left_index_array)
            if check_same(right_data):
                if right_data[0][right_data.shape[1]-1]==0:
                    node.right = False
                else:
                    node.right = True
            else:
                flag = 1
                right_child, right_entropy = subtreeIndex(bool_list, current_data, parent_entropy)
                bool_list[right_child] = True
                list_num += 1
                node.right = Node(right_child)
                node.right.array_data = right_index_array
                self.draw_tree(bool_list, node.right, right_data, list_num, right_index_array)
            if flag == 0:
                break
    def predict(self, data):
        result = np.zeros(data.shape[0])
        for i in range(data.shape[0]):
            node = self.root
            
            while True:
                if type(node) == bool and node == True:
                    result[i] = 1
                    break
                elif type(node) == bool:
                    result[i] = 0
                    break
                value = node.data
                if data[i][value] == 0:
                    if node.left == None:
                    	result[i] = find_max(node)
                    	break
                    
                    node = node.left
                else:
                	if node.right == None:
                		result[i] = find_max(node)
                		break
                	node = node.right
                print("a")
        return result
dt_graph = BDT(root_index)
bool_list[root_index] = True
list_num += 1
root = dt_graph.get_root()
current_index_array = [i for i in range(len(current_data))]
root.array_data = current_index_array
dt_graph.draw_tree(bool_list, root, current_data, list_num, current_index_array)
y_test = dt_graph.predict(X_test)
print(y_test)