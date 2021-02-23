# Google functions code that returns the benchmark results for calculating factorial
# Reporting
import time
import statistics


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
        return str(benchmark(msg))
    elif request_json and 'message' in request_json:
        msg = request_json.get('message')
        return str(benchmark(msg))
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
        print('benchmark beginning')
        t0 = time.time()
        factorial_function(num)
        t1 = time.time()
        print('Benchmark ended, calculating metrics')
        throughput_time["factorial"].append(1 / ((t1 - t0) * 1000))
        average_duration_time["factorial"].append(((t1 - t0) * 1000) / 1)

    for name, numbers in throughput_time.items():
        print('FUNCTION:', name, 'Used', len(numbers), 'times')
        print('\tMEDIAN', statistics.median(numbers), ' ops/s')
        print('\tMEAN  ', statistics.mean(numbers), ' ops/s')
        print('\tSTDEV ', statistics.stdev(numbers), ' ops/s')

    for name, numbers in average_duration_time.items():
        print('FUNCTION:', name, 'Used', len(numbers), 'times')
        print('\tMEDIAN', statistics.median(numbers), ' s/ops')
        print('\tMEAN  ', statistics.mean(numbers), ' s/ops')
        print('\tSTDEV ', statistics.stdev(numbers), ' s/ops')
