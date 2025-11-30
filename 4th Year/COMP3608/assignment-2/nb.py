import pandas as pd
import numpy as np

class GaussianNaiveBayes():

    def __init__(self):
        self.means = {}
        self.stds = {}
        self.priors = {}
        self.n = 0
        self.labels = []

    def fit(self, train: pd.DataFrame):
        self.n = len(train.columns) - 1

        # Calculate the means, stds, and prior probabilities for each label
        self.labels = train.iloc[:, -1].unique()
        for label in self.labels:
            train_subset = train[train.iloc[:, -1] == label].iloc[:, :-1]
            self.means[label] = train_subset.mean()
            self.stds[label] = train_subset.std()
            self.priors[label] = len(train_subset) / len(train)

    def calculate_likelihood(self, x, mean, std):
        '''
        Approximates P(X = x | Y = y) as f(X = x | Y = y) where f is the 
        Gaussian function.
        '''
        
        # Avoid division by zero in case standard deviation = 0
        if std == 0:
            std = 0.0001
        return (1 / (np.sqrt(2 * np.pi) * std)) * np.exp(-((x - mean) ** 2) / (2 * std ** 2))

    def predict(self, test: pd.DataFrame):
        '''
        Given a testing dataset (n features with no labels), return a list of
        labels corresponding to the classification of each row.
        
        Methodology:
        For each row in the prediction dataset, this function will return a 
        value of y (out of all possibilities Y, which in our case is simply 
        "yes" or "no) which maximises P(Y = y_i | X = (x_1, ..., x_n)).

        Applying Bayes (ignoring the denominator as it is independent of y):
        P(Y = y_i | X = (x_1, ..., x_n)) = P(X = (x_1, ..., x_n) | Y = y) * P(Y = y)

        Then, applying the assumption of conditional independence:
        P(Y = y_i | X = (x_1, ..., x_n)) = Pi {P( X_i = x_i | Y = y )} * P(Y = y)

        We have already calculated the prior probabilities for all labels in our
        fit() function. So, all we do is loop through each value x_i in the row 
        X and calculate P(X_i = x_i | Y = y),  the likelihood, using 
        the Gaussian function.

        - Although this assignment only covers binary classification, this
        program works with any number of labels.
        - Assumes the label column is the last column in the dataframe.
        - Assumes the test dataframe has no header row (data only).
        '''       

        classifications = []
        for _, row in test.iterrows():
            posteriors = {}
            for label in self.labels:
                # Start with the prior probability
                likelihood = self.priors[label]
                
                # Calculate the likelihood for every value x_i in X
                for i in range(self.n):
                    x_i = row[i]
                    mean = self.means[label][i]
                    std = self.stds[label][i]
                    likelihood *= self.calculate_likelihood(x_i, mean, std)

                posteriors[label] = likelihood
            
            # Choose the greatest of all the labels for the current row
            classifications.append(max(posteriors, key=posteriors.get))
        
        return classifications
    
def classify_nb(training_filename, testing_filename):
    train = pd.read_csv(training_filename, header=None)
    test = pd.read_csv(testing_filename, header=None)
    
    model = GaussianNaiveBayes()
    model.fit(train)
    classifications = model.predict(test)
    
    return classifications