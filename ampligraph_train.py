import numpy as np
import pandas as pd
import ampligraph
from ampligraph.datasets import load_from_csv
from ampligraph.evaluation import train_test_split_no_unseen 
from ampligraph.latent_features import ComplEx, DistMult, HolE
from ampligraph.latent_features import save_model, restore_model
from ampligraph.evaluation import evaluate_performance
from ampligraph.evaluation import mr_score, mrr_score, hits_at_n_score
import tensorflow as tf
from ampligraph.utils import create_tensorboard_visualizations


#Load data
X = load_from_csv('.', 'Triple/complete_triples.csv', sep=',')
X = X[1:,]
print(X[:5,])
entities = np.unique(np.concatenate([X[:, 0], X[:, 2]]))
relations = np.unique(X[:, 1])


num_test = int(len(X) * (10/ 100))

#data = {}
#data['train'], data['test'] = train_test_split_no_unseen(X, test_size=num_test, seed=0, allow_duplication=False) 

#Build model
model = ComplEx(batches_count=200, 
                seed=0, 
                epochs=50, 
                k=50, 
                eta=5,
                optimizer='adam', 
                optimizer_params={'lr':1e-3},
                loss='multiclass_nll', 
                regularizer='LP', 
                regularizer_params={'p':3, 'lambda':1e-5}, 
                verbose=True)

positives_filter = X

tf.logging.set_verbosity(tf.logging.ERROR)

#Fit the model
"""
print(data['train'].shape)
model.fit(data['train'], early_stopping = False)

save_model(model, './best_model.pkl')
ranks = evaluate_performance(data['test'], 
                             model=model, 
                             filter_triples=positives_filter,   # Corruption strategy filter defined above 
                             use_default_protocol=True, # corrupt subj and obj separately while evaluating
                             verbose=True)

mrr = mrr_score(ranks)
print("MRR: %.2f" % (mrr))

hits_10 = hits_at_n_score(ranks, n=10)
print("Hits@10: %.2f" % (hits_10))
hits_3 = hits_at_n_score(ranks, n=3)
print("Hits@3: %.2f" % (hits_3))
hits_1 = hits_at_n_score(ranks, n=1)
print("Hits@1: %.2f" % (hits_1))

create_tensorboard_visualizations(model, 'ampligraph_embeddings')


"""
model.fit(X, early_stopping = False)

save_model(model, './best_model.pkl')
