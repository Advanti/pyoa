from requests.auth import HTTPBasicAuth
import json
from bson import json_util
import base64
from codecs import encode
import datetime as dt
import pandas as pd
from requests import get, post
import pickle
from datetime import date
from decimal import Decimal

# initialize variables
dt_format = '%Y-%m-%d %H:%M:%S.%f'

# metadata parameters
request_key = 'request'
content_type_param_name = 'Content-Type'

# metadata parameter values
json_content_type = 'application/json'
serialized_content_type = 'application/octet-stream'
text_html_content_type = 'text/html'

# request parameters
subject_area_param_name = 'subject area'
request_type_param_name = 'request type'
resource_def_param_name = 'resource definition'
output_data_format_param_name = 'output data format'
output_data_categoricalize_param_name = 'output data make categorical'
input_data_param_name = 'data'
input_data_format_param_name = 'input data format'
dest_resource_name_param_name = 'destination resource name'
dest_resource_namespace_param_name = 'destination resource namespace'
src_resource_name_param_name = 'source resource name'
src_resource_namespace_param_name = 'source resource namespace'
max_row_count_param_name = 'max row count'
perspective_param_name = 'perspective'
entity_type_param_name = 'entity type'
data_elements_param_name = 'data elements'
distinct_param_name = 'distinct'
discovery_only_param_name = 'discovery only'
return_query_param_name = 'return query'
attribute_filters_param_name = 'attribute filters'

# request parameter values
request_type_get_data = 'get data'
request_type_put_data = 'put data'
request_type_del_data = 'delete data'
data_dataframe_format = 'data frame'
data_json_format = 'json'

# response variables
response_data_key = 'data'
response_query_key = 'query'
response_error_info_key = 'error info'
response_error_info_message_key = 'message'
response_error_info_file_key = 'file'
response_error_info_callable_key = 'callable'
response_error_info_line_no_key = 'line_no'
response_error_info_traceback_key = 'traceback'
response_error_info_type_key = 'type_name'


class Client(object):

    def __init__(self, host, access_key, secret_key, json_encoder, json_decoder):
        self._host = host
        self._access_key = access_key
        self._secret_key = secret_key
        self._json_encoder = json_encoder
        self._json_decoder = json_decoder

        pd.set_option('display.width', 1000)

    def request_headers(self, content_type):
        return {content_type_param_name: content_type,
                'Authorization': 'Basic %s' % base64.b64encode(encode('%s:%s' % (self._access_key, self._secret_key), encoding='utf-8'))}

    def serialize_to_json(self, obj):
        return json.dumps(obj, cls=self._json_encoder)

    def deserialize_json(self, obj):
        return json.loads(obj, cls=self._json_decoder)

    def process_error(self, content, status_code):
        has_error = False
        if status_code > 300:
            has_error = True
            print()
            if isinstance(content, dict):
                response_ei = content.get(response_error_info_key)
                if response_ei is not None:
                    print('ERROR INFO')
                    print('')
                    print(', '.join(['{} = {}'.format(key, response_ei[key]) for key in [
                        response_error_info_message_key, response_error_info_type_key,
                        response_error_info_file_key, response_error_info_callable_key,
                        response_error_info_line_no_key]]))
                    print()
                    response_tb = response_ei.get(
                        response_error_info_traceback_key)
                    if response_tb is not None:
                        [print(line) for line in response_tb]
                else:
                    [print('%s = %s' % (key, value))
                     for key, value in content.items()]
            else:
                raise Exception(
                    'Cannot process content python type of "%s".' % type(content.__name__))
        return has_error

    def response_content(self, response):
        content_type = response.headers['Content-Type']
        if content_type == json_content_type:
            content = self.deserialize_json(response.text)
        elif content_type == serialized_content_type:
            content = pickle.loads(response.content)
        elif content_type.startswith(text_html_content_type):
            content = {'text': response.text}
        else:
            raise Exception('Unknown content type "%s".' % content_type)
        return content

    def request(self, req):
        request_items = req[request_key]
        request_type = request_items[request_type_param_name]

        if request_type == request_type_get_data:
            request_func = get
            data_action = 'pulling'
            content_type = json_content_type
        else:
            request_func = post
            data_action = 'pushing' if request_type == request_type_put_data else 'deleting'
            if input_data_param_name in request_items:
                if isinstance(request_items[input_data_param_name], pd.DataFrame):
                    content_type = serialized_content_type
                else:
                    content_type = json_content_type
            else:
                content_type = json_content_type
        kwargs = {'json': self.serialize_to_json(req)} \
            if content_type == json_content_type else {'data': pickle.dumps(req)}

        response = request_func(
            '%s/data' % self._host, headers=self.request_headers(content_type), params={'Requested dt': dt.datetime.now().strftime(dt_format)}, **kwargs)

        # get response content
        content = self.response_content(response)

        # process error info
        self.process_error(content, response.status_code)

        return content.get('data')
