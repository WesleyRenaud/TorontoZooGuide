import { WeatherApiFetcher } from './weatherApiFetcher.js';

export class WeatherClient {
   static fetchWeatherTempForDate(dateStr) {
      if (WeatherApiFetcher.isTodayDate(dateStr)) {
         return WeatherApiFetcher.fetchCurrentTemp();
      }

      return WeatherApiFetcher.fetchForecastDateTemp(dateStr);
   }
}
