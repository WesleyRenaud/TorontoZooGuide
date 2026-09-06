import { OpenGuardiansTalkLinkedAnimal } from '../guardians/openGuardiansTalkLinkedAnimal.js';
import { AnimalSelectorModel } from '../itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { ResultRenderer } from '../itinerary/selectors/base/resultRenderer.js';
import { StoredSelection } from '../itinerary/selectors/base/storedSelection.js';
import { SpeciesOverlay } from '../overlays/speciesOverlay.js';
import { SearchResultPresentation } from './searchResultPresentation.js';
import { Strings } from '../strings.js';

function openWildEncounterLink(row) {
   const link = StoredSelection.normalizeStoredLink(row.link);

   if (link) {
      window.open(link, '_blank');
   }
}

function openAttractionInfoLink(row) {
   const link = AttractionSelectorModel.getAttractionInfoLink(row);

   if (link) {
      window.open(link, '_blank');
   }
}

const ROW_LEFT_RENDERERS = {
   animal: ResultRenderer.createDefaultSelectorRowLeftRenderer({
      getTitle: AnimalSelectorModel.getAnimalTitleLine,
      getTitleParts: (row) => ({
         species: AnimalSelectorModel.getAnimalSpecies(row),
         enclosureName: AnimalSelectorModel.getAnimalEnclosureName(row),
      }),
      getSubtitle: AnimalSelectorModel.getAnimalSubtitle,
      getImageSrc: AnimalSelectorModel.buildAnimalImageSrc,
      getInfoLink: () => null,
      onTitleClick: SpeciesOverlay.openAnimalSpeciesOverlay,
   }),
   attraction: ResultRenderer.createDefaultSelectorRowLeftRenderer({
      getTitle: AttractionSelectorModel.getAttractionTitle,
      getSubtitle: AttractionSelectorModel.getAttractionSubtitle,
      getImageSrc: AttractionSelectorModel.buildAttractionImageSrc,
      getInfoLink: () => null,
      onTitleClick: openAttractionInfoLink,
      shouldEnableTitleClick: (row) => Boolean(AttractionSelectorModel.getAttractionInfoLink(row)),
   }),
   wildEncounter: SearchResultPresentation.createSearchImageRowRenderer({
      presentation: SearchResultPresentation.SEARCH_RESULT_PRESENTATIONS.wildEncounter,
      imageDirectory: 'wild-encounters',
      getInfoLink: () => null,
      onTitleClick: openWildEncounterLink,
   }),
   guardiansTalk: SearchResultPresentation.createSearchImageRowRenderer({
      presentation: SearchResultPresentation.SEARCH_RESULT_PRESENTATIONS.guardiansTalk,
      imageDirectory: 'guardians-talks',
      onTitleClick: OpenGuardiansTalkLinkedAnimal.openGuardiansTalkLinkedAnimal,
      shouldEnableTitleClick: (row) => Boolean(OpenGuardiansTalkLinkedAnimal.getGuardiansTalkLinkedAnimal(row)),
   }),
   ...SearchResultPresentation.createSearchImageRowRenderers([
      { type: 'restaurant', imageDirectory: 'restaurants', getInfoLink: SearchResultPresentation.getRestaurantMenuLink },
      { type: 'giftShop', imageDirectory: 'gift-shops' },
      { type: 'pavilion', imageDirectory: 'pavilions' },
      { type: 'transportationStation', imageDirectory: 'transportation-stations' },
   ]),
};

function getRowTitle(row) {
   const presentation = SearchResultPresentation.getSearchResultPresentation(row);
   const title = presentation.getTitle(row) || '';
   const suffix = typeof presentation.getTitleSuffix === 'function'
      ? presentation.getTitleSuffix(row)
      : '';

   return `${title}${suffix}`;
}

function getRowSubtitle(row) {
   return SearchResultPresentation.getSearchResultPresentation(row).getSubtitle(row);
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
   button.textContent = Strings.common.viewOnMap;

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

export class ResultsView {
   static renderSearchResults(resultsEl, rows, onFocusRow) {
      if (!Array.isArray(rows) || rows.length === 0) {
         resultsEl.replaceChildren();
         return;
      }

      resultsEl.replaceChildren(createSearchResultsFragment(rows, onFocusRow));
   }
}
