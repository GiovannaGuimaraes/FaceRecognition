import os
import sys
import dlib

if len(sys.argv) != 2:
	print("Need path to training directory")
	exit()

faces_dir = sys.argv[1]

# Set options
options = dlib.shape_predictor_training_options()
options.oversampling_amount = 300 # Based on paper
options.nu = 0.05 # Based on paper
options.tree_depth = 2 # Based on paper
options.be_verbose = True

# Do training
training_xml_path = os.path.join(faces_dir, input("training xml file with face landmarks path: "))
dlib.train_shape_predictor(training_xml_path, input("model name: ") + ".dat", options)

# Test
# test from inside dlib
print("\nTraining accuracy: {}".format(dlib.test_shape_predictor(training_xml_path, "predictor.dat")))

# real test case
testing_xml_path = os.path.join(faces_dir, "testing_with_face_landmarks.xml")
print("\nTesting accuracy: {}".format(dlib.test_shape_predictor(training_xml_path, "predictor.dat")))

