import { SearchApi } from '../api/searchApi.js';
import { ResultsView } from './resultsView.js';
import { SearchRows } from './searchRows.js';

const DEFAULT_DEBOUNCE_MS = 250;

function createNoopSearch() {
   return { refresh: () => {} };
}

function debounce(fn, delay = DEFAULT_DEBOUNCE_MS) {
   let timeoutId = null;

   return (...args) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => fn(...args), delay);
   };
}

function getSearchQuery(inputEl) {
   return (inputEl.value || '').trim();
}

function shouldClearForEmptyQuery(query, allowEmptyQuery) {
   return !query && !allowEmptyQuery;
}

function clearSearchResults(resultsEl) {
   resultsEl.replaceChildren();
}

function createRequestTracker() {
   let latestRequestId = 0;

   return {
      nextRequestId: () => {
         latestRequestId += 1;
         return latestRequestId;
      },
      isCurrentRequest: (requestId) => requestId === latestRequestId,
   };
}

async function buildSearchRequest({
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

function logSearchError(error) {
   console.warn('[search] failed to fetch results:', error);
}

function createSearchRunner({
   inputEl,
   resultsEl,
   getIncludeFlags,
   getContext,
   onFocusRow,
   allowEmptyQuery,
   onError,
} = {}) {
   const requestTracker = createRequestTracker();

   return async function runSearch() {
      const requestId = requestTracker.nextRequestId();
      const query = getSearchQuery(inputEl);

      if (shouldClearForEmptyQuery(query, allowEmptyQuery)) {
         clearSearchResults(resultsEl);
         return;
      }

      try {
         const response = await SearchApi.searchZoo(
            await buildSearchRequest({
               query,
               getIncludeFlags,
               getContext,
            })
         );

         if (!requestTracker.isCurrentRequest(requestId)) {
            return;
         }

         ResultsView.renderSearchResults(resultsEl, SearchRows.flattenSearchRows(response), onFocusRow);
      } catch (error) {
         if (requestTracker.isCurrentRequest(requestId)) {
            onError(error);
         }
      }
   };
}

export class Search {
   static initSearch({
      inputEl,
      getIncludeFlags,
      getContext,
      onFocusRow,
      resultsEl = null,
      allowEmptyQuery = false,
      onError = logSearchError,
   } = {}) {
      if (!inputEl || !resultsEl) {
         return createNoopSearch();
      }

      const run = createSearchRunner({
         inputEl,
         resultsEl,
         getIncludeFlags,
         getContext,
         onFocusRow,
         allowEmptyQuery,
         onError,
      });

      const onChange = debounce(run);
      inputEl.addEventListener('input', onChange);

      function refresh() {
         run();
      }

      return { refresh };
   }
}
