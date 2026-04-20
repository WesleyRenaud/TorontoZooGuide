import { searchZoo } from '../api/searchApi.js';
import { renderSearchResults } from './resultsView.js';
import { flattenSearchRows } from './searchRows.js';

function debounce(fn, delay = 250) {
   let t = null;
   return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), delay);
   };
}

export function initSearch({
   inputEl,
   getIncludeFlags,
   getContext,
   onFocusRow,
   resultsEl = null,
   allowEmptyQuery = false,
} = {}) {
   if (!inputEl) {
      return { refresh: () => {} };
   }

   let latestRequestId = 0;

   async function run() {
      const requestId = ++latestRequestId;
      const query = (inputEl.value || '').trim();

      const target = resultsEl || document.getElementById('animalSearchResults');
      if (!target) return;

      if (!query && !allowEmptyQuery) {
         target.innerHTML = '';
         return;
      }

      const flags = getIncludeFlags?.() ?? {};
      const ctx = (await getContext?.()) ?? {};

      try {
         const response = await searchZoo({
            query,
            ...flags,
            ...ctx,
         });

         if (requestId !== latestRequestId) {
            return;
         }

         renderSearchResults(target, flattenSearchRows(response), onFocusRow);
      } catch {
         // ignore
      }
   }

   const onChange = debounce(run, 250);
   inputEl.addEventListener('input', onChange);

   function refresh() {
      run();
   }

   return { refresh };
}
