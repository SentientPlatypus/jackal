from train_classifier2 import Trainer, TrainerExited
from joblib import dump, load
import joblib

## This is to pre-train the classifier and save it as "classifier.joblib"

trainer = Trainer(train_path=r"/trainingdata", test_path=r"testingdata")
clf = trainer.train()
dump(clf, r'classifiers/super.joblib')
joblib_file = r"/super.pkl"
joblib.dump(clf, joblib_file)
