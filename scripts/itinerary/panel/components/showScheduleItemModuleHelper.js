export class ShowScheduleItemModuleHelper {
   static SEARCH_DEBOUNCE_MS = 250;

   static debounce(fn, delay = ShowScheduleItemModuleHelper.SEARCH_DEBOUNCE_MS) {
      let timeoutId = null;

      return (...args) => {
         clearTimeout(timeoutId);
         timeoutId = setTimeout(() => fn(...args), delay);
      };
   }
}
