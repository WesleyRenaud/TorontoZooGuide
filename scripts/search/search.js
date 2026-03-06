import { ajaxPost } from '../utils/ajax.js';

function debounce(fn, delay = 250) {
   let t = null;
   return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), delay);
   };
}

export function normalizeSearchRows(response) {
   if (!response) return [];
   if (Array.isArray(response)) return response;
   if (Array.isArray(response.results)) return response.results;

   const out = [];
   if (Array.isArray(response.animals)) out.push(...response.animals.map(x => ({ ...x, type: x.type || 'animal' })));
   if (Array.isArray(response.pavilions)) out.push(...response.pavilions.map(x => ({ ...x, type: x.type || 'pavilion' })));
   if (Array.isArray(response.restaurants)) out.push(...response.restaurants.map(x => ({ ...x, type: x.type || 'restaurant' })));
   if (Array.isArray(response.restrooms)) out.push(...response.restrooms.map(x => ({ ...x, type: x.type || 'restroom' })));
   if (Array.isArray(response.gift_shops)) out.push(...response.gift_shops.map(x => ({ ...x, type: x.type || 'giftShop' })));
   if (Array.isArray(response.attractions)) out.push(...response.attractions.map(x => ({ ...x, type: x.type || 'attraction' })));
   if (Array.isArray(response.zoomobile_stations)) out.push(...response.zoomobile_stations.map(x => ({ ...x, type: x.type || 'zoomobileStation' })));
   if (Array.isArray(response.meet_the_guardians_talks)) out.push(...response.meet_the_guardians_talks.map(x => ({ ...x, type: x.type || 'meetTheGuardiansTalk' })));
   if (Array.isArray(response.wild_encounter_meeting_spots)) out.push(...response.wild_encounter_meeting_spots.map(x => ({ ...x, type: x.type || 'wildEncounterMeetingSpot' })));
   return out;
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

   async function run() {
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
         const response = await ajaxPost('/search', {
            query,
            ...flags,
            ...ctx,
         });

         renderSearchResults(target, normalizeSearchRows(response), onFocusRow);
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

function getRowType(row) {
   return String(row.type || row.TYPE || 'animal');
}

function getRowTitle(row, type) {
   if (type === 'wildEncounterMeetingSpot') return row.name ?? row.NAME ?? 'Wild Encounter Meeting Spot';
   if (type === 'meetTheGuardiansTalk') return row.name ?? row.NAME ?? 'Meet The Guardians Talk';
   if (type === 'zoomobileStation') return row.name ?? row.NAME ?? 'Zoomobile Station';
   if (type === 'attraction') return row.name ?? row.NAME ?? 'Attraction';
   if (type === 'giftShop') return row.name ?? row.NAME ?? 'Gift Shop';
   if (type === 'restroom') return row.title ?? row.TITLE ?? 'Restroom';
   if (type === 'restaurant') return row.name ?? row.NAME ?? 'Restaurant';
   if (type === 'pavilion') return row.name ?? row.NAME ?? 'Pavilion';
   return row.SPECIES ?? row.species ?? 'Animal';
}

function getRowSubtitle(row, type) {
   if (type === 'wildEncounterMeetingSpot') return null;

   if (type === 'meetTheGuardiansTalk') {
      return 'Meet The Guardians Talk';
   }

   if (type === 'zoomobileStation') return null;

   if (type === 'attraction') {
      const parts = [];
      parts.push(row.free_with_admission ? 'Free With Admission' : 'Extra Charge');
      return parts.join(', ') || 'Attraction';
   }

   if (type === 'giftShop') {
      const parts = [];
      if (row.location) parts.push(`Location: ${row.location}`);
      if (row.sub_location) parts.push(row.sub_location);
      return parts.join(', ') || 'Gift Shop';
   }

   if (type === 'restroom') return null;

   if (type === 'restaurant') {
      const parts = [];
      if (row.location) parts.push(`Location: ${row.location}`);
      if (row.sub_location) parts.push(row.sub_location);
      return parts.join(', ') || 'Restaurant';
   }

   if (type === 'pavilion') {
      const region = row.region ?? row.REGION;
      return region ? `Region: ${region}` : 'Pavilion';
   }

   const exhibit = row.EXHIBIT ?? row.exhibit;
   return exhibit ? `Exhibit: ${exhibit}` : 'Animal';
}

function renderSearchResults(resultsEl, rows, onFocusRow) {
   resultsEl.innerHTML = '';
   if (!Array.isArray(rows) || rows.length === 0) return;

   rows.forEach(row => {
      const type = getRowType(row);
      const title = getRowTitle(row, type);
      const subtitle = getRowSubtitle(row, type);

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
         onFocusRow?.(row);
      });

      item.appendChild(left);
      item.appendChild(btn);
      resultsEl.appendChild(item);
   });
}