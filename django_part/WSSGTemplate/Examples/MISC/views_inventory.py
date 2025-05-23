from django.http import HttpResponse

from WSSGTemplate.Core import utilities
from WSSGTemplate.Core.models import *
from WSSGTemplate.Examples.MISC import views

'''
get_inventory_by_id receives: "id"
get inventory by the  owner's name
'''


def get_inventory_by_id(request):
    return views.get_by_id_with_communication(request, Inventory)


'''
get_inventories receives: nothing
get all inventories
'''


def get_inventories(request):
    return views.get_all_with_communication(request, Inventory)


'''
set_inventory_by_id receives: "id" optional: TODO
set a inventory with the given the optional keys
'''


def set_inventory_by_id(request):
    result_from_check = utilities.basic_request_check(request)
    if isinstance(result_from_check, HttpResponse):
        return result_from_check

    extracted_values = utilities.extract_request_values(request)

    return views.generic_set_by_id(extracted_values, Inventory)
