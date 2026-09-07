import { SearchQueryRunner } from './searchQueryRunner.js';

export class Search {
   static initSearch({
      inputEl,
      getIncludeFlags,
      getContext,
      onFocusRow,
      resultsEl = null,
      allowEmptyQuery = false,
      onError = SearchQueryRunner.logSearchError,
   } = {}) {
      if (!inputEl || !resultsEl) {
         return SearchQueryRunner.createNoopSearch();
      }

      const run = SearchQueryRunner.createSearchRunner({
         inputEl,
         resultsEl,
         getIncludeFlags,
         getContext,
         onFocusRow,
         allowEmptyQuery,
         onError,
      });

      const onChange = SearchQueryRunner.debounce(run);
      inputEl.addEventListener('input', onChange);

      return {
         refresh: () => {
            run();
         },
      };
   }
}
