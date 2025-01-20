

def validate_api_response(data):
    if data is None:
        return None
    if isinstance(data,list) or isinstance(data,dict):
        if not data:
            return None
        return data
    return None

def validate_singular_api_response(data):
    if data is None:
        return None
    if isinstance(data,list):
        if not data:
            return None
        return data[0]
    if isinstance(data,dict):
        if not data:
            return None
        return data
    return None