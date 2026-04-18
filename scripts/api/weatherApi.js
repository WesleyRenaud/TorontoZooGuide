import { CONFIG } from '../config/appConfig.js';

export function fetchForecastTemp(dateStr) {
   return fetch(
      `https://api.openweathermap.org/data/2.5/forecast?lat=${CONFIG.lat}&lon=${CONFIG.lon}&units=metric&appid=${CONFIG.apiKey}`
   )
      .then(res => res.json())
      .then(data => {
         const daily = (data.list || []).filter(f => String(f.dt_txt || '').startsWith(dateStr));
         if (daily.length === 0) return null;

         return daily.reduce((sum, f) => sum + Number(f.main?.temp ?? 0), 0) / daily.length;
      });
}
