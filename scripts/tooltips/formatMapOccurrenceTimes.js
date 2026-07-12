export function formatMapOccurrenceTimes(item = {}) {
   const times = Array.isArray(item.times)
      ? item.times.filter(Boolean)
      : [];

   if (times.length > 0) {
      return times.join(', ');
   }

   return item.start_time || '';
}
