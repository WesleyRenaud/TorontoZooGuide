import { OpenGuardiansTalkLinkedAnimal } from '../guardians/openGuardiansTalkLinkedAnimal.js';
import { AnimalSelectorModel } from '../itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { ResultRenderer } from '../itinerary/selectors/base/resultRenderer.js';
import { StoredSelection } from '../itinerary/selectors/base/storedSelection.js';
import { SpeciesOverlay } from '../overlays/speciesOverlay.js';
import { SearchResultPresentation } from './searchResultPresentation.js';
import { Strings } from '../strings.js';

export class SearchResultRowBuilder {
   static getRowLeftRenderers() {
      if (SearchResultRowBuilder._rowLeftRenderers) {
         return SearchResultRowBuilder._rowLeftRenderers;
      }

      SearchResultRowBuilder._rowLeftRenderers = {
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
            onTitleClick: SearchResultRowBuilder.openAttractionInfoLink,
            shouldEnableTitleClick: (row) => Boolean(AttractionSelectorModel.getAttractionInfoLink(row)),
         }),
         wildEncounter: SearchResultPresentation.createSearchImageRowRenderer({
            presentation: SearchResultPresentation.SEARCH_RESULT_PRESENTATIONS.wildEncounter,
            imageDirectory: 'wild-encounters',
            getInfoLink: () => null,
            onTitleClick: SearchResultRowBuilder.openWildEncounterLink,
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

      return SearchResultRowBuilder._rowLeftRenderers;
   }

   static openWildEncounterLink(row) {
      const link = StoredSelection.normalizeStoredLink(row.link);

      if (link) {
         window.open(link, '_blank');
      }
   }

   static openAttractionInfoLink(row) {
      const link = AttractionSelectorModel.getAttractionInfoLink(row);

      if (link) {
         window.open(link, '_blank');
      }
   }

   static getRowTitle(row) {
      const presentation = SearchResultPresentation.getSearchResultPresentation(row);
      const title = presentation.getTitle(row) || '';
      const suffix = typeof presentation.getTitleSuffix === 'function'
         ? presentation.getTitleSuffix(row)
         : '';

      return `${title}${suffix}`;
   }

   static getRowSubtitle(row) {
      return SearchResultPresentation.getSearchResultPresentation(row).getSubtitle(row);
   }

   static createTextElement(className, text) {
      const element = document.createElement('div');
      element.className = className;
      element.textContent = text;

      return element;
   }

   static createResultText(row) {
      const left = document.createElement('div');
      left.className = 'animal-result-left';

      left.appendChild(
         SearchResultRowBuilder.createTextElement('animal-result-species', SearchResultRowBuilder.getRowTitle(row))
      );

      const subtitle = SearchResultRowBuilder.getRowSubtitle(row);

      if (subtitle) {
         left.appendChild(
            SearchResultRowBuilder.createTextElement('animal-result-exhibit', subtitle)
         );
      }

      return left;
   }

   static createResultContent(row) {
      const renderWithImage = SearchResultRowBuilder.getRowLeftRenderers()[row.type];

      if (renderWithImage) {
         return renderWithImage(row);
      }

      return SearchResultRowBuilder.createResultText(row);
   }

   static createFocusButton(row, onFocusRow) {
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

   static createSearchResultItem(row, onFocusRow) {
      const item = document.createElement('div');
      item.className = 'animal-result';

      item.append(
         SearchResultRowBuilder.createResultContent(row),
         SearchResultRowBuilder.createFocusButton(row, onFocusRow)
      );

      return item;
   }

   static createSearchResultsFragment(rows, onFocusRow) {
      const fragment = document.createDocumentFragment();

      rows.forEach((row) => {
         fragment.appendChild(SearchResultRowBuilder.createSearchResultItem(row, onFocusRow));
      });

      return fragment;
   }
}
