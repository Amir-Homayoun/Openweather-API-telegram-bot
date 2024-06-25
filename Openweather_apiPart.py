import json

import requests

import dicttoxml

# finding appropriate data for show---------------------------------
import pycountry
import datetime
from mtranslate import translate
import essential_dictionaries

main_file_name_json = []
main_file_name_xml = []

def telegram_weather_sender(selected_city,user_name):
    for i in [1,2,3,4,5,6,7,8,9,0]:
        if str(i) in selected_city:
            return """Earth doesn't have any city that has number in it⚠️\n\nPlease try again? 🔄 """
    city_name=translate(selected_city,'en','auto')
    print(city_name)
    api_key='9adc78b0ec8764ec5dab0374c0c3a61c'
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city_name}"

    response = requests.get(url)
    data = response.json()
    # making files for sending---------------------------------------------------


    try:
        if data['message']=='city not found':
            return ["""There is not city called""","'"+selected_city+"'",' error⚠️\nPlease try again? 🔄']
    except:
        None

    def json_file():
        file_name=f"weather for {city_name} situation on {str(datetime.datetime.fromtimestamp(data['dt']))[0:10]} at{str(datetime.datetime.fromtimestamp(data['dt']))[10:]}.json "
        for i in file_name:
            if i==':':
                main_file_name_json.append('-')
            else:
                main_file_name_json.append(i)

        f=open(''.join(main_file_name_json),'w')
        json.dump(data,f,indent=4)
    json_file()
    def xml_file():
        # Convert dictionary to XML
        xml_data = dicttoxml.dicttoxml(data)

        # Create XML file

        file_name=f"weather situation for {city_name} on {str(datetime.datetime.fromtimestamp(data['dt']))[0:10]} at{str(datetime.datetime.fromtimestamp(data['dt']))[10:]}.xml "
        for i in file_name:
            if i==':':
                main_file_name_xml.append('-')
            else:
                main_file_name_xml.append(i)

        with open(''.join(main_file_name_xml), 'wb') as f:
            f.write(xml_data)
    xml_file()

    # finding appropriate data for show---------------------------------
    # country code
    country_name=[]
    def get_country_name(country_code):
        country_name.clear()
        try:

            country = pycountry.countries.get(alpha_2=country_code.upper())
            x=country.name
            country_name.append(x.split())
        except KeyError:
            return "Country not found"
    get_country_name(data['sys']['country'])
    def country_emoji(given_country):
        country_emoji=essential_dictionaries.country_emojis
        check=0
        for i in country_emoji.items():
            if i[0]==given_country:
                check+=1
                return given_country+i[1]
        if check>0:
            return given_country



    # base info emoji
    def base_info_emoji(base):
        if base=='satelite':
            return f'{base} 🛰'
        else:
            return base
    # weather emoji
    weather_info=[]
    def weather_emoji(weather):
        weather_info.clear()
        weather_emojis = {"Clear sky": "☀️","Few clouds": "🌤️","Scattered clouds": "🌥️","Broken clouds": "🌦️","Shower rain": "🌧️","Rain": "🌧️","Thunderstorm": "⛈️","Snow": "❄️","Mist": "🌫️","Smoke": "🌫️🔥","Haze": "🌫️","Dust": "💨","Fog": "🌫️"}
        for i in weather_emojis.items():
            if weather.lower() == i[0].lower():
                weather_info.append(weather+i[1])
        if len(weather_info)==0:
            weather_info.append(weather)
    weather_emoji(data["weather"][0]['description'])

    return f"""
Hi again {user_name.capitalize()}👋
Here is weather situation for {city_name}🌏!

Date of this information : {str(datetime.datetime.fromtimestamp(data['dt']))}⏰
Country : {country_emoji(country_name[0][0][0:country_name[0][0].find(',')])}
base of information : {base_info_emoji(data['base'])}

sunrise : {datetime.datetime.fromtimestamp(data['sys']['sunrise'])}🌅
sunset : {datetime.datetime.fromtimestamp(data['sys']['sunset'])}🌇

weather : {weather_info[0]}
clouds : {data['clouds']['all']}☁️

Temperature : {str(float(data['main']['temp'])-273.15)}°C 🌡
How it feels : {str(float(data['main']['feels_like'])-273.15)}°C 🌡
Minimum temperature : {str(float(data['main']['temp_min'])-273.15)}°C 🌡
Maximum temperature : {str(float(data['main']['temp_max'])-273.15)}°C 🌡
Atmospheric pressure : {float(data['main']['pressure']) / 1013.25}atm OR {data['main']['pressure']}hPa
Humidity : {data['main']['humidity'] }%

Wind speed : {data['wind']['speed']} 💨༄࿐ ࿔*:･ﾟ🍃
Wind degree : {data['wind']['deg']}
    
    """
# print(telegram_weather_sender('tehran'))
# os.remove(''.join(main_file_name_json))
# link of more information of this api= https://openweathermap.org/current#name