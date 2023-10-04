from train_classifier2 import Trainer, TrainerExited
from joblib import dump, load
from sklearn.externals import joblib

## This is to pre-train the classifier and save it as "classifier.joblib"

trainer = Trainer(train_path="data3/11-5/train", test_path="data3/11-5/test/")
clf = trainer.train()
dump(clf, 'classifiers/11-5.joblib')
joblib_file = "11-5.pkl"
joblib.dump(clf, joblib_file)
