from Providers.VilniausVandenys import VilniausVandenys
from Providers.CHC import CHC
import os


items = [
    (VilniausVandenys, os.environ['VV_USERNAME'], os.environ['VV_PASSWORD']),
    (CHC, os.environ['CHC_USERNAME'], os.environ['CHC_PASSWORD']),
]

for provider_class, username, password in items:

    with provider_class(username=username, password=password) as provider:
        print(f"Provider:   {provider.provider}\n"
              f"Date:       {provider.year}-{provider.month}\n"
              f"Bill:       {provider.bill:.2f}")

        for service in provider.services:
            print(f"Service:    {service.name} ({service.bill:.2f})")
            if service.has_meter:
                print(f"\t\t\tFrom:  {service.meter.previous_reading:.2f} {service.meter.units}\n"
                      f"\t\t\tTo:    {service.meter.current_reading:.2f} {service.meter.units}\n"
                      f"\t\t\tDiff:  {service.meter.difference:.2f} {service.meter.units}")
