#!/bin/sh
echo converting training vector
info2vectors --input training.vectors.txt --output training.vectors
echo converting test vector
info2vectors --input test.vectors.txt --output test.vectors --use-pipe-from training.vectors
echo starting to classify
vectors2classify --training-file training.vectors --testing-file test.vectors --trainer NaiveBayes >NaiveBayes.stdout 2>NaiveBayes.stderr
vectors2classify --training-file training.vectors --testing-file test.vectors --trainer MaxEnt >MaxEnt.stdout 2>MaxEnt.stderr
vectors2classify --training-file training.vectors --testing-file test.vectors --trainer DecisionTree >DecisionTree.stdout 2>DecisionTree.stderr