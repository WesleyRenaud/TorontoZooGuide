import { SearchResultRowBuilder } from './searchResultRowBuilder.js';

export class SearchResultsRenderer {
   static renderSearchResults(resultsEl, rows, onFocusRow) {
      if (!Array.isArray(rows) || rows.length === 0) {
         resultsEl.replaceChildren();
         return;
      }

      resultsEl.replaceChildren(SearchResultRowBuilder.createSearchResultsFragment(rows, onFocusRow));
   }
}
