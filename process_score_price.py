"""
Script for classifying green coffee processing method based on its price and score

Transforms the data using 'processes.py', visualizes the data, creates k-Nearest Neighbors and Fixed-Radius Near
Neighbors Classifiers and fits them on the training set, tests the models on the testing set

Requires installation of 'pandas', 'matplotlib', 'scikit-learn'
"""

import pandas
import adjust_data
import processes
from matplotlib import pyplot
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier

print('\nClassifying green coffee processing method based on its price and score...')

# read relevant training data from the adjusted file
data = pandas.read_csv('adjusted_data.csv')
train_features = data[['Score', 'Price']]
train_processes = data['Process']
# drop rows with missing values using 'adjust_data.py'
train_features, train_processes = adjust_data.drop_missing(train_features, train_processes)

# read relevant testing data from the adjusted file
test_data = pandas.read_csv('adjusted_test_data.csv')
test_features = test_data[['Score', 'Price']]
test_processes = test_data['Process']
# drop rows with missing values using 'adjust_data.py'
test_features, test_processes = adjust_data.drop_missing(test_features, test_processes)

# transform training and testing data using 'processes.py'
# (simplify processing method names to integer ids, print the mapping for reference)
train_features, train_processes, test_features, test_processes \
    = processes.simplify_processes(train_features, train_processes, test_features, test_processes, print_map=True)

# plot the data
pyplot.scatter('Score', 'Price', data=train_features, c=train_processes, cmap='gist_rainbow')
pyplot.colorbar(ticks=train_processes)
pyplot.xlabel('SCA score')
pyplot.ylabel('Price PLN/kg')
pyplot.title('Green coffee processing method classification')
pyplot.scatter('Score', 'Price', data=test_features, c='black')
pyplot.show()

# convert the data to numpy arrays
train_features = train_features.to_numpy()
train_processes = train_processes.to_numpy()
test_features = test_features.to_numpy()
test_processes = test_processes.to_numpy()

# create k-Nearest Neighbors and Fixed-Radius Near Neighbors Classifiers for the training data
k_classifier = KNeighborsClassifier()
k_classifier.fit(train_features, train_processes)
radius_classifier = RadiusNeighborsClassifier()
radius_classifier.fit(train_features, train_processes)

# make predictions on the testing data
k_predicted_processes = k_classifier.predict(test_features)
k_accuracy = k_classifier.score(test_features, test_processes)
radius_predicted_processes = radius_classifier.predict(test_features)
radius_accuracy = radius_classifier.score(test_features, test_processes)

# the results
print(f'\nTrue processing methods: {test_processes}')
print(f'Processing methods predicted with k-Nearest Neighbors: {k_predicted_processes}')
print(f'Accuracy (mean accuracy): {k_accuracy:.2f}')
print(f'\nTrue processing methods: {test_processes}')
print(f'Processing methods predicted with Fixed-Radius Near Neighbors: {radius_predicted_processes}')
print(f'Accuracy (mean accuracy): {radius_accuracy:.2f}')
