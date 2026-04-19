function buildDetailSummary(parts, fallback) {
   const details = parts.filter(Boolean);

   if (details.length === 0) {
      return fallback;
   }

   return `${fallback}\n${details.join(' | ')}`;
}

function getRowTitle(row) {
   switch (row.type) {
      case 'wildEncounter':
         return row.name || 'Wild Encounter';
      case 'guardiansTalk':
         return row.name || 'Meet The Guardians Talk';
      case 'zoomobileStation':
         return row.name || 'Zoomobile Station';
      case 'attraction':
         return row.name || 'Attraction';
      case 'giftShop':
         return row.name || 'Gift Shop';
      case 'restroom':
         return row.title || 'Restroom';
      case 'restaurant':
         return row.name || 'Restaurant';
      case 'pavilion':
         return row.name || 'Pavilion';
      default:
         return row.species || 'Animal';
   }
}

function getRowSubtitle(row) {
   switch (row.type) {
      case 'wildEncounter':
         return buildDetailSummary(
            [row.meeting_spot, row.time_of_day],
            'Wild Encounter'
         );
      case 'guardiansTalk':
         return buildDetailSummary(
            [row.location, row.time_of_day],
            'Meet The Guardians Talk'
         );
      case 'zoomobileStation':
      case 'restroom':
         return null;
      case 'attraction':
         return row.free_with_admission ? 'Free With Admission' : 'Extra Charge';
      case 'giftShop':
         return [row.location ? `Location: ${row.location}` : null, row.sub_location]
            .filter(Boolean)
            .join(', ') || 'Gift Shop';
      case 'restaurant':
         return [row.location ? `Location: ${row.location}` : null, row.sub_location]
            .filter(Boolean)
            .join(', ') || 'Restaurant';
      case 'pavilion':
         return row.region ? `Region: ${row.region}` : 'Pavilion';
      default:
         return row.exhibit ? `Exhibit: ${row.exhibit}` : 'Animal';
   }
}

function createSearchResultItem(row, onFocusRow) {
   const item = document.createElement('div');
   item.className = 'animal-result';

   const left = document.createElement('div');
   left.className = 'animal-result-left';

   const titleEl = document.createElement('div');
   titleEl.className = 'animal-result-species';
   titleEl.textContent = getRowTitle(row);

   const subtitleEl = document.createElement('div');
   subtitleEl.className = 'animal-result-exhibit';
   subtitleEl.textContent = getRowSubtitle(row);

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

   return item;
}

export function renderSearchResults(resultsEl, rows, onFocusRow) {
   resultsEl.innerHTML = '';

   if (!Array.isArray(rows) || rows.length === 0) {
      return;
   }

   rows.forEach((row) => {
      resultsEl.appendChild(createSearchResultItem(row, onFocusRow));
   });
}
