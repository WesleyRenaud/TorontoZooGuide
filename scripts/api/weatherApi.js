import {
   OPEN_WEATHER_API_KEY,
   TORONTO_ZOO_COORDINATES,
} from '../config/appConfig.js';

export function fetchForecastTemp(dateStr) {
   return fetch(
      `https://api.openweathermap.org/data/2.5/forecast?lat=${TORONTO_ZOO_COORDINATES.lat}&lon=${TORONTO_ZOO_COORDINATES.lon}&units=metric&appid=${OPEN_WEATHER_API_KEY}`
   )
      .then(res => res.json())
      .then(data => {
         const daily = (data.list || []).filter(f => String(f.dt_txt || '').startsWith(dateStr));
         if (daily.length === 0) return null;

         return daily.reduce((sum, f) => sum + Number(f.main?.temp ?? 0), 0) / daily.length;
      });
}
