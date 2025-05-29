from http import HTTPStatus
import json
from behave import *
import jsonschema
from jsonpath import jsonpath
import requests
from assertpy import assert_that, fail



@given('a request url {url}')
def step_url(context, url):
    context.url = url
    
@given('indexes from {start} to {end}')
def step_url(context, start, end):
    context.indexes = [i for i in range(start, end)]


@given('a request json payload')
def step_impl(context):
    json_dict = context.text
    context.payload = json_dict


@when('the request sends {method}')
def step_request(context, method):
    headers = json.loads("""{
                            "Content-Type": "application/json"
                        }""")
    context.response = requests.request(
        method=method, url=context.url, headers=headers, data=context.payload)


@then('response is OK')
def step_response(context):
    assert 200 <= context.response.status_code < 300, "Response code is different: %s" % context.response.status_code + \
        " Error: " + str(context.response.content)

@then('the response status is {expected_status}')
def step_response(context, expected_status):
    expected_status = _as_numeric_status(expected_status)
    actual_status = context.response.status_code
    assert_that(actual_status).is_equal_to(expected_status)

@then('the response json matches')
def step_impl(context):
    schema = json.loads(context.text)
    json_body = context.response.content
    jsonschema.validate(json_body, schema)
    
@then('the response json at {path} is equal to {expected_value}')
def step_impl(context, path, expected_value):
    actual_value = context.response.json()[path]
    assert_that(expected_value).is_equal_to(actual_value)
    
def _as_numeric_status(status):
    status = status.replace(' ', '_')
    numeric_status = getattr(HTTPStatus, status.upper(), None)
    if not numeric_status:
        numeric_status = int(status)
    return numeric_status
