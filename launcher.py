from Providers.VilniausVandenys import VilniausVandenys
from Providers.CHC import CHC
import os


items = [
    (CHC, os.environ['CHC_USERNAME'], os.environ['CHC_PASSWORD']),
    (VilniausVandenys, os.environ['VV_USERNAME'], os.environ['VV_PASSWORD']),
]

for provider_class, username, password in items:

    with provider_class(username=username, password=password) as provider:
        provider.retrieve_current_data()
        print(f"Provider:   {provider.provider}\n"
              f"Month:      {str(provider.month)}\n"
              f"Bill:       {str(provider.bill)}\n")

        for meter in provider.meters:
            print(f"\tProvider:   {str(meter.provider)}\n"
                  f"\tDifference: {str(meter.difference)}\n"
                  f"\tTo:         {str(meter.current_reading)}\n"
                  f"\tFrom:       {str(meter.previous_reading)}\n")
