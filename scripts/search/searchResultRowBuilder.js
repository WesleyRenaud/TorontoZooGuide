import { GuardiansTalkLinkedAnimalOpener } from '../guardians/guardiansTalkLinkedAnimalOpener.js';
import { AnimalSelectorModel } from '../itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { ResultRenderer } from '../itinerary/selectors/base/resultRenderer.js';
import { StoredSelectionNormalizer } from '../itinerary/selectors/base/storedSelectionNormalizer.js';
import { SpeciesFragment } from '../overlays/speciesFragment.js';
import { SearchResultPresenter } from './searchResultPresenter.js';
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
            onTitleClick: SpeciesFragment.openAnimalSpeciesOverlay,
         }),
         attraction: ResultRenderer.createDefaultSelectorRowLeftRenderer({
            getTitle: AttractionSelectorModel.getAttractionTitle,
            getSubtitle: AttractionSelectorModel.getAttractionSubtitle,
            getImageSrc: AttractionSelectorModel.buildAttractionImageSrc,
            getInfoLink: () => null,
            onTitleClick: SearchResultRowBuilder.openAttractionInfoLink,
            shouldEnableTitleClick: (row) => Boolean(AttractionSelectorModel.getAttractionInfoLink(row)),
         }),
         wildEncounter: SearchResultPresenter.createSearchImageRowRenderer({
            presentation: SearchResultPresenter.SEARCH_RESULT_PRESENTATIONS.wildEncounter,
            imageDirectory: 'wild-encounters',
            getInfoLink: () => null,
            onTitleClick: SearchResultRowBuilder.openWildEncounterLink,
         }),
         guardiansTalk: SearchResultPresenter.createSearchImageRowRenderer({
            presentation: SearchResultPresenter.SEARCH_RESULT_PRESENTATIONS.guardiansTalk,
            imageDirectory: 'guardians-talks',
            onTitleClick: GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal,
            shouldEnableTitleClick: (row) => Boolean(GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal(row)),
         }),
         ...SearchResultPresenter.createSearchImageRowRenderers([
            { type: 'restaurant', imageDirectory: 'restaurants', getInfoLink: SearchResultPresenter.getRestaurantMenuLink },
            { type: 'giftShop', imageDirectory: 'gift-shops' },
            { type: 'pavilion', imageDirectory: 'pavilions' },
            { type: 'transportationStation', imageDirectory: 'transportation-stations' },
         ]),
      };

      return SearchResultRowBuilder._rowLeftRenderers;
   }

   static openWildEncounterLink(row) {
      const link = StoredSelectionNormalizer.normalizeStoredLink(row.link);

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
      const presentation = SearchResultPresenter.getSearchResultPresentation(row);
      const title = presentation.getTitle(row) || '';
      const suffix = typeof presentation.getTitleSuffix === 'function'
         ? presentation.getTitleSuffix(row)
         : '';

      return `${title}${suffix}`;
   }

   static getRowSubtitle(row) {
      return SearchResultPresenter.getSearchResultPresentation(row).getSubtitle(row);
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
