import pickle
with open('label_encoder.pickle', 'rb') as f:
    le = pickle.load(f)
print(list(le.classes_))
print(f"Number of classes: {len(le.classes_)}")
