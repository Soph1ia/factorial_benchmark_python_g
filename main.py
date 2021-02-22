# Google functions code that returns the benchmark results for calculating factorial

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
    print("The request received is: ", request)
    if request.args and 'message' in request.args:
        msg = request.args.get('message')
        return factorial_function(msg)
    elif request_json and 'message' in request_json:
        msg = request_json.get('message')
        return factorial_function(msg)
    else:
        return f'Hello World!'


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
