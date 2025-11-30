import pandas as pd
import numpy as np

class DTNode:
    def __init__(self, attribute: str):
        self.attribute = attribute
        self.children = {}
        self.is_leaf = False
        self.label = None

    def add_child(self, key: str, node):
        self.children[key] = node

class Leaf:
    def __init__(self, label: str):
        self.label = label
        self.is_leaf = True

class DTClassifier:

    def __init__(self):
        self.tree = None

    def calculate_entropy(self, S: pd.DataFrame) -> float:
        '''
        Calculates the entropy (a.k.a information content) of the set of 
        examples contained in a dataset S using pandas and numpy for more 
        efficient computation.

        H(S) = -Sigma_{i in classes(S)} P_i * log_2(P_i)

        where P_i is the proportion of examples that belong to class i.
        '''
        
        class_counts = S["class"].value_counts()
        probabilities = class_counts / len(S)
        entropy = -np.sum(probabilities * np.log2(probabilities))
        
        return entropy

    def calculate_info_gain(self, S: pd.DataFrame, A: str):
        '''
        Information gain, Gain(S|A) measures the reduction in entropy caused by 
        partitioning the set of examples S using attribute A.

        Gain(S|A)   = H(S) - H(S|A)
                    = H(S) - Sigma_{j in values(A)} P(A = v_j) * H(S|A = v_j)
                    = H(S) - Sigma_{j in values(A)} |S_vj|/|S| * H(S|A = v_J)
        '''
        
        H_s = self.calculate_entropy(S)

        # Find the possible values of A
        values_A = S.loc[:, A].unique()

        n = len(S)
        summation = 0
        for j in values_A:
            # Partition S on A
            subset_j = S[S.loc[:, A] == j]

            subset_prop = len(subset_j) / n
            subset_entropy = self.calculate_entropy(subset_j)

            summation += subset_prop * subset_entropy
        
        return H_s - summation
    
    def select_best_attribute(self, S: pd.DataFrame) -> str:
        '''
        The best attribute to split a dataset on is the attribute which 
        maximises the information gain. Returns this attribute's name.
        
        Returns -1 if all attributes have the same information gain or
        or if no attribute provides a positive information gain.
        '''

        gains = {}
        for A in S.columns:
            if A == "class":
                continue
            gains[A] = self.calculate_info_gain(S, A)
        
        max_gain = max(gains, key=gains.get)
        
        if len(set(gains.values())) == 1 or gains[max_gain] <= 0:
            return -1

        return max_gain
    
    def mode(self, S: pd.DataFrame, col_index=-1) -> str:
        if len(S) == 1:
            return S.iloc[:, col_index]
        
        num_yes = S[S.iloc[:, col_index] == "yes"].shape[0]
        num_no = S[S.iloc[:, col_index] == "no"].shape[0]
        
        if num_yes >= num_no:
            return "yes"
        else:
            return "no"
        
    def build_tree(self, S: pd.DataFrame, parent_class: str):
        # Stopping Criteria c): The subset is empty.
        # Return a leaf node with the majority class of the parent's subset.
        if len(S) == 0:
            return Leaf(parent_class)
        
        # STOPPING CRITERIA a): All examples in the subset have the same class.
        # Return a leaf node of that class.
        if len(S.loc[:, "class"].unique()) == 1:
            _class = S.loc[:, "class"].unique()[0]
            return Leaf(_class)
        
        best_attr = self.select_best_attribute(S)
        
        # STOPPING CRITERIA b): All examples in the subset have the same 
        # attribute values but different class labels.
        # Return a leaf node with the majority class.
        if best_attr == -1:
            mode = self.mode(S)
            return Leaf(mode)

        node = DTNode(best_attr)
        attr_unique = S.loc[:, best_attr].unique()
        for val in attr_unique:
            branch_subset = S[S.loc[:, best_attr] == val]
            branch_subset = branch_subset.drop(best_attr, axis=1)
            child_node = self.build_tree(branch_subset, self.mode(S))
            node.add_child(val, child_node)
        
        return node

    def fit(self, train: pd.DataFrame):
        '''
        Builds a decision tree given a dataset containing n features and a
        class attribute. Follows the ID3 procedure as below:

        1. Select the best attribute for the root node
        2. Create a new branch for each possible attribute value
        3. Split the dataset to contain the rows which fulfill each attribute 
        value
        4. Repeat the procedure for each branch using only the entries which 
        reach the branch
        5. Stop according to the stopping criteria and make a leaf node 
        accordingly
        '''
        # Add temporary columns
        cols = []
        for i in range(len(train.columns) - 1):
            cols.append(chr(ord('a') + i))
        cols.append("class")
        train.columns = cols
        
        self.tree = self.build_tree(train, self.mode(train))
    
    def predict_example(self, X: pd.Series) -> str:
        '''
        Predicts the class of one example i.e. n input attributes.
        '''
        ptr = self.tree
        while not ptr.is_leaf:
            attribute_to_check = ptr.attribute
            attribute_value = X[attribute_to_check]

            # Handle the case where attribute_value is not in ptr.children
            if attribute_value not in ptr.children:
                return "yes"
                
            ptr = ptr.children[attribute_value]
            
        return ptr.label

    def predict(self, X):
        if type(X) == pd.DataFrame:
            # Add temporary columns
            cols = []
            for i in range(len(X.columns)):
                cols.append(chr(ord('a') + i))
            X.columns = cols
            
            predictions = []
            for _, row in X.iterrows():
                predictions.append(self.predict_example(row))
            return predictions
        else:
            raise Exception("Input must be of type pandas.DataFrame")
    
    def print_tree(self, node=None, depth=0, value=None):
        if node is None:
            node = self.tree
        
        prefix = "-" * (depth * 2)
        
        if depth == 0:
            print(f"Root: splits on '{node.attribute}'")
        else:
            if node.is_leaf:
                print(f"{prefix}|- {value} [Leaf] Class: {node.label}")
            else:
                print(f"{prefix}|- [Value: {value}] -> Node: splits on '{node.attribute}'")
        
        if not node.is_leaf:
            for val, child in node.children.items():
                self.print_tree(child, depth + 1, val)

def classify_dt(training_filename, testing_filename):
    train = pd.read_csv(training_filename, header=None)
    test = pd.read_csv(testing_filename, header=None)
    
    dt = DTClassifier()
    dt.fit(train)
    
    return dt.predict(test)

#classify_dt("pima_train.csv", "pima_test.csv")