import { SearchClient } from '../../api/searchClient.js';
import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { SelectorSearchRunnerHelper } from './selectorSearchRunnerHelper.js';

export class SelectorSearchRunner {
   static SELECTOR_SEARCH_DEBOUNCE_MS = 250;

   static debounce(fn, delay = SelectorSearchRunner.SELECTOR_SEARCH_DEBOUNCE_MS) {
      return SelectorSearchRunnerHelper.debounce(fn, delay);
   }

   static createSelectorSearchRunner({
      searchEndpoint,
      buildSearchPayload,
      extractRows,
      getContext,
      getQuery,
      onRows,
      searchItems = SearchClient.searchItineraryItems,
      debounceMs = SelectorSearchRunner.SELECTOR_SEARCH_DEBOUNCE_MS,
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
         const query = ValueNormalizer.asTrimmedString(getQuery?.());

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

      const scheduleCurrentQuery = SelectorSearchRunner.debounce(() => {
         void runCurrentQuery();
      }, debounceMs);

      return {
         runCurrentQuery,
         scheduleCurrentQuery,
      };
   }
}
