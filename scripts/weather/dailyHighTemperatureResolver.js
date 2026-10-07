import { WeatherClient } from '../api/weatherClient.js';
import { VisitDateValidator } from '../visitDates/visitDateValidator.js';

export class DailyHighTemperatureResolver {
   static isTodayDate(dateStr) {
      return dateStr === VisitDateValidator.toISODate(VisitDateValidator.getToday());
   }

   static toLocalISODate(unixSeconds, timezoneOffsetSeconds) {
      return new Date((unixSeconds + timezoneOffsetSeconds) * 1000).toISOString().slice(0, 10);
   }

   static getForecastHigh(forecast, dateStr) {
      const temps = forecast.slots
         .filter(slot => (
            DailyHighTemperatureResolver.toLocalISODate(slot.unixSeconds, forecast.timezoneOffsetSeconds) === dateStr
         ))
         .map(slot => slot.tempMax);

      return temps.length ? Math.max(...temps) : null;
   }

   static getTodayHigh(currentTemp, forecastHigh) {
      return forecastHigh === null ? currentTemp : Math.max(currentTemp, forecastHigh);
   }

   static async resolve(dateStr) {
      if (!DailyHighTemperatureResolver.isTodayDate(dateStr)) {
         return DailyHighTemperatureResolver.getForecastHigh(await WeatherClient.getForecast(), dateStr);
      }

      const [currentTemp, forecast] = await Promise.all([
         WeatherClient.getCurrentTemp(),
         WeatherClient.getForecast(),
      ]);

      return DailyHighTemperatureResolver.getTodayHigh(
         currentTemp,
         DailyHighTemperatureResolver.getForecastHigh(forecast, dateStr)
      );
   }
}
