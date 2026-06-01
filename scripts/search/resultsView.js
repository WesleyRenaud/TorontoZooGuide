import { normalizeAssetKey } from '../assets/normalizeAssetKey.js';
import {
   buildAnimalImageSrc,
   getAnimalSpecies,
   getAnimalSubtitle,
} from '../itinerary/selectors/animalSelector/model.js';
import {
   buildAttractionImageSrc,
   getAttractionInfoLink,
   getAttractionSubtitle,
   getAttractionTitle,
} from '../itinerary/selectors/attractionSelector/model.js';
import { createDefaultSelectorRowLeftRenderer } from '../itinerary/selectors/base/resultRenderer.js';
import { normalizeStoredLink } from '../itinerary/selectors/base/storedSelection.js';
import { openAnimalSpeciesOverlay } from '../overlays/speciesOverlay.js';
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

function getWildEncounterTitle(row) {
   return String(row.name).trim() || APP_STRINGS.entityLabels.wildEncounter;
}

function getWildEncounterSubtitle(row) {
   return buildDetailSummary(
      [row.meeting_spot, row.start_time],
      APP_STRINGS.entityLabels.wildEncounter
   );
}

function buildWildEncounterImageSrc(row) {
   const normalizedName = normalizeAssetKey(getWildEncounterTitle(row));

   if (!normalizedName) {
      return null;
   }

   return `../images/details/wild-encounters/${normalizedName}.png`;
}

function openWildEncounterLink(row) {
   const link = normalizeStoredLink(row.link);

   if (link) {
      window.open(link, '_blank');
   }
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

const ROW_LEFT_RENDERERS = {
   animal: createDefaultSelectorRowLeftRenderer({
      getTitle: getAnimalSpecies,
      getSubtitle: getAnimalSubtitle,
      getImageSrc: buildAnimalImageSrc,
      getInfoLink: () => null,
      onTitleClick: openAnimalSpeciesOverlay,
   }),
   attraction: createDefaultSelectorRowLeftRenderer({
      getTitle: getAttractionTitle,
      getSubtitle: getAttractionSubtitle,
      getImageSrc: buildAttractionImageSrc,
      getInfoLink: getAttractionInfoLink,
   }),
   wildEncounter: createDefaultSelectorRowLeftRenderer({
      getTitle: getWildEncounterTitle,
      getSubtitle: getWildEncounterSubtitle,
      getImageSrc: buildWildEncounterImageSrc,
      getInfoLink: () => null,
      onTitleClick: openWildEncounterLink,
   }),
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

function createResultContent(row) {
   const renderWithImage = ROW_LEFT_RENDERERS[row.type];

   if (renderWithImage) {
      return renderWithImage(row);
   }

   return createResultText(row);
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
      createResultContent(row),
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
