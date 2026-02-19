import { ajaxPost } from '../utils/ajax.js';
import { getPavilionName } from '../utils/dom.js';

function debounce(fn, delay = 250) {
   let t = null;
   return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), delay);
   };
}

function normalizeSearchRows(response) {
   if (!response) return [];
   if (Array.isArray(response)) return response;
   if (Array.isArray(response.results)) return response.results;

   const out = [];
   if (Array.isArray(response.animals)) out.push(...response.animals.map(x => ({ ...x, type: x.type || 'animal' })));
   if (Array.isArray(response.pavilions)) out.push(...response.pavilions.map(x => ({ ...x, type: x.type || 'pavilion' })));
   return out;
}

export function initSearch({ inputEl, getIncludeFlags, onFocusRow }) {
   if (!inputEl) {
      return { refresh: () => {} };
   }

   async function run() {
      const query = (inputEl.value || '').trim();
      const resultsEl = document.getElementById('animalSearchResults');
      if (!resultsEl) return;

      if (!query) {
         resultsEl.innerHTML = '';
         return;
      }

      const flags = getIncludeFlags?.() ?? {};

      try {
         const response = await ajaxPost('/search', { query, ...flags });
         renderSearchResults(resultsEl, normalizeSearchRows(response), onFocusRow);
      } catch {
         // ignore
      }
   }

   const onChange = debounce(run, 250);
   inputEl.addEventListener('input', onChange);

   // ✅ allow other parts of the app to re-run search when filters change
   function refresh() {
      run();
   }

   return { refresh };
}

function renderSearchResults(resultsEl, rows, onFocusRow) {
   resultsEl.innerHTML = '';
   if (!Array.isArray(rows) || rows.length === 0) return;

   rows.forEach(row => {
      const type = String(row.type || row.TYPE || 'animal').toLowerCase();

      const title = type === 'pavilion'
         ? (getPavilionName(row) || 'Pavilion')
         : (row.SPECIES ?? row.species ?? 'Animal');

      const subtitle = type === 'pavilion'
         ? ((row.region ?? row.REGION) ? `Region: ${row.region ?? row.REGION}` : 'Pavilion')
         : ((row.EXHIBIT ?? row.exhibit) ? `Exhibit: ${row.EXHIBIT ?? row.exhibit}` : 'Animal');

      const item = document.createElement('div');
      item.className = 'animal-result';

      const left = document.createElement('div');
      left.className = 'animal-result-left';

      const titleEl = document.createElement('div');
      titleEl.className = 'animal-result-species';
      titleEl.textContent = title;

      const subtitleEl = document.createElement('div');
      subtitleEl.className = 'animal-result-exhibit';
      subtitleEl.textContent = subtitle;

      left.appendChild(titleEl);
      left.appendChild(subtitleEl);

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'animal-result-map-btn';
      btn.textContent = 'View on Map';

      btn.addEventListener('click', (e) => {
         e.stopPropagation();

         try {
            onFocusRow?.(row);
         } catch (err) {
            console.error('[search] Error inside onFocusRow:', err);
         }
      });

      item.appendChild(left);
      item.appendChild(btn);
      resultsEl.appendChild(item);
   });
}