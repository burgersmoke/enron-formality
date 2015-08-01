#!/bin/sh
echo converting complete vector
info2vectors --input all.vectors.txt --output all.vectors
echo starting to classify
vectors2classify --input all.vectors --num-trials 5 --training-portion 0.8 --trainer NaiveBayes >Cross/NaiveBayes.stdout 2>Cross/NaiveBayes.stderr
vectors2classify --input all.vectors --num-trials 5 --training-portion 0.8 --trainer MaxEnt >Cross/MaxEnt.stdout 2>Cross/MaxEnt.stderr
vectors2classify --input all.vectors --num-trials 5 --training-portion 0.8 --trainer DecisionTree >Cross/DecisionTree.stdout 2>Cross/DecisionTree.stderr