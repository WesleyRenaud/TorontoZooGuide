import { SearchApi } from '../../api/searchApi.js';

export const SELECTOR_SEARCH_DEBOUNCE_MS = 250;

export function debounce(fn, delay = SELECTOR_SEARCH_DEBOUNCE_MS) {
   let timeoutId = null;

   return (...args) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => fn(...args), delay);
   };
}

export function createSelectorSearchRunner({
   searchEndpoint,
   buildSearchPayload,
   extractRows,
   getContext,
   getQuery,
   onRows,
   searchItems = SearchApi.searchItineraryItems,
   debounceMs = SELECTOR_SEARCH_DEBOUNCE_MS,
} = {}) {
   let latestSearchRequestId = 0;

   async function fetchRows(query) {
      const context = typeof getContext === 'function'
         ? await getContext()
         : {};

      const response = await searchItems(searchEndpoint, {
         ...buildSearchPayload(query),
         ...context,
      });

      return extractRows(response);
   }

   async function runCurrentQuery() {
      const requestId = ++latestSearchRequestId;
      const query = getQuery()?.trim() ?? '';

      try {
         const rows = await fetchRows(query);

         if (requestId !== latestSearchRequestId) {
            return;
         }

         onRows(rows);
      }
      catch {
         if (requestId !== latestSearchRequestId) {
            return;
         }

         onRows([]);
      }
   }

   const scheduleCurrentQuery = debounce(() => {
      void runCurrentQuery();
   }, debounceMs);

   return {
      runCurrentQuery,
      scheduleCurrentQuery,
   };
}
