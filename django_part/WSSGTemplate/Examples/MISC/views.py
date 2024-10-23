from typing import Type

from django.http import HttpResponse

from WSSGTemplate.Core import utilities
from WSSGTemplate.Core.models import *

# TODO instead of getting the response, it should only get the model and then an wrapper to get the json

'''
a generic method to get some specific object by their id
mostly getting the model and converting it into json
id= for identification
model= which Model e.g models.py-> Player
'''


def generic_get_by_id(model: Type[models.Model], **kwargs):
    model_instance = utilities.search_object_by_attribute(model, **kwargs)
    return model_instance


# basic generic method to reduce code size, since it always works in the same way
# used for setting an object according to the given json string

def generic_set_by_id(dict_values, ):
    model_instance = generic_get_by_id(dict_values["id"], )
    if model_instance is None:
        return utilities.server_message_response(message=f'no object was found with id: {dict_values["id"]}')

    model_instance = utilities.jsondict_to_obj(model_instance, dict_values)

    model_instance.save()
    return utilities.server_message_response(status=200, identifier="MESSAGE",
                                             message=f'Object  was saved or updated')


# basic generic method to reduce code size, since it always works in the same way
# used for getting  ALL objects of a class
def generic_get_all(model: Type[models.Model]):
    model_instances = None
    if model is not None:
        model_instances = model.objects.all()

    return model_instances


def get_by_id_with_communication(request, model, **kwargs):
    result_from_check = utilities.basic_request_check(request, ["id"])

    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    id_req = result_from_check["id"]

    model_instance = generic_get_by_id(model, **kwargs)
    if model_instance is None:
        return utilities.server_message_response(f"instance of {id_req} not found")
    else:
        result = utilities.convert_specific_fields(utilities.get_json_from_instance(model_instance))
        print(result)
        return utilities.server_message_response(status=200, identifier="MESSAGE",
                                                 message=f"{result}")


def get_all_with_communication(request, model: Type[models.Model]):
    result_from_check = utilities.basic_request_check(request)
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    model_instances = generic_get_all(model)
    res = utilities.get_json_from_instances(model_instances)

    return utilities.server_message_response(status=200, identifier="MESSAGE", message=f"{res}")
