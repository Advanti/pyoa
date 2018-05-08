import json
from bson import json_util
from collections import OrderedDict


class DefaultJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            serializable = obj.isoformat()
        elif isinstance(obj, Decimal):
            serializable = float(obj)
        else:
            serializable = json_util.default(obj)
        return serializable


class DefaultJSONDecoder(json.JSONDecoder):
    def __init__(self, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True,
                 object_pairs_hook=None):
        json.JSONDecoder.__init__(
            self, object_hook=json_util.object_hook if object_hook is None else object_hook, parse_float=parse_float,
            parse_int=parse_int, parse_constant=parse_constant, strict=strict,
            object_pairs_hook=OrderedDict if object_pairs_hook is None else object_pairs_hook)
