import phonenumbers
from phonenumbers import geocoder, timezone, carrier
from colorama import Fore, Style
import folium
import argparse
import os
import requests
from opencage.geocoder import OpenCageGeocode

def process_number(number):
    parsed_number = phonenumbers.parse(number, None)
    if not phonenumbers.is_valid_number(parsed_number):
        print(f"{Fore.RED}[-] Invalid phone number")
        return

    print(f"{Fore.GREEN}[+] Phone Number: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
    if carrier.name_for_number(parsed_number, 'en'):
        print(f"{Fore.GREEN}[+] Carrier: {carrier.name_for_number(parsed_number, 'en')}")
    else:
        print(f"{Fore.RED}[-] Carrier: Unknown")

    if timezone.time_zones_for_number(parsed_number):
        print(f"{Fore.GREEN}[+] Timezone: {timezone.time_zones_for_number(parsed_number)[0]}")
    else:
        print(f"{Fore.RED}[-] Timezone: Unknown")

    return geocoder.description_for_number(parsed_number, "en")

def get_location(location):
    global latitude, longitude
    geocoder = OpenCageGeocode(key="YOUR_API_KEY")
    results = geocoder.geocode(location)
    if results:
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']

def draw_map():
    try:
        my_map = folium.Map(location=[latitude, longitude], zoom_start=9)
        folium.Marker([latitude, longitude], popup=location).add_to(my_map)
        cleaned_phone_number = "".join(e for e in args.phone_number if e.isalnum())
        file_name = f"{cleaned_phone_number}.html"
        my_map.save(file_name)
        print(f"[+] See Aerial Coverage at: {os.path.abspath(file_name)}")
    except Exception as e:
        print(f"{Fore.RED}[-] Could not get Aerial coverage for this number. Error: {str(e)}")

if __name__ == "__main__":
    from colorama import init
    init(convert=True)
    arg_parser = argparse.ArgumentParser(description="Get approximate location of a Phone number.")
    arg_parser.add_argument("-p", "--phone", dest="phone_number", type=str, help="Phone number to track")
    args = arg_parser.parse_args()

    location = process_number(args.phone_number)
    if location:
        print(f"{Fore.GREEN}[+] Location: {location}")
        get_location(location)
        draw_map()