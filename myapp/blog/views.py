import requests
from datetime import datetime
from django.shortcuts import render
from .forms import CityForm
from decouple import config  # ✅ Import to read from .env

def index(request):
    weather_data = None
    forecast_data = []

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            api_key = config('API_KEY')  # ✅ Get API key from .env

            current_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'

            current_res = requests.get(current_url)
            forecast_res = requests.get(forecast_url)

            if current_res.status_code == 200 and forecast_res.status_code == 200:
                current = current_res.json()
                forecast = forecast_res.json()

                weather_data = {
                    'city': city,
                    'temperature': current['main']['temp'],
                    'description': current['weather'][0]['description'],
                    'icon': current['weather'][0]['icon'],
                    'humidity': current['main'].get('humidity', 'N/A'),
                    'wind_speed': current['wind'].get('speed', 'N/A'),
                }

                # Group forecast data by date, take 12:00 PM entry for each day
                seen_dates = set()
                for entry in forecast['list']:
                    date_str = entry['dt_txt']
                    if "12:00:00" in date_str:
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        date_label = date_obj.strftime('%A, %b %d')
                        if date_label not in seen_dates:
                            seen_dates.add(date_label)
                            forecast_data.append({
                                'date': date_label,
                                'temp': entry['main']['temp'],
                                'desc': entry['weather'][0]['description'].capitalize(),
                                'icon': entry['weather'][0]['icon'],
                            })
            else:
                weather_data = {'error': 'City not found'}
    else:
        form = CityForm()

    return render(request, 'blog/index.html', {
        'form': form,
        'weather': weather_data,
        'forecast': forecast_data
    })
