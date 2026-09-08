import { SearchApi } from '../api/searchApi.js';
import { ValueNormalizer } from '../api/valueNormalizer.js';
import { SearchResultsRenderer } from './searchResultsRenderer.js';
import { SearchRows } from './searchRows.js';

export class SearchQueryRunner {
   static DEFAULT_DEBOUNCE_MS = 250;

   static createNoopSearch() {
      return { refresh: () => {} };
   }

   static debounce(fn, delay = SearchQueryRunner.DEFAULT_DEBOUNCE_MS) {
      let timeoutId = null;

      return (...args) => {
         clearTimeout(timeoutId);
         timeoutId = setTimeout(() => fn(...args), delay);
      };
   }

   static getSearchQuery(inputEl) {
      return ValueNormalizer.asTrimmedString(inputEl.value);
   }

   static shouldClearForEmptyQuery(query, allowEmptyQuery) {
      return !query && !allowEmptyQuery;
   }

   static clearSearchResults(resultsEl) {
      resultsEl.replaceChildren();
   }

   static createRequestTracker() {
      let latestRequestId = 0;

      return {
         nextRequestId: () => {
            latestRequestId += 1;
            return latestRequestId;
         },
         isCurrentRequest: (requestId) => requestId === latestRequestId,
      };
   }

   static logSearchError(error) {
      console.warn('[search] failed to fetch results:', error);
   }

   static async buildSearchRequest({
      query,
      getIncludeFlags,
      getContext,
   } = {}) {
      return {
         query,
         ...(getIncludeFlags?.() ?? {}),
         ...((await getContext?.()) ?? {}),
      };
   }

   static createSearchRunner({
      inputEl,
      resultsEl,
      getIncludeFlags,
      getContext,
      onFocusRow,
      allowEmptyQuery,
      onError,
   } = {}) {
      const requestTracker = SearchQueryRunner.createRequestTracker();

      return async function runSearch() {
         const requestId = requestTracker.nextRequestId();
         const query = SearchQueryRunner.getSearchQuery(inputEl);

         if (SearchQueryRunner.shouldClearForEmptyQuery(query, allowEmptyQuery)) {
            SearchQueryRunner.clearSearchResults(resultsEl);
            return;
         }

         try {
            const response = await SearchApi.searchZoo(
               await SearchQueryRunner.buildSearchRequest({
                  query,
                  getIncludeFlags,
                  getContext,
               })
            );

            if (!requestTracker.isCurrentRequest(requestId)) {
               return;
            }

            SearchResultsRenderer.renderSearchResults(resultsEl, SearchRows.flattenSearchRows(response), onFocusRow);
         } catch (error) {
            if (requestTracker.isCurrentRequest(requestId)) {
               onError(error);
            }
         }
      };
   }
}
