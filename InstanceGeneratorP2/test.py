from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load a smaller subset of the dataset
data = Dataset.load_builtin('ml-100k')
raw_ratings = data.raw_ratings[:100]  # Using only the first 100 ratings

# Convert to a Dataset
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(pd.DataFrame(raw_ratings, columns=['user', 'item', 'rating', 'timestamp']), reader)

# Split the data into training and testing sets
trainset, testset = train_test_split(data, test_size=0.25)

# Use the SVD algorithm
algo = SVD(n_factors=25)
algo.fit(trainset)
predictions = algo.test(testset)

# Function to get top n predictions for each user
def get_top_n(predictions, n=10):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

# Function to calculate precision and recall at k
def precision_recall_at_k(predictions, k=10, threshold=3.5):
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    precisions = dict()
    recalls = dict()

    for uid, user_ratings in user_est_true.items():
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])
        n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold)) for (est, true_r) in user_ratings[:k])

        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 1
        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 1

    return precisions, recalls

# Calculate precision and recall for different k values
ks = [5, 10]
average_precisions = []
average_recalls = []

for k in ks:
    precisions, recalls = precision_recall_at_k(predictions, k=k, threshold=3.5)
    average_precisions.append(np.mean([prec for prec in precisions.values()]))
    average_recalls.append(np.mean([rec for rec in recalls.values()]))

# Plotting Precision-Recall Graphs
plt.figure(figsize=(10, 5))
plt.plot(ks, average_precisions, label='Average Precision')
plt.plot(ks, average_recalls, label='Average Recall')
plt.xlabel('Number of Recommendations')
plt.ylabel('Metric')
plt.title('Precision and Recall at Different k')
plt.legend()
plt.show()
