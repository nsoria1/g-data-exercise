from helper import query_metric

METRIC_1 = 'first_metric.sql'
METRIC_2 = 'second_metric.sql'

def metric1():
    return query_metric(METRIC_1)

def metric2():
    return query_metric(METRIC_2)