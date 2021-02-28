# Google functions code that returns the benchmark results for calculating factorial
# Reporting
import time
import statistics
# import logging
from google.cloud import logging
from google.cloud.logging.resource import Resource

log_client = logging.Client()

# This is the resource type of the log
log_name = 'projects/fyp-hello-world-g/logs/cloudaudit.googleapis.com%2Factivity'

# Inside the resource, nest the required labels specific to the resource type
res = Resource(type="cloud_function",
               labels={
                   "function_name": "python-factorial-code",
                   "region": "europe-west2"
               },
               )
logger = log_client.logger(log_name.format("fyp-hello-world-g"))
logger.log_struct(
    {"message": "message string to log"}, resource=res, severity='ERROR')


def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        msg = request.args.get('message')
        benchmark(msg)
        return "Benchmark finished"
    elif request_json and 'message' in request_json:
        msg = request_json.get('message')
        benchmark(msg)
        return "Benchmark finished "
    else:
        return f'factorial benchmark did not run'


def factorial_function(num):
    num = int(num)
    factorial = 1
    # check if the number is negative, positive or zero
    if num < 0:
        return "Sorry, factorial does not exist for negative numbers"
    else:
        for i in range(1, num + 1):
            factorial = factorial * i
        return factorial


def benchmark(num):
    throughput_time = {"factorial": []}
    average_duration_time = {"factorial": []}

    for i in range(10000):  # adjust accordingly so whole thing takes a few sec
        logger.info('factorial execution beginning')
        t0 = time.time()
        factorial_function(num)
        t1 = time.time()
        logger.info('factorial function ended, calculating metrics')
        throughput_time["factorial"].append(1 / ((t1 - t0) * 1000))
        average_duration_time["factorial"].append(((t1 - t0) * 1000) / 1)

    for name, numbers in throughput_time.items():
        length = len(numbers)
        median = statistics.median(numbers)
        mean = statistics.mean(numbers)
        stdev = statistics.stdev(numbers)
        logger.info('FUNCTION:', name, 'Used', length, 'times')
        logger.info('\tMEDIAN', median, ' ops/s')
        logger.info('\tMEAN  ', mean, ' ops/s')
        logger.info('\tSTDEV ', stdev, ' ops/s')

    for name, numbers in average_duration_time.items():
        length = len(numbers)
        median = statistics.median(numbers)
        mean = statistics.mean(numbers)
        stdev = statistics.stdev(numbers)
        logger.info('FUNCTION:', name, 'Used', length, 'times')
        logger.info('\tMEDIAN', median, ' ops/s')
        logger.info('\tMEAN  ', mean, ' ops/s')
        logger.info('\tSTDEV ', stdev, ' ops/s')

    logger.critical("The benchmark is finished properly")
