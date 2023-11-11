import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

def weather_api():

	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": 48.7651,
		"longitude": 11.4237,
		"current": ["temperature_2m", "precipitation", "rain", "showers", "snowfall", "weather_code"],
		"timezone": "Europe/Berlin",
		"forecast_days": 1
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	# print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
	# print(f"Elevation {response.Elevation()} m asl")
	# print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
	# print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

	# Current values. The order of variables needs to be the same as requested.
	current = response.Current()
	current_temperature_2m = current.Variables(0).Value()
	current_precipitation = current.Variables(1).Value()
	current_rain = current.Variables(2).Value()
	current_showers = current.Variables(3).Value()
	current_snowfall = current.Variables(4).Value()
	current_weather_code = current.Variables(5).Value()

	# print(f"Current time {current.Time()}")
	# print(f"Current temperature_2m {current_temperature_2m}")
	# print(f"Current precipitation {current_precipitation}")
	# print(f"Current rain {current_rain}")
	# print(f"Current showers {current_showers}")
	# print(f"Current snowfall {current_snowfall}")
	# print(f"Current weather_code {current_weather_code}")
	return current_temperature_2m, current_precipitation, current_rain, current_showers, current_snowfall, current_weather_code


def weather_sentence(current_weather_code, current_temperature_2m):
	weather_dict = {"Dry":[0,1,2,3],"Fog":[45,48],"Rain":[51,53,55,56,57,61,63,65,66,67,80,81,82],"Snow":[71,73,75,77,85,86],"Thunderstorm":[95,96,99]}

	temp_dict = {0:"Freezing",10:"Cold",15:"Moderate",20:"Warm",25:"Very Warm",100:"Hot"}

	for wetter, elem in weather_dict.items():
		if int(current_weather_code) in elem and wetter == "Dry":
			for temp, desc in temp_dict.items():
				if current_temperature_2m < temp:
					if desc == "Freezing":
						return "It's freezing! Take the bus unless you're brave, and don't forget to wear a coat!"
					elif desc == "Cold":
						return "It's pretty cold, a brisk walk might keep you warm, but bring a jacket!"
					elif desc == "Moderate":
						return "The weather is ok today, take the bus or walk, life is what you make of it!"
					elif desc == "Warm":
						return "It's quite warm, ditch the jacket, unless you need the pockets."
					elif desc == "Very Warm":
						return "It's very warm today, show off those guns!"
					elif desc == "Hot":
						return "Is it hot today, or is it just you?"
					else:
						raise ValueError
		elif int(current_weather_code) in elem:
			if wetter == "Fog":
				return "Conditions are foggy, be careful!"
			elif wetter == "Rain":
				return "It's raining, bring an umbrella and stay dry on the bus!"
			elif wetter == "Snow":
				return "It's snowing! Stay warm on the bus!"
			elif wetter == "Thunderstorm":
				return "It's stormy out, be careful!"
	else:
		return f'It\'s {current_temperature_2m} degrees.'

def weather() -> dict:
	current_temperature_2m, current_precipitation, current_rain, current_showers, current_snowfall, current_weather_code = weather_api()
	advice = weather_sentence(current_weather_code, current_temperature_2m)
	res = {"Advice": advice,"Data":[current_temperature_2m,current_precipitation,current_rain,current_showers,current_snowfall]}
	return res


