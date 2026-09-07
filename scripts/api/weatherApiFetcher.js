import { AppConfig } from '../config/appConfig.js';
import { VisitDateRules } from '../visitDates/visitDateRules.js';

export class WeatherApiFetcher {
   static weatherApiUrl(path) {
      return (
         `https://api.openweathermap.org/data/2.5/${path}`
         + `?lat=${AppConfig.TORONTO_ZOO_COORDINATES.lat}`
         + `&lon=${AppConfig.TORONTO_ZOO_COORDINATES.lon}`
         + `&units=metric`
         + `&appid=${AppConfig.OPEN_WEATHER_API_KEY}`
      );
   }

   static isTodayDate(dateStr) {
      return dateStr === VisitDateRules.toISODate(VisitDateRules.getToday());
   }

   static fetchCurrentTemp() {
      return fetch(WeatherApiFetcher.weatherApiUrl('weather'))
         .then(res => res.json())
         .then(data => {
            const temp = Number(data.main?.temp);
            return Number.isFinite(temp) ? temp : null;
         });
   }

   static fetchForecastDateTemp(dateStr) {
      return fetch(
         WeatherApiFetcher.weatherApiUrl('forecast')
      )
         .then(res => res.json())
         .then(data => {
            const daily = (data.list || []).filter(f => String(f.dt_txt || '').startsWith(dateStr));
            if (daily.length === 0) return null;

            return daily.reduce((sum, f) => sum + Number(f.main?.temp ?? 0), 0) / daily.length;
         });
   }
}
