from enum import Enum

class VehicleFeatureChoice(Enum):
    AC = 'AC'
    NON_AC = 'Non AC'

def django_enum(cls):
    # decorator needed to enable enums in django templates
    cls.do_not_call_in_templates = True
    return cls

@django_enum
class AmenitiesChoice(Enum):
    lodging = "Lodging"
    petrol_pump = "Petrol Pump"
    eating_place = "Eating Place"


@django_enum
class VehicleTypeChoice(Enum):
    hatchback = "HATCHBACK"
    sedan = "SEDAN"
    suv = "SUV"
    minibus = "MINIBUS"
    sedan_premium = "SEDAN - PREMIUM"
    sedan_business = "SEDAN - BUSINEESS CLASS"
    luxury = "LUXURY"

@django_enum
class ReviewStatusChoice(Enum):
    approved = "APPROVED"
    rejected = "REJECTED"
    new = "NEW"

@django_enum
class ReviewActionChoice(Enum):
    approve = "APPROVE"
    reject = "REJECT"
    delete = "DELETE"
