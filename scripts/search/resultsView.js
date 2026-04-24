function buildDetailSummary(parts, fallback) {
   const details = parts.filter(Boolean);

   if (details.length === 0) {
      return fallback;
   }

   return `${fallback}\n${details.join(' | ')}`;
}

function buildLocationSummary(row, fallback) {
   return [
      row.location ? `Location: ${row.location}` : null,
      row.sub_location,
   ]
      .filter(Boolean)
      .join(', ') || fallback;
}

function buildNamedResultPresentation(fallbackTitle, getSubtitle) {
   return {
      getTitle: (row) => row.name || fallbackTitle,
      getSubtitle,
   };
}

const DEFAULT_RESULT_PRESENTATION = {
   getTitle: (row) => row.species || 'Animal',
   getSubtitle: (row) => row.exhibit ? `Exhibit: ${row.exhibit}` : 'Animal',
};

const RESULT_PRESENTATIONS = {
   wildEncounter: buildNamedResultPresentation(
      'Wild Encounter',
      (row) => buildDetailSummary([row.meeting_spot, row.time_of_day], 'Wild Encounter')
   ),
   guardiansTalk: buildNamedResultPresentation(
      'Meet The Guardians Talk',
      (row) => buildDetailSummary([row.location, row.time_of_day], 'Meet The Guardians Talk')
   ),
   zoomobileStation: buildNamedResultPresentation(
      'Zoomobile Station',
      () => null
   ),
   attraction: buildNamedResultPresentation(
      'Attraction',
      (row) => row.free_with_admission ? 'Free With Admission' : 'Extra Charge'
   ),
   giftShop: buildNamedResultPresentation(
      'Gift Shop',
      (row) => buildLocationSummary(row, 'Gift Shop')
   ),
   restroom: {
      getTitle: (row) => row.title || 'Restroom',
      getSubtitle: () => null,
   },
   restaurant: buildNamedResultPresentation(
      'Restaurant',
      (row) => buildLocationSummary(row, 'Restaurant')
   ),
   pavilion: buildNamedResultPresentation(
      'Pavilion',
      (row) => row.region ? `Region: ${row.region}` : 'Pavilion'
   ),
};

function getRowPresentation(row) {
   return RESULT_PRESENTATIONS[row.type] ?? DEFAULT_RESULT_PRESENTATION;
}

function getRowTitle(row) {
   return getRowPresentation(row).getTitle(row);
}

function getRowSubtitle(row) {
   return getRowPresentation(row).getSubtitle(row);
}

function createTextElement(className, text) {
   const element = document.createElement('div');
   element.className = className;
   element.textContent = text;

   return element;
}

function createResultText(row) {
   const left = document.createElement('div');
   left.className = 'animal-result-left';

   left.appendChild(
      createTextElement('animal-result-species', getRowTitle(row))
   );

   const subtitle = getRowSubtitle(row);

   if (subtitle) {
      left.appendChild(
         createTextElement('animal-result-exhibit', subtitle)
      );
   }

   return left;
}

function createFocusButton(row, onFocusRow) {
   const button = document.createElement('button');
   button.type = 'button';
   button.className = 'animal-result-map-btn';
   button.textContent = 'View on Map';

   button.addEventListener('click', (event) => {
      event.stopPropagation();
      onFocusRow?.(row);
   });

   return button;
}

function createSearchResultItem(row, onFocusRow) {
   const item = document.createElement('div');
   item.className = 'animal-result';

   item.append(
      createResultText(row),
      createFocusButton(row, onFocusRow)
   );

   return item;
}

function createSearchResultsFragment(rows, onFocusRow) {
   const fragment = document.createDocumentFragment();

   rows.forEach((row) => {
      fragment.appendChild(createSearchResultItem(row, onFocusRow));
   });

   return fragment;
}

export function renderSearchResults(resultsEl, rows, onFocusRow) {
   if (!Array.isArray(rows) || rows.length === 0) {
      resultsEl.replaceChildren();
      return;
   }

   resultsEl.replaceChildren(createSearchResultsFragment(rows, onFocusRow));
}
