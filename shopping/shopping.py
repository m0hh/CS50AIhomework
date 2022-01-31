import csv
from curses.ascii import isalpha
from re import A
import sys
import random

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)

    sensitivity, specificity = evaluate(y_test, predictions)


    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    months = {"Jan":0,	"Feb":1,	"Mar":2,	"Apr":3,	"May":4,	"June":5,	"Jul":6,	"Aug":7,	"Sep":8,	"Oct":9,	"Nov":10,	"Dec":11}
    visitor = {"Returning_Visitor":1, "New_Visitor":0,"Other":0}
    with open(filename) as f:
        reader = csv.reader(f)
        evidence = []
        labels = []
        f = [1,3,5,6,7,8,9]
        for row in reader:
            a = []
            if isalpha(row[0][0]):
                continue
            for c in range(len(row)):
                if c == 10:
                    a.append(int(months[row[c]]))
                elif c == 15:
                    a.append(visitor[row[c]])
                elif c == 16:
                    if row[c] =="TRUE":
                        a.append(1)
                    elif row[c] == "FALSE":
                        a.append(0)
                elif c == 17:
                    if row[c] =="TRUE":
                        labels.append(1)
                    elif row[c] == "FALSE":
                        labels.append(0)
                elif c in f :
                    a.append(float(row[c]))
                else :
                    a.append(int(row[c]))
                    
            evidence.append(a)
    return(evidence, labels)
        
            
                        

                
                    
            


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sen = 0.0
    spec = 0.0
    for L,P in zip(labels,predictions):
        if L== 1 and P ==1:
            sen += 1
        elif L==0 and P==0:
            spec += 1
    sen = sen/len(predictions)
    spec = spec/len(predictions)
    return(sen,spec)



if __name__ == "__main__":
    main()
