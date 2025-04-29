We have 12 measures per hour. Data is lableed with "no risk" and "risk" based on some previous calculations. We'll use XGBoost classifier to have logical regression.

https://docs.aws.amazon.com/images/sagemaker/latest/dg/images/xgboost_illustration.png

* Slope (how fast the value is changing — first derivative)
* Acceleration (how much the change itself is speeding up — second derivative)
* Average glucose over last 15 minutes
* Min and max glucose in the last hour


Train data are generated with a help of a script, which was created based on real-person data with unstable glucose level and then scaled it with one month perspective having similar trend.

Data still requires tweaking