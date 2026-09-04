import {
   OPEN_WEATHER_API_KEY,
   TORONTO_ZOO_COORDINATES,
} from '../config/appConfig.js';
import { VisitDateRules } from '../visitDates/visitDateRules.js';

function weatherApiUrl(path) {
   return (
      `https://api.openweathermap.org/data/2.5/${path}`
      + `?lat=${TORONTO_ZOO_COORDINATES.lat}`
      + `&lon=${TORONTO_ZOO_COORDINATES.lon}`
      + `&units=metric`
      + `&appid=${OPEN_WEATHER_API_KEY}`
   );
}

function isTodayDate(dateStr) {
   return dateStr === VisitDateRules.toISODate(VisitDateRules.getToday());
}

function fetchCurrentTemp() {
   return fetch(weatherApiUrl('weather'))
      .then(res => res.json())
      .then(data => {
         const temp = Number(data.main?.temp);
         return Number.isFinite(temp) ? temp : null;
      });
}

function fetchForecastDateTemp(dateStr) {
   return fetch(
      weatherApiUrl('forecast')
   )
      .then(res => res.json())
      .then(data => {
         const daily = (data.list || []).filter(f => String(f.dt_txt || '').startsWith(dateStr));
         if (daily.length === 0) return null;

         return daily.reduce((sum, f) => sum + Number(f.main?.temp ?? 0), 0) / daily.length;
      });
}

export class WeatherApi {
   static fetchWeatherTempForDate(dateStr) {
      if (isTodayDate(dateStr)) {
         return fetchCurrentTemp();
      }

      return fetchForecastDateTemp(dateStr);
   }
}
