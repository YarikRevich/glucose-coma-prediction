# glucose-coma-prediction

[![StandWithUkraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md)

## General Information

This repository contains the implementation of glucose coma prediction model.

## Dataset

We collect 60 measurements per hour. Each data point is labeled as either “no risk” (0) or “risk” (1), based on prior calculations that incorporate features such as glucose delta values and their acceleration. The dataset is generated using a simulation script that models multiple virtual patients with diverse lifestyles, including varying meal schedules and sleep patterns.

## Models

There are implemented next models, which implement logical regression approach:
* **XGBoost**
* **RandomForest**
* **Custom Nueral Model**

After model training next quality parameters are calculated:
* **Accuracy**: definies a proportion of classifications, which are correct
* **Precision**: definies the quality of positive values, taking into account true positives and false positives
* **Recall**: definies how often a model correctly identifies positive values
* **F1 Score**: a mean of precision and recall
* **ROC AUC**: represents if model would choose positive value over negative one
* **Confusion Matrix**: TN, FP, FN, TP

## Setup

All setup related operations are processed via **Makefile** placed in the root directory.

### Generate

In order to generate data used for model training it's required to execute the next command:
```shell
make generate
```

### Build

In order to build all the models, it's required to execute the next command:
```shell
make build
```


### Server

In order to start the **API server**, it's required to execute the next command:
```shell
make start-server
```


### Demo

In order to start the demo application, it's required to execute the next command:
```shell
make start-demo
```

