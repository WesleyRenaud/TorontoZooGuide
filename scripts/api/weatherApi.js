import { WeatherApiFetcher } from './weatherApiFetcher.js';

export class WeatherApi {
   static fetchWeatherTempForDate(dateStr) {
      if (WeatherApiFetcher.isTodayDate(dateStr)) {
         return WeatherApiFetcher.fetchCurrentTemp();
      }

      return WeatherApiFetcher.fetchForecastDateTemp(dateStr);
   }
}
