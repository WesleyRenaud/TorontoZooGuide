import { AppConfig } from '../config/appConfig.js';

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

   static fetchJson(path) {
      return fetch(WeatherApiFetcher.weatherApiUrl(path)).then(res => res.json());
   }
}
