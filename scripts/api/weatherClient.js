import { WeatherApiFetcher } from './weatherApiFetcher.js';

export class WeatherClient {
   static getCurrentTemp() {
      return WeatherApiFetcher.fetchJson('weather').then(data => data.main.temp);
   }

   static getForecast() {
      return WeatherApiFetcher.fetchJson('forecast').then(data => ({
         timezoneOffsetSeconds: data.city.timezone,
         slots: data.list.map(slot => ({
            unixSeconds: slot.dt,
            tempMax: slot.main.temp_max,
         })),
      }));
   }
}
