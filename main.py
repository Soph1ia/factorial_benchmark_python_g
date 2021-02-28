# Google functions code that returns the benchmark results for calculating factorial
# Reporting
import time
import statistics
import logging
import google.cloud.logging


def setup_logging():
    client = google.cloud.logging.Client()

    client.get_default_handler()
    client.setup_logging()


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
    setup_logging()
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

    for i in range(20):  # adjust accordingly so whole thing takes a few sec
        logging.info('factorial execution beginning')
        t0 = time.time()
        factorial_function(num)
        t1 = time.time()
        logging.info('factorial function ended, calculating metrics')
        throughput_time["factorial"].append(1 / ((t1 - t0) * 1000))
        average_duration_time["factorial"].append(((t1 - t0) * 1000) / 1)

    for name, numbers in throughput_time.items():
        length = str(len(numbers))
        median = str(statistics.median(numbers))
        mean = str(statistics.mean(numbers))
        stdev = str(statistics.stdev(numbers))
        output = "FUNCTION {} used {} times. > MEDIAN {} ops/s > MEAN {} ops/s  > STDEV {} ops/s".format(name, length,
                                                                                                         median, mean,
                                                                                                         stdev)
        logging.info(output)

    for name, numbers in average_duration_time.items():
        length = str(len(numbers))
        median = str(statistics.median(numbers))
        mean = str(statistics.mean(numbers))
        stdev = str(statistics.stdev(numbers))
        output = "FUNCTION {} used {} times. > MEDIAN {} ops/s > MEAN {} ops/s  > STDEV {} ops/s".format(name, length,
                                                                                                         median, mean,
                                                                                                         stdev)
        logging.info(output)

    logging.critical("The benchmark is finished properly")


if __name__ == '__main__':
    benchmark(5)
