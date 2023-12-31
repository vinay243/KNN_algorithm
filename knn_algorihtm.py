import math
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

def minvalue(l:list(), n:int ):
  minlist = []
  for i in range(n):
    a = min(l)
    minlist.append(a)
    l[l.index(a)] = float('inf')
  return minlist

# inputing the training and testing dataset
data = open(r"/content/haberman.data",'r')
d = []
for i in data.readlines():
  d.append(list(map(float,i.strip().split(','))))
training_data,testing_data = train_test_split(d, test_size = 0.33,random_state = 42)

training_features = []
training_labels = []
for i in training_data:
  training_features.append(i[:3])
  training_labels.append(i[3])

testing_features = []
testing_labels = []
for i in testing_data:
  testing_features.append(i[:3])
  testing_labels.append(i[3])

# k-nearest-neighbour.
def knn(newinput,features,labels,k):
  distance = list()
  for i in range(len(features)):
    value = 0;
    for j in range(3):
      value += (features[i][j] - newinput[j])**2
    distance.append((math.sqrt(value),labels[i]))
    distance.sort()
  one = 0
  two = 0
  for i in range(k):
    if distance[i][1] == 1.0:
      one += 1
    else:
      two += 1
  if one > two:
    newlabel = 1
  else:
    newlabel = 2
  return newlabel

# testing our algorithm against testing data and saving the output in result.txt file.
results = []
k = int(input("Enter the value of k of the KNN classifier : ",))
for i in range(len(testing_features)):
  results.append(knn(testing_features[i],training_features, training_labels, k))

# checking how many values are not getting correctly labeled
error = 0
for i in range(len(results)):
  if (results[i] != testing_labels[i]):
    error += 1

print("Number of inputs wrongly labeled are : ",error)

# applying leave one out cross validation to get an optimal value of k for knn algoritm.
list_of_k = [i for i in range(100) if i%2 != 0]
n = len(training_features)
new_training_features = training_features.copy()
new_training_labels    = training_labels.copy()
least_error = float('inf')
# error list just for graphical representation
error_list = list()

for k in list_of_k:
  error = 0
  for i in range(n):
    validation_data = training_features[i]
    validation_label = training_labels[i]
    new_training_features.pop(i)
    new_training_labels.pop(i)
    new_validation_label = knn(validation_data, new_training_features,new_training_labels,k )
    if validation_label != new_validation_label:
      error+= 1
    new_training_features.insert(i,validation_data)
    new_training_labels.insert(i,validation_label)
  estimated_error = error/n
  error_list.append(estimated_error)
  if(estimated_error < least_error):
    least_error = estimated_error
    optimal_k = k

print(optimal_k)

# creating the graph for error_list
plt.plot(list_of_k, error_list)
plt.xlabel("Value of k in KNN clasifier")
plt.ylabel("Error of the given K")
plt.title("leave one out error graph")
plt.show()

# applying 5 fold cross validation technique to the dataset.
# step 1 checking whether the dataset can be divided into 5 equal sections if not then removing few elements to make that possible.(here it is poossible as we have 100 elements in training set)
estimate_error = 0
for i in range(1,6):
  new_testing_features = training_features[i*20:(i+1)*20]
  new_testing_labels   = training_labels[i*20:(i+1)*20]
  fold_training_features = training_features[:i*20] + training_features[(i+1)*20:]
  fold_training_labels = training_labels[:i*20] + training_labels[(i+1)*20:]

  error = 0
  for i in range(len(new_testing_features)):
    a = knn(new_testing_features[i],fold_training_features,fold_training_labels,27)
    if a != new_testing_labels[i]:
      error+= 1
  estimate_error += error/5

print(estimate_error)

# using 5 fold validation and finding the optimal value of k using leave one out cross vaidation.

####################
estimate_error = 0
for i in range(1,6):
  new_testing_features = training_features[i*20:(i+1)*20]
  new_testing_labels   = training_labels[i*20:(i+1)*20]
  fold_training_features = training_features[:i*20] + training_features[(i+1)*20:]
  fold_training_labels = training_labels[:i*20] + training_labels[(i+1)*20:]

  #applying leave one out here to get the optimal value of k
  list_of_k = [i for i in range(100) if i%2 != 0]
  n = len(training_features)
  leaveoneouttrainingfeatures = fold_training_features.copy()
  leaveoneouttraininglabels   = fold_training_labels.copy()
  least_error = float('inf')
  # error list just for graphical representation
  error_list = list()

  for k in list_of_k:
    error = 0
    for i in range(n):
      validation_data = training_features[i]
      validation_label = training_labels[i]
      new_training_features.pop(i)
      new_training_labels.pop(i)
      new_validation_label = knn(validation_data, new_training_features,new_training_labels,k )
      if validation_label != new_validation_label:
        error+= 1
      new_training_features.insert(i,validation_data)
      new_training_labels.insert(i,validation_label)
    estimated_error = error/n
    error_list.append(estimated_error)
    if(estimated_error < least_error):
      least_error = estimated_error
      optimal_k = k

  error = 0
  for i in range(len(new_testing_features)):
    a = knn(new_testing_features[i],fold_training_features,fold_training_labels,optimal_k)
    if a != new_testing_labels[i]:
      error+= 1
  estimate_error += error/5

print(estimate_error)
