import {
   getGuardiansTalkLinkedAnimal,
   openGuardiansTalkLinkedAnimal,
} from '../guardians/openGuardiansTalkLinkedAnimal.js';
import {
   buildAnimalImageSrc,
   getAnimalEnclosureName,
   getAnimalSpecies,
   getAnimalSubtitle,
   getAnimalTitleLine,
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
import {
   createSearchImageRowRenderer,
   createSearchImageRowRenderers,
   getRestaurantMenuLink,
   getSearchResultPresentation,
   SEARCH_RESULT_PRESENTATIONS,
} from './searchResultPresentation.js';
import { APP_STRINGS } from '../strings.js';

function openWildEncounterLink(row) {
   const link = normalizeStoredLink(row.link);

   if (link) {
      window.open(link, '_blank');
   }
}

const ROW_LEFT_RENDERERS = {
   animal: createDefaultSelectorRowLeftRenderer({
      getTitle: getAnimalTitleLine,
      getTitleParts: (row) => ({
         species: getAnimalSpecies(row),
         enclosureName: getAnimalEnclosureName(row),
      }),
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
   wildEncounter: createSearchImageRowRenderer({
      presentation: SEARCH_RESULT_PRESENTATIONS.wildEncounter,
      imageDirectory: 'wild-encounters',
      getInfoLink: () => null,
      onTitleClick: openWildEncounterLink,
   }),
   guardiansTalk: createSearchImageRowRenderer({
      presentation: SEARCH_RESULT_PRESENTATIONS.guardiansTalk,
      imageDirectory: 'guardians-talks',
      onTitleClick: openGuardiansTalkLinkedAnimal,
      shouldEnableTitleClick: (row) => Boolean(getGuardiansTalkLinkedAnimal(row)),
   }),
   ...createSearchImageRowRenderers([
      { type: 'restaurant', imageDirectory: 'restaurants', getInfoLink: getRestaurantMenuLink },
      { type: 'giftShop', imageDirectory: 'gift-shops' },
      { type: 'pavilion', imageDirectory: 'pavilions' },
      { type: 'zoomobileStation', imageDirectory: 'zoomobile-stations' },
   ]),
};

function getRowTitle(row) {
   return getSearchResultPresentation(row).getTitle(row);
}

function getRowSubtitle(row) {
   return getSearchResultPresentation(row).getSubtitle(row);
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
