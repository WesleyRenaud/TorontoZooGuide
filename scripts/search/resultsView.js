import { APP_STRINGS } from '../strings.js';

function buildDetailSummary(parts, fallback) {
   const details = parts.filter(Boolean);

   if (details.length === 0) {
      return fallback;
   }

   return `${fallback}\n${details.join(' | ')}`;
}

function buildLocationSummary(row, fallback) {
   return [
      row.location ? APP_STRINGS.search.location(row.location) : null,
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
   getTitle: (row) => row.species || APP_STRINGS.entityLabels.animal,
   getSubtitle: (row) => row.exhibit
      ? `${APP_STRINGS.entityLabels.exhibit}: ${row.exhibit}`
      : APP_STRINGS.entityLabels.animal,
};

const RESULT_PRESENTATIONS = {
   wildEncounter: buildNamedResultPresentation(
      APP_STRINGS.entityLabels.wildEncounter,
      (row) => buildDetailSummary(
         [row.meeting_spot, row.start_time],
         APP_STRINGS.entityLabels.wildEncounter
      )
   ),
   guardiansTalk: buildNamedResultPresentation(
      APP_STRINGS.entityLabels.guardiansTalk,
      (row) => buildDetailSummary(
         [row.location, row.start_time],
         APP_STRINGS.entityLabels.guardiansTalk
      )
   ),
   zoomobileStation: buildNamedResultPresentation(
      APP_STRINGS.entityLabels.zoomobileStation,
      () => null
   ),
   attraction: buildNamedResultPresentation(
      APP_STRINGS.entityLabels.attraction,
      (row) => row.free_with_admission
         ? APP_STRINGS.search.freeWithAdmission
         : APP_STRINGS.search.extraCharge
   ),
   giftShop: buildNamedResultPresentation(
      APP_STRINGS.entityLabels.giftShop,
      (row) => buildLocationSummary(row, APP_STRINGS.entityLabels.giftShop)
   ),
   restroom: {
      getTitle: (row) => row.title || APP_STRINGS.entityLabels.restroom,
      getSubtitle: () => null,
   },
   restaurant: buildNamedResultPresentation(
      APP_STRINGS.entityLabels.restaurant,
      (row) => buildLocationSummary(row, APP_STRINGS.entityLabels.restaurant)
   ),
   pavilion: buildNamedResultPresentation(
      APP_STRINGS.entityLabels.pavilion,
      (row) => row.region
         ? APP_STRINGS.search.region(row.region)
         : APP_STRINGS.entityLabels.pavilion
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
   button.textContent = APP_STRINGS.common.viewOnMap;

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
