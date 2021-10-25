class RequestError(Exception):
    """ Reject Request Error from venue

    Args:
        Exception ([type]): [description]
    """
    pass

class InvalidArgumentError(Exception):
    """ Private  function argument error

    Args:
        Exception ([type]): [description]
    """
    pass

class OrderParamException(Exception):
    """  Invalid Order param error

    Args:
        Exception ([type]): [description]
    """
    pass

class  CapacityException(Exception):
    """ Capacity check by myself error

    Args:
        Exception ([type]): [description]
    """
    pass