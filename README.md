<img src="https://static.scarf.sh/a.png?x-pxid=bc3c57b0-9a65-49fe-b8ea-f711c4d35b82" /><p align="center">
    <img src="https://i.imgur.com/nv33goV.png" width="35%"/>
    </br>
    <h1 align="center">The open source standard for data logging
 </h1>
  <h3 align="center">
   <a href="https://docs.whylabs.ai/docs/"><b>Documentation</b></a> &bull;
   <a href="https://bit.ly/whylogsslack"><b>Slack Community</b></a> &bull;
   <a href="https://github.com/whylabs/whylogs#python-quickstart"><b>Python Quickstart</b></a>
 </h3>




[![License](http://img.shields.io/:license-Apache%202-blue.svg)](https://github.com/whylabs/whylogs-python/blob/mainline/LICENSE)
[![PyPI version](https://badge.fury.io/py/whylogs.svg)](https://badge.fury.io/py/whylogs)
[![Coverage Status](https://coveralls.io/repos/github/whylabs/whylogs/badge.svg?branch=mainline)](https://coveralls.io/github/whylabs/whylogs?branch=mainline)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/4490/badge)](https://bestpractices.coreinfrastructure.org/projects/4490)
[![PyPi Downloads](https://pepy.tech/badge/whylogs)](https://pepy.tech/project/whylogs)
![CI](https://github.com/whylabs/whylogs-python/workflows/whylogs%20CI/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/442f6ca3dca1e583a488/maintainability)](https://codeclimate.com/github/whylabs/whylogs-python/maintainability)

## What is whylogs

whylogs is the open source standard for logging your data. With whylogs, users are able to generate summaries of their datasets (called *whylogs profiles*) which they can use to:
1. Track changes in their dataset
2. Create *data constraints* to know whether their data looks they way it should
3. Quickly visualize key summary statistics about their datasets

These three functionalities enable a variety of use cases for data scientists, machine learning engineers, and data engineers:
* Detecting data drift (and resultant ML model performance degradation)
* Data quality validation
* Exploratory data analysis via data profiling
* Tracking data for ML experiments
* And many more

whylogs can be run in Python or [Apache Spark](https://docs.whylabs.ai/docs/spark-integration) (both PySpark and Scala) environments on a variety of [data types](#data-types). We [integrate](#integrations) with lots of other tools including Pandas, [AWS Sagemaker](https://aws.amazon.com/blogs/startups/preventing-amazon-sagemaker-model-degradation-with-whylabs/), [MLflow](https://docs.whylabs.ai/docs/mlflow-integration), [Flask](https://whylabs.ai/blog/posts/deploy-and-monitor-your-ml-application-with-flask-and-whylabs), [Ray](https://docs.whylabs.ai/docs/ray-integration), [RAPIDS](https://whylabs.ai/blog/posts/monitoring-high-performance-machine-learning-models-with-rapids-and-whylogs), [Apache Kafka](https://docs.whylabs.ai/docs/kafka-integration), and more.

If you have any questions, comments, or just want to hang out with us, please join [our Slack Community](http://join.slack.whylabs.ai/). In addition to joining the Slack Community, you can also help this project by giving us a ⭐ in the upper right corner of this page.


## Python Quickstart<a name="python-quickstart" />


### Install whylogs

Install whylogs using the pip package manager by running

```
pip install whylogs
```

### Log some data

whylogs is easy to get up and runnings

```python
from whylogs import get_or_create_session
import pandas as pd

session = get_or_create_session()

df = pd.read_csv("path/to/file.csv")

with session.logger(dataset_name="my_dataset") as logger:
    
    #dataframe
    logger.log_dataframe(df)

    #dict
    logger.log({"name": 1})

    #images
    logger.log_image("path/to/image.png")
```

## Table of Contents

- [whylogs Profiles](#whylogs-profiles)
- [Visualizing Profiles](#visualizing-profiles)
- [Features](#features)
- [Data Types](#data-types)
- [Integrations](#integrations)
- [Examples](#examples)
- [Community](#community)
- [Roadmap](#roadmap)
- [Contribute](#contribute)

## whylogs Profiles<a name="whylogs-profiles" />

whylogs profiles are the core of the whylogs library. They capture key statistical properties of data, such as the distribution (far beyond simple mean, median, and standard deviation measures), the number of missing values, and a wide range of configurable custom metrics. By capturing these summary statistics, we are able to accurately represent the data and enable all of the use cases described in the introduction.

whylogs profiles have three properties that make them ideal for data logging: they are **descriptive**, **lightweight**, and **mergeable**.

<img align="left" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOTIiIGhlaWdodD0iOTIiIHZpZXdCb3g9IjAgMCA5MiA5MiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGcgb3BhY2l0eT0iMC41Ij4KPGcgb3BhY2l0eT0iMC41Ij4KPHJlY3QgeD0iMTQiIHk9IjI1LjI0OTUiIHdpZHRoPSI0Ny4xMjU4IiBoZWlnaHQ9IjEyLjc3NjgiIHJ4PSIyIiBmaWxsPSIjRkY2OTRGIi8+CjxyZWN0IHg9IjE0IiB5PSI0MC40OTEyIiB3aWR0aD0iNDcuMTI1OCIgaGVpZ2h0PSIxMi43NzY4IiByeD0iMiIgZmlsbD0iI0ZGNjk0RiIvPgo8cmVjdCB4PSIxNCIgeT0iNTUuNzMzNCIgd2lkdGg9IjQ3LjEyNTgiIGhlaWdodD0iMTIuNzc2OCIgcng9IjIiIGZpbGw9IiNGRjY5NEYiLz4KPC9nPgo8L2c+CjxnIGZpbHRlcj0idXJsKCNmaWx0ZXIwX2QpIj4KPHJlY3QgeD0iMjcuMTAxNiIgeT0iMzUiIHdpZHRoPSI0MyIgaGVpZ2h0PSIzOCIgcng9IjIiIGZpbGw9InVybCgjcGFpbnQwX2xpbmVhcikiLz4KPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0zNC45NTg3IDQyQzM1LjQzMjEgNDIgMzUuODE1OCA0Mi4zODM4IDM1LjgxNTggNDIuODU3MVY2My44NTcxSDYzLjI0NDRDNjMuNzE3OCA2My44NTcxIDY0LjEwMTYgNjQuMjQwOSA2NC4xMDE2IDY0LjcxNDNDNjQuMTAxNiA2NS4xODc3IDYzLjcxNzggNjUuNTcxNCA2My4yNDQ0IDY1LjU3MTRIMzQuMTAxNlY0Mi44NTcxQzM0LjEwMTYgNDIuMzgzOCAzNC40ODUzIDQyIDM0Ljk1ODcgNDJaIiBmaWxsPSJ3aGl0ZSIvPgo8cmVjdCB4PSIzNy4xMDE2IiB5PSI0OCIgd2lkdGg9IjciIGhlaWdodD0iMTciIHJ4PSIwLjg1NzE0MyIgZmlsbD0id2hpdGUiLz4KPHJlY3QgeD0iNDYuMTAxNiIgeT0iNTciIHdpZHRoPSI3IiBoZWlnaHQ9IjgiIHJ4PSIwLjg1NzE0MyIgZmlsbD0id2hpdGUiLz4KPHJlY3QgeD0iNTUuMTAxNiIgeT0iNTMiIHdpZHRoPSI3IiBoZWlnaHQ9IjEyIiByeD0iMC44NTcxNDMiIGZpbGw9IndoaXRlIi8+CjwvZz4KPHJlY3QgeD0iMSIgeT0iLTEiIHdpZHRoPSIyNiIgaGVpZ2h0PSIyNiIgcng9IjEiIHRyYW5zZm9ybT0ibWF0cml4KDEgMCAwIC0xIDUwLjEwMTYgNDUuOTk5NSkiIGZpbGw9IndoaXRlIiBzdHJva2U9IiNGRkE3NzYiIHN0cm9rZS13aWR0aD0iMiIvPgo8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTU3LjE3MjIgMzguNDk5NUM1Ny4xNzIyIDM4Ljc3NTcgNTYuOTQ4MyAzOC45OTk1IDU2LjY3MjIgMzguOTk5NUg1NS42OTI0QzU1LjQxNjIgMzguOTk5NSA1NS4xOTI0IDM4Ljc3NTcgNTUuMTkyNCAzOC40OTk1QzU1LjE5MjQgMzguMjIzNCA1NS40MTYyIDM3Ljk5OTUgNTUuNjkyNCAzNy45OTk1SDU2LjY3MjJDNTYuOTQ4MyAzNy45OTk1IDU3LjE3MjIgMzguMjIzNCA1Ny4xNzIyIDM4LjQ5OTVaIiBmaWxsPSIjRjA3MDI4Ii8+CjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNNzMuMDExNSAzOC40OTk1QzczLjAxMTUgMzguNzc1NyA3Mi43ODc3IDM4Ljk5OTUgNzIuNTExNSAzOC45OTk1SDYwLjY0MjhDNjAuMzY2NyAzOC45OTk1IDYwLjE0MjggMzguNzc1NyA2MC4xNDI4IDM4LjQ5OTVDNjAuMTQyOCAzOC4yMjM0IDYwLjM2NjcgMzcuOTk5NSA2MC42NDI4IDM3Ljk5OTVINzIuNTExNUM3Mi43ODc3IDM3Ljk5OTUgNzMuMDExNSAzOC4yMjM0IDczLjAxMTUgMzguNDk5NVoiIGZpbGw9IiNGMDcwMjgiLz4KPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik01Ny4xNzIyIDQxLjQ5OTVDNTcuMTcyMiA0MS43NzU3IDU2Ljk0ODMgNDEuOTk5NSA1Ni42NzIyIDQxLjk5OTVINTUuNjkyNEM1NS40MTYyIDQxLjk5OTUgNTUuMTkyNCA0MS43NzU3IDU1LjE5MjQgNDEuNDk5NUM1NS4xOTI0IDQxLjIyMzQgNTUuNDE2MiA0MC45OTk1IDU1LjY5MjQgNDAuOTk5NUg1Ni42NzIyQzU2Ljk0ODMgNDAuOTk5NSA1Ny4xNzIyIDQxLjIyMzQgNTcuMTcyMiA0MS40OTk1WiIgZmlsbD0iI0YwNzAyOCIvPgo8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTY3LjkxOTggNDEuNDk5NUM2Ny45MTk4IDQxLjc3NTcgNjcuNjk2IDQxLjk5OTUgNjcuNDE5OCA0MS45OTk1SDYwLjc4MzRDNjAuNTA3MyA0MS45OTk1IDYwLjI4MzQgNDEuNzc1NyA2MC4yODM0IDQxLjQ5OTVDNjAuMjgzNCA0MS4yMjM0IDYwLjUwNzMgNDAuOTk5NSA2MC43ODM0IDQwLjk5OTVINjcuNDE5OEM2Ny42OTYgNDAuOTk5NSA2Ny45MTk4IDQxLjIyMzQgNjcuOTE5OCA0MS40OTk1WiIgZmlsbD0iI0YwNzAyOCIvPgo8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTU3LjE3MjIgMzUuNDk5NUM1Ny4xNzIyIDM1Ljc3NTcgNTYuOTQ4MyAzNS45OTk1IDU2LjY3MjIgMzUuOTk5NUg1NS42OTI0QzU1LjQxNjIgMzUuOTk5NSA1NS4xOTI0IDM1Ljc3NTcgNTUuMTkyNCAzNS40OTk1QzU1LjE5MjQgMzUuMjIzNCA1NS40MTYyIDM0Ljk5OTUgNTUuNjkyNCAzNC45OTk1SDU2LjY3MjJDNTYuOTQ4MyAzNC45OTk1IDU3LjE3MjIgMzUuMjIzNCA1Ny4xNzIyIDM1LjQ5OTVaIiBmaWxsPSIjRjA3MDI4Ii8+CjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNNzEuMDMxNyAzNS40OTk1QzcxLjAzMTcgMzUuNzc1NyA3MC44MDc5IDM1Ljk5OTUgNzAuNTMxNyAzNS45OTk1SDYwLjY0MjhDNjAuMzY2NyAzNS45OTk1IDYwLjE0MjggMzUuNzc1NyA2MC4xNDI4IDM1LjQ5OTVDNjAuMTQyOCAzNS4yMjM0IDYwLjM2NjcgMzQuOTk5NSA2MC42NDI4IDM0Ljk5OTVINzAuNTMxN0M3MC44MDc5IDM0Ljk5OTUgNzEuMDMxNyAzNS4yMjM0IDcxLjAzMTcgMzUuNDk5NVoiIGZpbGw9IiNGMDcwMjgiLz4KPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik01Ny4xNzIyIDMyLjQ5OTVDNTcuMTcyMiAzMi43NzU3IDU2Ljk0ODMgMzIuOTk5NSA1Ni42NzIyIDMyLjk5OTVINTUuNjkyNEM1NS40MTYyIDMyLjk5OTUgNTUuMTkyNCAzMi43NzU3IDU1LjE5MjQgMzIuNDk5NUM1NS4xOTI0IDMyLjIyMzQgNTUuNDE2MiAzMS45OTk1IDU1LjY5MjQgMzEuOTk5NUg1Ni42NzIyQzU2Ljk0ODMgMzEuOTk5NSA1Ny4xNzIyIDMyLjIyMzQgNTcuMTcyMiAzMi40OTk1WiIgZmlsbD0iI0YwNzAyOCIvPgo8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTcxLjAzMTcgMzIuNDk5NUM3MS4wMzE3IDMyLjc3NTcgNzAuODA3OSAzMi45OTk1IDcwLjUzMTcgMzIuOTk5NUg2MC42NDI4QzYwLjM2NjcgMzIuOTk5NSA2MC4xNDI4IDMyLjc3NTcgNjAuMTQyOCAzMi40OTk1QzYwLjE0MjggMzIuMjIzNCA2MC4zNjY3IDMxLjk5OTUgNjAuNjQyOCAzMS45OTk1SDcwLjUzMTdDNzAuODA3OSAzMS45OTk1IDcxLjAzMTcgMzIuMjIzNCA3MS4wMzE3IDMyLjQ5OTVaIiBmaWxsPSIjRjA3MDI4Ii8+CjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNNTcuMTcyMiAyOS40OTk1QzU3LjE3MjIgMjkuNzc1NyA1Ni45NDgzIDI5Ljk5OTUgNTYuNjcyMiAyOS45OTk1SDU1LjY5MjRDNTUuNDE2MiAyOS45OTk1IDU1LjE5MjQgMjkuNzc1NyA1NS4xOTI0IDI5LjQ5OTVDNTUuMTkyNCAyOS4yMjM0IDU1LjQxNjIgMjguOTk5NSA1NS42OTI0IDI4Ljk5OTVINTYuNjcyMkM1Ni45NDgzIDI4Ljk5OTUgNTcuMTcyMiAyOS4yMjM0IDU3LjE3MjIgMjkuNDk5NVoiIGZpbGw9IiNGMDcwMjgiLz4KPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik02Ny45MTk4IDI5LjQ5OTVDNjcuOTE5OCAyOS43NzU3IDY3LjY5NiAyOS45OTk1IDY3LjQxOTggMjkuOTk5NUg2MC43ODM0QzYwLjUwNzMgMjkuOTk5NSA2MC4yODM0IDI5Ljc3NTcgNjAuMjgzNCAyOS40OTk1QzYwLjI4MzQgMjkuMjIzNCA2MC41MDczIDI4Ljk5OTUgNjAuNzgzNCAyOC45OTk1SDY3LjQxOThDNjcuNjk2IDI4Ljk5OTUgNjcuOTE5OCAyOS4yMjM0IDY3LjkxOTggMjkuNDk5NVoiIGZpbGw9IiNGMDcwMjgiLz4KPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik01Ny4xNzIyIDI2LjQ5OTVDNTcuMTcyMiAyNi43NzU3IDU2Ljk0ODMgMjYuOTk5NSA1Ni42NzIyIDI2Ljk5OTVINTUuNjkyNEM1NS40MTYyIDI2Ljk5OTUgNTUuMTkyNCAyNi43NzU3IDU1LjE5MjQgMjYuNDk5NUM1NS4xOTI0IDI2LjIyMzQgNTUuNDE2MiAyNS45OTk1IDU1LjY5MjQgMjUuOTk5NUg1Ni42NzIyQzU2Ljk0ODMgMjUuOTk5NSA1Ny4xNzIyIDI2LjIyMzQgNTcuMTcyMiAyNi40OTk1WiIgZmlsbD0iI0YwNzAyOCIvPgo8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTcxLjAzMTcgMjYuNDk5NUM3MS4wMzE3IDI2Ljc3NTcgNzAuODA3OSAyNi45OTk1IDcwLjUzMTcgMjYuOTk5NUg2MC42NDI4QzYwLjM2NjcgMjYuOTk5NSA2MC4xNDI4IDI2Ljc3NTcgNjAuMTQyOCAyNi40OTk1QzYwLjE0MjggMjYuMjIzNCA2MC4zNjY3IDI1Ljk5OTUgNjAuNjQyOCAyNS45OTk1SDcwLjUzMTdDNzAuODA3OSAyNS45OTk1IDcxLjAzMTcgMjYuMjIzNCA3MS4wMzE3IDI2LjQ5OTVaIiBmaWxsPSIjRjA3MDI4Ii8+CjxkZWZzPgo8ZmlsdGVyIGlkPSJmaWx0ZXIwX2QiIHg9IjcuMTAxNTYiIHk9IjE3IiB3aWR0aD0iNjkiIGhlaWdodD0iNjQiIGZpbHRlclVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgY29sb3ItaW50ZXJwb2xhdGlvbi1maWx0ZXJzPSJzUkdCIj4KPGZlRmxvb2QgZmxvb2Qtb3BhY2l0eT0iMCIgcmVzdWx0PSJCYWNrZ3JvdW5kSW1hZ2VGaXgiLz4KPGZlQ29sb3JNYXRyaXggaW49IlNvdXJjZUFscGhhIiB0eXBlPSJtYXRyaXgiIHZhbHVlcz0iMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMTI3IDAiIHJlc3VsdD0iaGFyZEFscGhhIi8+CjxmZU9mZnNldCBkeD0iLTciIGR5PSItNSIvPgo8ZmVHYXVzc2lhbkJsdXIgc3RkRGV2aWF0aW9uPSI2LjUiLz4KPGZlQ29sb3JNYXRyaXggdHlwZT0ibWF0cml4IiB2YWx1ZXM9IjAgMCAwIDAgMC44MjA4MzMgMCAwIDAgMCAwLjM1MzE2NiAwIDAgMCAwIDAuMjcxNTU5IDAgMCAwIDAuNSAwIi8+CjxmZUJsZW5kIG1vZGU9Im5vcm1hbCIgaW4yPSJCYWNrZ3JvdW5kSW1hZ2VGaXgiIHJlc3VsdD0iZWZmZWN0MV9kcm9wU2hhZG93Ii8+CjxmZUJsZW5kIG1vZGU9Im5vcm1hbCIgaW49IlNvdXJjZUdyYXBoaWMiIGluMj0iZWZmZWN0MV9kcm9wU2hhZG93IiByZXN1bHQ9InNoYXBlIi8+CjwvZmlsdGVyPgo8bGluZWFyR3JhZGllbnQgaWQ9InBhaW50MF9saW5lYXIiIHgxPSIyMi42NzI2IiB5MT0iMzEuNjYwMSIgeDI9Ijc0LjUwMDMiIHkyPSIzNS45MTU3IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiNFQTVCNEYiLz4KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjRjlDNDUyIi8+CjwvbGluZWFyR3JhZGllbnQ+CjwvZGVmcz4KPC9zdmc+Cg=="></img>

**Descriptive**: whylogs profiles describe the dataset that they represent. This high fidelity representation of datasets is what enables whylogs profiles to be effective snapshots of the data. They are better at capturing the characteristics of a dataset than a sample would be, as discussed in our [Data Logging: Sampling versus Profiling](https://whylabs.ai/blog/posts/data-logging-sampling-versus-profiling) blog post. 

<img align="left" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOTIiIGhlaWdodD0iOTUiIHZpZXdCb3g9IjAgMCA5MiA5NSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGcgb3BhY2l0eT0iMC41Ij4KPHJlY3QgeD0iMTQiIHk9IjIzLjgwOTYiIHdpZHRoPSI0Ny4xMjU4IiBoZWlnaHQ9IjEyLjc3NjgiIHJ4PSIyIiBmaWxsPSIjRjA3MDI4Ii8+CjxyZWN0IHg9IjE0IiB5PSIzOS4wNTEzIiB3aWR0aD0iNDcuMTI1OCIgaGVpZ2h0PSIxMi43NzY4IiByeD0iMiIgZmlsbD0iI0YwNzAyOCIvPgo8cmVjdCB4PSIxNCIgeT0iNTQuMjkzNSIgd2lkdGg9IjQ3LjEyNTgiIGhlaWdodD0iMTIuNzc2OCIgcng9IjIiIGZpbGw9IiNGMDcwMjgiLz4KPC9nPgo8ZyBmaWx0ZXI9InVybCgjZmlsdGVyMF9kKSI+CjxwYXRoIGQ9Ik01MS42OTEzIDU0LjI0MThDNTIuNDgxNyA1My44ODE2IDUzLjM4OTUgNTMuODgxNiA1NC4xNzk5IDU0LjI0MThMNzIuODQ2NiA2Mi43NTA0QzczLjYyNjkgNjMuMTA2MSA3My42MjcgNjQuMjE0NiA3Mi44NDY2IDY0LjU3MDJMNTQuMTc5OSA3My4wNzg4QzUzLjM4OTUgNzMuNDM5IDUyLjQ4MTcgNzMuNDM5IDUxLjY5MTMgNzMuMDc4OEwzMy4wMjQ2IDY0LjU3MDJDMzIuMjQ0MyA2NC4yMTQ2IDMyLjI0NDMgNjMuMTA2MSAzMy4wMjQ2IDYyLjc1MDRMNTEuNjkxMyA1NC4yNDE4WiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTUxLjY5MTMgNDUuODk1MUM1Mi40ODE3IDQ1LjUzNDggNTMuMzg5NSA0NS41MzQ4IDU0LjE3OTkgNDUuODk1MUw3Mi44NDY2IDU0LjQwMzZDNzMuNjI2OSA1NC43NTkzIDczLjYyNyA1NS44Njc4IDcyLjg0NjYgNTYuMjIzNUw1NC4xNzk5IDY0LjczMkM1My4zODk1IDY1LjA5MjMgNTIuNDgxNyA2NS4wOTIzIDUxLjY5MTMgNjQuNzMyTDMzLjAyNDYgNTYuMjIzNUMzMi4yNDQzIDU1Ljg2NzggMzIuMjQ0MyA1NC43NTkzIDMzLjAyNDYgNTQuNDAzNkw1MS42OTEzIDQ1Ljg5NTFaIiBmaWxsPSJ1cmwoI3BhaW50MF9saW5lYXIpIi8+CjxwYXRoIGQ9Ik01MS42OTEzIDM3LjU2NzJDNTIuNDgxNyAzNy4yMDY5IDUzLjM4OTUgMzcuMjA2OSA1NC4xNzk5IDM3LjU2NzJMNzIuODQ2NiA0Ni4wNzU3QzczLjYyNjkgNDYuNDMxNCA3My42MjcgNDcuNTM5OSA3Mi44NDY2IDQ3Ljg5NTZMNTQuMTc5OSA1Ni40MDQxQzUzLjM4OTUgNTYuNzY0NCA1Mi40ODE3IDU2Ljc2NDQgNTEuNjkxMyA1Ni40MDQxTDMzLjAyNDYgNDcuODk1NkMzMi4yNDQzIDQ3LjUzOTkgMzIuMjQ0MyA0Ni40MzE0IDMzLjAyNDYgNDYuMDc1N0w1MS42OTEzIDM3LjU2NzJaIiBmaWxsPSJ3aGl0ZSIvPgo8L2c+CjxjaXJjbGUgY3g9IjYyLjg4MjgiIGN5PSIzMi41IiByPSIxMy41IiBmaWxsPSJ3aGl0ZSIgc3Ryb2tlPSIjRkZBNzc2IiBzdHJva2Utd2lkdGg9IjIiLz4KPGcgY2xpcC1wYXRoPSJ1cmwoI2NsaXAwKSI+CjxwYXRoIGQ9Ik01My42NzAyIDM3LjU1ODdDNTMuNjY4NyAzNy41NjIgNTMuNjY4MiAzNy41NjU2IDUzLjY2NjggMzcuNTY5MkM1My42NjA3IDM3LjU4NDMgNTMuNjU1MyAzNy41OTk3IDUzLjY1MTcgMzcuNjE1N0M1My42NTE2IDM3LjYxNTggNTMuNjUxNSAzNy42MTYyIDUzLjY1MTQgMzcuNjE2NEM1My42NTE0IDM3LjYxNjYgNTMuNjUxMyAzNy42MTY4IDUzLjY1MTMgMzcuNjE3QzUzLjY0OTkgMzcuNjIzOSA1My42NDk1IDM3LjYzMDggNTMuNjQ4OSAzNy42Mzc3QzUzLjY0NzEgMzcuNjQ5NiA1My42NDQ4IDM3LjY2MTIgNTMuNjQ0NyAzNy42NzM0QzUzLjY0NDcgMzcuNjc0IDUzLjY0NDQgMzcuNjc0NCA1My42NDQ0IDM3LjY3NUM1My42NDQ0IDM3LjY3NTIgNTMuNjQ0NSAzNy42NzU1IDUzLjY0NDUgMzcuNjc1NkM1My42NDQ0IDM3LjY3NjcgNTMuNjQ1IDM3LjY3NzQgNTMuNjQ1IDM3LjY3ODNDNTMuNjQ0OCAzNy42OTYgNTMuNjQ1OCAzNy43MTQxIDUzLjY0OSAzNy43MzIzQzUzLjY1MjUgMzcuNzUyMyA1My42NTggMzcuNzcxNCA1My42NjUxIDM3Ljc4OTdDNTMuNjY1NSAzNy43OTA2IDUzLjY2NTggMzcuNzkxNSA1My42NjY0IDM3Ljc5MjVDNTMuNjgwNSAzNy44Mjc4IDUzLjcwMTEgMzcuODU5NCA1My43MjY0IDM3Ljg4NkM1My43MjY3IDM3Ljg4NjcgNTMuNzI2OCAzNy44ODc2IDUzLjcyNzMgMzcuODg4MUM1My43MjggMzcuODg4NyA1My43Mjg3IDM3Ljg4OTEgNTMuNzI5NCAzNy44ODk3QzUzLjc0NjYgMzcuOTA3NCA1My43NjY1IDM3LjkyMiA1My43ODc3IDM3LjkzNUM1My43OTM5IDM3LjkzODcgNTMuOCAzNy45NDI0IDUzLjgwNjYgMzcuOTQ1NkM1My44Mjk0IDM3Ljk1NzUgNTMuODUzNSAzNy45NjczIDUzLjg3OTIgMzcuOTcyOUM1My44Nzk1IDM3Ljk3MyA1My44ODAxIDM3Ljk3MzQgNTMuODgwNSAzNy45NzM1QzYwLjAzMzUgMzkuMzE0NSA2Mi43MTE3IDM3Ljg4NzMgNjMuNzE4MiAzNi45OTk2TDYzLjc0MjIgMzcuODA3NEw2NC4wNTUgMzcuNzgzOEM2NS41ODUxIDM3LjY2OTEgNjYuNjQ1MiAzNi4yMjkgNjYuNjg5OCAzNi4xNjc5QzY2Ljc4NjggMzYuMDMzOCA2Ni43NTY4IDM1Ljg0NjUgNjYuNjIzMSAzNS43NDkxQzY2LjU5MjMgMzUuNzI3IDY2LjU1OTMgMzUuNzExMyA2Ni41MjQ3IDM1LjcwMkM2Ni40MDgyIDM1LjY3MDggNjYuMjc5MyAzNS43MTE5IDY2LjIwNDMgMzUuODE1MkM2Ni4xOTYgMzUuODI2OCA2NS40MTI3IDM2Ljg4NTMgNjQuMzIyNyAzNy4xMzcyTDY0LjMwMjggMzYuNDY0N0M2NC4yOTgzIDM2LjMwMzggNjQuMTk2NyAzNi4xNjYyIDY0LjA0MzggMzYuMTE0N0M2My44OTI0IDM2LjA2MjEgNjMuNzI3OSAzNi4xMTA0IDYzLjYyNjcgMzYuMjM1M0M2My4xNzU2IDM2Ljc5MzYgNjEuNDQ2NCAzOC4zNTE1IDU2LjU5NDEgMzcuODE3NEM2MS42NTI5IDM3LjA4NzEgNjQuOTY3MSAzNC4wNDYgNjYuOTM3OCAzMS40MTZDNjcuNTQzOSAzMC42MDcgNjguMDU1OSAyOS43OTk4IDY4LjQ4NDkgMjkuMDM5MkM2OC45MTIyIDI5Ljg1OSA2OS42MDQ3IDMxLjc2NzYgNjguMjU4MSAzMy44NTU4TDY3LjYzNTcgMzIuNDU2OEw2Ny4wNzIyIDMyLjY1NzhDNjcuMDc0NSAzMi42NjY5IDY3LjMxMTkgMzMuNTk5NCA2Ni43MDYyIDM1LjAxNjJDNjYuNjQwOSAzNS4xNjg1IDY2LjcxMTcgMzUuMzQ0OCA2Ni44NjM5IDM1LjQwOThDNjcuMDE1OCAzNS40NzUyIDY3LjE5MjUgMzUuNDA0NSA2Ny4yNTc1IDM1LjI1MjFDNjcuNDYzNiAzNC43NzA0IDY3LjU4MzIgMzQuMzM2NiA2Ny42NDkxIDMzLjk2MzNMNjguMTI4MSAzNS4wNDA0TDY4LjQzNTQgMzQuNjQzQzcwLjY0MDIgMzEuNzg5NSA2OS4yNDM5IDI5LjEwMjYgNjguODIxMyAyOC40MjIyQzY5LjkwMDIgMjYuMzY3MSA3MC4zNDEzIDI0Ljc4MzcgNzAuMzY3NCAyNC42ODg2QzcwLjQxMSAyNC41Mjg5IDcwLjMxNjggMjQuMzY0MSA3MC4xNTcxIDI0LjMyMDNDNzAuMTU2NSAyNC4zMjAxIDcwLjE1NjEgMjQuMzIgNzAuMTU1NiAyNC4zMTk4QzY5Ljk5NjQgMjQuMjc3MiA2OS44MzIyIDI0LjM3MTMgNjkuNzg4NSAyNC41MzA0QzY5Ljc3OTUgMjQuNTYzNCA2OC44NTk3IDI3Ljg1NjkgNjYuNDQ1NyAzMS4wNzE3QzYzLjczNjkgMzQuNjc5NSA2MC4zMjYgMzYuNzQ3NyA1Ni4yODc1IDM3LjI1NDdDNTYuNzA5MyAzNy4wMzYgNTYuOTAxOCAzNi44NjAyIDU2LjkxNzMgMzYuODQ1M0M1Ny4wMzcxIDM2LjczMiA1Ny4wNDIzIDM2LjU0NDQgNTYuOTMwMSAzNi40MjM2QzU2Ljg5MDYgMzYuMzgxMSA1Ni44NDEzIDM2LjM1MjYgNTYuNzg5MSAzNi4zMzg2QzU2LjY5MjkgMzYuMzEyOCA1Ni41ODU4IDM2LjMzNTUgNTYuNTA3IDM2LjQwNzZDNTYuNTAwMSAzNi40MTQgNTUuNzgzIDM3LjA1NDkgNTMuODkyOCAzNy4zODVDNTMuODkyNCAzNy4zODUxIDUzLjg5MTkgMzcuMzg1NCA1My44OTE0IDM3LjM4NTRDNTMuODkwOCAzNy4zODU1IDUzLjg5MDIgMzcuMzg1NSA1My44ODk1IDM3LjM4NTZDNTMuODc1NiAzNy4zODgyIDUzLjg2MjMgMzcuMzkyOCA1My44NDkxIDM3LjM5NzNDNTMuODQ0MSAzNy4zOTkxIDUzLjgzODcgMzcuMzk5OSA1My44MzM4IDM3LjQwMTdDNTMuODMzOCAzNy40MDE3IDUzLjgzMzcgMzcuNDAxNiA1My44MzM2IDM3LjQwMThDNTMuODIzOCAzNy40MDU4IDUzLjgxNDggMzcuNDExMSA1My44MDU3IDM3LjQxNjNDNTMuNzcwOCAzNy40MzQ3IDUzLjc0MDMgMzcuNDU5NSA1My43MTU2IDM3LjQ4OTFDNTMuNzEzNyAzNy40OTE1IDUzLjcxMTUgMzcuNDkzNiA1My43MDk2IDM3LjQ5NkM1My43MDY0IDM3LjUwMDEgNTMuNzAyNCAzNy41MDM2IDUzLjY5OTQgMzcuNTA3OUM1My42OTc3IDM3LjUxMDQgNTMuNjk2NyAzNy41MTMyIDUzLjY5NTEgMzcuNTE1NUM1My42ODU2IDM3LjUyOTMgNTMuNjc3IDM3LjU0MzUgNTMuNjcwMiAzNy41NTg3WiIgZmlsbD0iI0YwNzAyOCIgc3Ryb2tlPSIjRjA3MDI4IiBzdHJva2Utd2lkdGg9IjAuNjUiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPHBhdGggZD0iTTU3Ljc0IDM1Ljk5NzFDNTguMDk2NCAzNS43NDU4IDU4LjYwNiAzNS4yMDMzIDU4LjgxNTEgMzQuOTc0NEw2MS43MTE3IDM1LjA0NjdMNTkuODg4OSAzMy44NDMzTDYxLjIxOTEgMzIuMjY5NEw2My45OTM4IDMxLjc1MDRDNjQuMTQzNSAzMS43MjI0IDY0LjI1NzUgMzEuNjAyMiA2NC4yNzc3IDMxLjQ1MTJDNjQuMjk4IDMxLjMwMDMgNjQuMjE5NyAzMS4xNTQ1IDY0LjA4MjggMzEuMDg4Mkw2Mi42MzAyIDMwLjM4NEM2NC40MzExIDI3LjkzODIgNjcuMDY4IDI4LjEzMzMgNjcuMTgzMyAyOC4xNDNDNjcuMzQ4IDI4LjE1NzMgNjcuNDkzNCAyOC4wMzU4IDY3LjUwODMgMjcuODcxMUM2Ny41MjE1IDI3LjcyMzcgNjcuNDI1OSAyNy41OTE2IDY3LjI4NzUgMjcuNTU0NUM2Ny4yNzA5IDI3LjU1MDEgNjcuMjUzOSAyNy41NDcgNjcuMjM2MyAyNy41NDU0QzY3LjEwMjUgMjcuNTMzMyA2My45MzM5IDI3LjI4NTggNjEuOTMyNyAzMC4zMzY1TDYxLjc0NTQgMzAuNjIyTDYzLjE0MjMgMzEuMjk5Mkw2MC44OTg2IDMxLjcxODlMNTguOTk0NiAzMy45NzIzTDU5LjYzNTEgMzQuMzk1MUw1OC41NTMgMzQuMzY3OUw1OC40NjA0IDM0LjQ3MjNDNTguMjc0MyAzNC42ODIzIDU3LjcxOTkgMzUuMjc3NSA1Ny4zOTM5IDM1LjUwNzJDNTcuMjU4NiAzNS42MDI3IDU3LjIyNjMgMzUuNzg5OSA1Ny4zMjE3IDM1LjkyNTJDNTcuNDE3MyAzNi4wNTk5IDU3LjYwNDIgMzYuMDkyNiA1Ny43NCAzNS45OTcxWiIgZmlsbD0iI0YwNzAyOCIgc3Ryb2tlPSIjRjA3MDI4IiBzdHJva2Utd2lkdGg9IjAuNjUiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9nPgo8ZGVmcz4KPGZpbHRlciBpZD0iZmlsdGVyMF9kIiB4PSIxNy40Mzk1IiB5PSIyOC4yOTciIHdpZHRoPSI3MC45OTIyIiBoZWlnaHQ9IjY2LjA1MiIgZmlsdGVyVW5pdHM9InVzZXJTcGFjZU9uVXNlIiBjb2xvci1pbnRlcnBvbGF0aW9uLWZpbHRlcnM9InNSR0IiPgo8ZmVGbG9vZCBmbG9vZC1vcGFjaXR5PSIwIiByZXN1bHQ9IkJhY2tncm91bmRJbWFnZUZpeCIvPgo8ZmVDb2xvck1hdHJpeCBpbj0iU291cmNlQWxwaGEiIHR5cGU9Im1hdHJpeCIgdmFsdWVzPSIwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAxMjcgMCIgcmVzdWx0PSJoYXJkQWxwaGEiLz4KPGZlT2Zmc2V0IGR5PSI2Ii8+CjxmZUdhdXNzaWFuQmx1ciBzdGREZXZpYXRpb249IjcuNSIvPgo8ZmVDb2xvck1hdHJpeCB0eXBlPSJtYXRyaXgiIHZhbHVlcz0iMCAwIDAgMCAwLjk2NDcwNiAwIDAgMCAwIDAuNTA1ODgyIDAgMCAwIDAgMC4xOTIxNTcgMCAwIDAgMC40NCAwIi8+CjxmZUJsZW5kIG1vZGU9Im5vcm1hbCIgaW4yPSJCYWNrZ3JvdW5kSW1hZ2VGaXgiIHJlc3VsdD0iZWZmZWN0MV9kcm9wU2hhZG93Ii8+CjxmZUJsZW5kIG1vZGU9Im5vcm1hbCIgaW49IlNvdXJjZUdyYXBoaWMiIGluMj0iZWZmZWN0MV9kcm9wU2hhZG93IiByZXN1bHQ9InNoYXBlIi8+CjwvZmlsdGVyPgo8bGluZWFyR3JhZGllbnQgaWQ9InBhaW50MF9saW5lYXIiIHgxPSIyNi41MTU1IiB5MT0iNDMuNTcyNiIgeDI9Ijc4LjM2NyIgeTI9IjUxLjgyNyIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgo8c3RvcCBzdG9wLWNvbG9yPSIjRUE1QjRGIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI0Y5QzQ1MiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8Y2xpcFBhdGggaWQ9ImNsaXAwIj4KPHJlY3Qgd2lkdGg9IjE0LjIwMTEiIGhlaWdodD0iMTcuNjAxMyIgZmlsbD0id2hpdGUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDY3LjA5OTYgNDEuNjc2OCkgcm90YXRlKC0xNjUpIi8+CjwvY2xpcFBhdGg+CjwvZGVmcz4KPC9zdmc+Cg=="></img>

**Lightweight**: In addition to being a high fidelity representation of data, whylogs profiles also have high information density. You can easily profile terabytes or even petabytes of data in profiles that are only megabytes large. Because whylogs profiles are lightweight, they are very inexpensive to store, transport, and interact with.


<img align="left" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOTIiIGhlaWdodD0iOTUiIHZpZXdCb3g9IjAgMCA5MiA5NSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGcgb3BhY2l0eT0iMC41Ij4KPHJlY3QgeD0iMTQiIHk9IjIzLjgwOTYiIHdpZHRoPSI0Ny4xMjU4IiBoZWlnaHQ9IjEyLjc3NjgiIHJ4PSIyIiBmaWxsPSIjRjA3MDI4Ii8+CjxyZWN0IHg9IjE0IiB5PSIzOS4wNTEzIiB3aWR0aD0iNDcuMTI1OCIgaGVpZ2h0PSIxMi43NzY4IiByeD0iMiIgZmlsbD0iI0YwNzAyOCIvPgo8cmVjdCB4PSIxNCIgeT0iNTQuMjkzNSIgd2lkdGg9IjQ3LjEyNTgiIGhlaWdodD0iMTIuNzc2OCIgcng9IjIiIGZpbGw9IiNGMDcwMjgiLz4KPC9nPgo8ZyBmaWx0ZXI9InVybCgjZmlsdGVyMF9kKSI+CjxwYXRoIGQ9Ik01MS42OTEzIDU0LjI0MThDNTIuNDgxNyA1My44ODE2IDUzLjM4OTUgNTMuODgxNiA1NC4xNzk5IDU0LjI0MThMNzIuODQ2NiA2Mi43NTA0QzczLjYyNjkgNjMuMTA2MSA3My42MjcgNjQuMjE0NiA3Mi44NDY2IDY0LjU3MDJMNTQuMTc5OSA3My4wNzg4QzUzLjM4OTUgNzMuNDM5IDUyLjQ4MTcgNzMuNDM5IDUxLjY5MTMgNzMuMDc4OEwzMy4wMjQ2IDY0LjU3MDJDMzIuMjQ0MyA2NC4yMTQ2IDMyLjI0NDMgNjMuMTA2MSAzMy4wMjQ2IDYyLjc1MDRMNTEuNjkxMyA1NC4yNDE4WiIgZmlsbD0idXJsKCNwYWludDBfbGluZWFyKSIvPgo8cGF0aCBkPSJNNTEuNjkxMyA0NS44OTUxQzUyLjQ4MTcgNDUuNTM0OCA1My4zODk1IDQ1LjUzNDggNTQuMTc5OSA0NS44OTUxTDcyLjg0NjYgNTQuNDAzNkM3My42MjY5IDU0Ljc1OTMgNzMuNjI3IDU1Ljg2NzggNzIuODQ2NiA1Ni4yMjM1TDU0LjE3OTkgNjQuNzMyQzUzLjM4OTUgNjUuMDkyMyA1Mi40ODE3IDY1LjA5MjMgNTEuNjkxMyA2NC43MzJMMzMuMDI0NiA1Ni4yMjM1QzMyLjI0NDMgNTUuODY3OCAzMi4yNDQzIDU0Ljc1OTMgMzMuMDI0NiA1NC40MDM2TDUxLjY5MTMgNDUuODk1MVoiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik01MS42OTEzIDM3LjU2NzJDNTIuNDgxNyAzNy4yMDY5IDUzLjM4OTUgMzcuMjA2OSA1NC4xNzk5IDM3LjU2NzJMNzIuODQ2NiA0Ni4wNzU3QzczLjYyNjkgNDYuNDMxNCA3My42MjcgNDcuNTM5OSA3Mi44NDY2IDQ3Ljg5NTZMNTQuMTc5OSA1Ni40MDQxQzUzLjM4OTUgNTYuNzY0NCA1Mi40ODE3IDU2Ljc2NDQgNTEuNjkxMyA1Ni40MDQxTDMzLjAyNDYgNDcuODk1NkMzMi4yNDQzIDQ3LjUzOTkgMzIuMjQ0MyA0Ni40MzE0IDMzLjAyNDYgNDYuMDc1N0w1MS42OTEzIDM3LjU2NzJaIiBmaWxsPSJ1cmwoI3BhaW50MV9saW5lYXIpIi8+CjwvZz4KPGNpcmNsZSBjeD0iNjIuODgyOCIgY3k9IjMyLjUiIHI9IjEzLjUiIGZpbGw9IndoaXRlIiBzdHJva2U9IiNGRkE3NzYiIHN0cm9rZS13aWR0aD0iMiIvPgo8cGF0aCBkPSJNNTcgMzUuNzVWMzNDNTcgMzIuNDQ3NyA1Ny40NDc3IDMyIDU4IDMySDY4QzY4LjU1MjMgMzIgNjkgMzIuNDQ3NyA2OSAzM1YzNyIgc3Ryb2tlPSIjRjA3MDI4IiBzdHJva2Utd2lkdGg9IjEuMjUiLz4KPHBhdGggZD0iTTYzIDI4TDYzIDM2IiBzdHJva2U9IiNGMDcwMjgiIHN0cm9rZS13aWR0aD0iMS4yNSIvPgo8Y2lyY2xlIGN4PSI2MyIgY3k9IjM3IiByPSIyIiBmaWxsPSIjRjA3MDI4Ii8+CjxjaXJjbGUgY3g9IjU3IiBjeT0iMzciIHI9IjIiIGZpbGw9IiNGMDcwMjgiLz4KPGNpcmNsZSBjeD0iNjkiIGN5PSIzNyIgcj0iMiIgZmlsbD0iI0YwNzAyOCIvPgo8cGF0aCBkPSJNNjMgMjRMNjUuNTk4MSAyOC41SDYwLjQwMTlMNjMgMjRaIiBmaWxsPSIjRjA3MDI4Ii8+CjxkZWZzPgo8ZmlsdGVyIGlkPSJmaWx0ZXIwX2QiIHg9IjE3LjQzOTUiIHk9IjI4LjI5NyIgd2lkdGg9IjcwLjk5MjIiIGhlaWdodD0iNjYuMDUyIiBmaWx0ZXJVbml0cz0idXNlclNwYWNlT25Vc2UiIGNvbG9yLWludGVycG9sYXRpb24tZmlsdGVycz0ic1JHQiI+CjxmZUZsb29kIGZsb29kLW9wYWNpdHk9IjAiIHJlc3VsdD0iQmFja2dyb3VuZEltYWdlRml4Ii8+CjxmZUNvbG9yTWF0cml4IGluPSJTb3VyY2VBbHBoYSIgdHlwZT0ibWF0cml4IiB2YWx1ZXM9IjAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDEyNyAwIiByZXN1bHQ9ImhhcmRBbHBoYSIvPgo8ZmVPZmZzZXQgZHk9IjYiLz4KPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iNy41Ii8+CjxmZUNvbG9yTWF0cml4IHR5cGU9Im1hdHJpeCIgdmFsdWVzPSIwIDAgMCAwIDAuOTY0NzA2IDAgMCAwIDAgMC41MDU4ODIgMCAwIDAgMCAwLjE5MjE1NyAwIDAgMCAwLjQ0IDAiLz4KPGZlQmxlbmQgbW9kZT0ibm9ybWFsIiBpbjI9IkJhY2tncm91bmRJbWFnZUZpeCIgcmVzdWx0PSJlZmZlY3QxX2Ryb3BTaGFkb3ciLz4KPGZlQmxlbmQgbW9kZT0ibm9ybWFsIiBpbj0iU291cmNlR3JhcGhpYyIgaW4yPSJlZmZlY3QxX2Ryb3BTaGFkb3ciIHJlc3VsdD0ic2hhcGUiLz4KPC9maWx0ZXI+CjxsaW5lYXJHcmFkaWVudCBpZD0icGFpbnQwX2xpbmVhciIgeDE9IjI2LjUxNTUiIHkxPSI1MS45MTk0IiB4Mj0iNzguMzY3IiB5Mj0iNjAuMTczOCIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgo8c3RvcCBzdG9wLWNvbG9yPSIjRUE1QjRGIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI0Y5QzQ1MiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9InBhaW50MV9saW5lYXIiIHgxPSIyNi41MTU1IiB5MT0iMzUuMjQ0NyIgeDI9Ijc4LjM2NyIgeTI9IjQzLjQ5OTEiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agc3RvcC1jb2xvcj0iI0VBNUI0RiIvPgo8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNGOUM0NTIiLz4KPC9saW5lYXJHcmFkaWVudD4KPC9kZWZzPgo8L3N2Zz4K"></img>

**Mergeable**: One of the most powerful features of whylogs profiles is their mergeability. Mergeability means that whylogs profiles can be combined together to form new profiles which represent the aggregate of their constituent profiles. This enables logging for distributed and streaming systems, and allows users to view aggregated data across any time granularity.


## Visualizing Profiles<a name="visualizing-profiles" />

### Multiple profile plots

To view your logger profiles you can use, methods within `whylogs.viz`: 

```python
vizualization = ProfileVisualizer()
vizualization.set_profiles([profile_day_1, profile_day_2])
figure= vizualization.plot_distribution("<feature_name>")
figure.savefig("/my/image/path.png")
```

Individual profiles are saved to disk, AWS S3, or WhyLabs API, automatically when loggers are closed, per the configuration found in the Session configuration.

Current profiles from active loggers can be loaded from memory with:
```python
profile = logger.profile()
```

### Profile viewer

You can also load a local profile viewer, where you upload the `json` summary file. The default path for the json files is set as `output/{dataset_name}/{session_id}/json/dataset_profile.json`.

```python
from whylogs.viz import profile_viewer
profile_viewer()
```

This will open a viewer on your default browser where you can load a profile json summary, using the `Select JSON profile` button:
Once the json is selected you can view your profile's features and 
associated and statistics.

<img src="https://whylabs-public.s3-us-west-2.amazonaws.com/assets/whylogs-viewer.gif" title="whylogs HTML viewer demo">

## Features


whylogs collects approximate statistics and sketches of data on a column-basis into a statistical profile. These metrics include:

- Simple counters: boolean, null values, data types.
- Summary statistics: sum, min, max, median, variance.
- Unique value counter or cardinality: tracks an approximate unique value of your feature using HyperLogLog algorithm.
- Histograms for numerical features. whyLogs binary output can be queried to with dynamic binning based on the shape of your data.
- Top frequent items (default is 128). Note that this configuration affects the memory footprint, especially for text features.

Some other key features about whylogs:

- Accurate data profiling: whylogs calculates statistics from 100% of the data, never requiring sampling, ensuring an accurate representation of data distributions
- Lightweight runtime: whylogs utilizes approximate statistical methods to achieve minimal memory footprint that scales with the number of features in the data
- Any architecture: whylogs scales with your system, from local development mode to live production systems in multi-node clusters, and works well with batch and streaming architectures
- Configuration-free: whylogs infers the schema of the data, requiring zero manual configuration to get started
- Tiny storage footprint: whylogs turns data batches and streams into statistical fingerprints, 10-100MB uncompressed
- Unlimited metrics: whylogs collects all possible statistical metrics about structured or unstructured data


## Data Types<a name="data-types" />
Whylogs supports both structured and unstructured data, specifically: 

| Data type  | Features | Notebook Example |
| --- | --- | ---|
|Structured Data | Distribution, cardinality, schema, counts, missing values | [Getting started with structured data](https://github.com/whylabs/whylogs-examples/blob/mainline/python/GettingStarted.ipynb) | 
| Images | exif metadata, derived pixels features,  bounding boxes | [Getting started with images](https://github.com/whylabs/whylogs-examples/blob/mainline/python/Logging_Images.ipynb) |
| Video  | In development  | [Github Issue #214](https://github.com/whylabs/whylogs/issues/214) |
| Tensors | derived 1d features (more in developement) | [Github Issue #216](https://github.com/whylabs/whylogs/issues/216) |
| Text | top k values, counts, cardinality | [String Features](https://github.com/whylabs/whylogs/blob/mainline/examples/String_Features.ipynb) |
| Audio | In developement | [Github Issue #212](https://github.com/whylabs/whylogs/issues/212) | 


## Integrations

![current integration](images/integrations.001.png)
| Integration | Features | Resources |
| --- | --- | ---  | 
| Spark | Run whylogs in Apache Spark environment|  <ul><li>[Code Example](https://github.com/whylabs/whylogs-examples/blob/mainline/scala/src/main/scala/WhyLogsDemo.scala)</li></ul> | 
| Pandas | Log and monitor any pandas dataframe |  <ul><li>[Notebook Example](https://github.com/whylabs/whylogs-examples/blob/mainline/python/logging_example.ipynb)</li><li>[whylogs: Embrace Data Logging](https://whylabs.ai/blog/posts/whylogs-embrace-data-logging)</li></ul>  |
| Kafka | Log and monitor Kafka topics with whylogs| <ul><li>[Notebook Example](https://github.com/whylabs/whylogs-examples/blob/mainline/python/Kafka.ipynb)</li><li> [Integrating whylogs into your Kafka ML Pipeline](https://whylabs.ai/blog/posts/integrating-whylogs-into-your-kafka-ml-pipeline) </li></ul>|
| MLflow | Enhance MLflow metrics with whylogs:  | <ul><li>[Notebook Example](https://github.com/whylabs/whylogs-examples/blob/mainline/python/MLFlow%20Integration%20Example.ipynb)</li><li>[Streamlining data monitoring with whylogs and MLflow](https://whylabs.ai/blog/posts/on-model-lifecycle-and-monitoring)</li></ul> |
| Github actions | Unit test data with whylogs and github actions| <ul><li>[Notebook Example](https://github.com/whylabs/whylogs-examples/tree/mainline/github-actions)</li></ul> |
| RAPIDS |  Use whylogs in RAPIDS environment | <ul><li>[Notebook Example](https://github.com/whylabs/whylogs-examples/blob/mainline/python/RAPIDS%20GPU%20Integration%20Example.ipynb)</li><li>[Monitoring High-Performance Machine Learning Models with RAPIDS and whylogs](https://whylabs.ai/blog/posts/monitoring-high-performance-machine-learning-models-with-rapids-and-whylogs)</li></ul> |
| Java | Run whylogs in Java environment| <ul><li>[Notebook Example](https://github.com/whylabs/whylogs-examples/blob/mainline/java/demo1/src/main/java/com/whylogs/examples/WhyLogsDemo.java)</li></ul>  |
| Docker | Run whylogs as in Docker |  <ul><li>[Rest Container](https://docs.whylabs.ai/docs/integrations-rest-container)</li></ul>| 
| AWS S3 |  Store whylogs profiles in S3 | <ul><li>[S3 example](https://github.com/whylabs/whylogs-examples/blob/mainline/python/S3%20example.ipynb)</li></ul>

## Examples
For a full set of our examples, please check out [whylogs-examples](https://github.com/whylabs/whylogs-examples).

Check out our example notebooks with Binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/whylabs/whylogs-examples/HEAD)
- [Getting Started notebook](https://github.com/whylabs/whylogs-examples/blob/mainline/python/GettingStarted.ipynb)
- [Logging Example notebook](https://github.com/whylabs/whylogs-examples/blob/mainline/python/logging_example.ipynb)
- [Logging Images](https://github.com/whylabs/whylogs-examples/blob/mainline/python/Logging_Images.ipynb)
- [MLflow Integration](https://github.com/whylabs/whylogs-examples/blob/mainline/python/MLFlow%20Integration%20Example.ipynb)


## Roadmap

whylogs is maintained by [WhyLabs](https://whylabs.ai).

## Community

If you have any questions, comments, or just want to hang out with us, please join [our Slack channel](http://join.slack.whylabs.ai/).

## Contribute

We welcome contributions to whylogs. Please see our [contribution guide](https://github.com/whylabs/whylogs/blob/mainline/CONTRIBUTING.md) and our [development guide](https://github.com/whylabs/whylogs/blob/mainline/DEVELOPMENT.md) for details.
