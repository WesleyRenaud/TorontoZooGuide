import { DetailImageBuilder } from '../assets/detailImageBuilder.js';
import { AnimalSelectorModel } from '../itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { ResultRenderer } from '../itinerary/selectors/base/resultRenderer.js';
import { StoredSelectionNormalizer } from '../itinerary/selectors/base/storedSelectionNormalizer.js';
import { GuardiansTalkSelectorModel } from '../itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { WildEncounterSelectorModel } from '../itinerary/selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { SearchResultPresentationHelper } from './searchResultPresentationHelper.js';
import { Strings } from '../strings.js';

export class SearchResultPresenter {
   static SEARCH_DETAIL_IMAGE_BASE_PATH = '../images/details';

   static DEFAULT_SEARCH_RESULT_PRESENTATION = {
      getTitle: AnimalSelectorModel.getAnimalTitleLine,
      getSubtitle: AnimalSelectorModel.getAnimalSubtitle,
   };

   static buildSearchDetailImageSrc(imageDirectory, name) {
      return DetailImageBuilder.buildDetailImageSrc(imageDirectory, name, {
         basePath: SearchResultPresenter.SEARCH_DETAIL_IMAGE_BASE_PATH,
      });
   }

   static buildDetailSummary(parts, fallback) {
      const details = parts.filter(Boolean);

      if (details.length === 0) {
         return fallback;
      }

      return `${fallback}\n${details.join(' | ')}`;
   }

   static buildLocationSummary(row, fallback) {
      return [
         row.location ? Strings.search.location(row.location) : null,
         row.sub_location,
      ]
         .filter(Boolean)
         .join(', ') || fallback;
   }

   static SEARCH_RESULT_PRESENTATIONS = {
      wildEncounter: {
         getTitle: WildEncounterSelectorModel.getWildEncounterName,
         getTitleSuffix: WildEncounterSelectorModel.getWildEncounterTitleSuffix,
         getImageName: WildEncounterSelectorModel.getWildEncounterName,
         getSubtitle: WildEncounterSelectorModel.getWildEncounterSubtitle,
      },
      guardiansTalk: {
         getTitle: GuardiansTalkSelectorModel.getGuardiansTalkName,
         getTitleSuffix: GuardiansTalkSelectorModel.getGuardiansTalkTitleSuffix,
         getImageName: GuardiansTalkSelectorModel.getGuardiansTalkName,
         getSubtitle: GuardiansTalkSelectorModel.getGuardiansTalkSubtitle,
      },
      transportationStation: SearchResultPresentationHelper.buildNamedResultPresentation(
         Strings.entityLabels.transportationStation,
         () => null
      ),
      attraction: SearchResultPresentationHelper.buildNamedResultPresentation(
         Strings.entityLabels.attraction,
         AttractionSelectorModel.getAttractionSubtitle
      ),
      giftShop: SearchResultPresentationHelper.buildNamedResultPresentation(
         Strings.entityLabels.giftShop,
         (row) => SearchResultPresenter.buildLocationSummary(
            row,
            Strings.entityLabels.giftShop
         )
      ),
      restroom: {
         getTitle: (row) => row.title || Strings.entityLabels.restroom,
         getSubtitle: () => null,
      },
      restaurant: SearchResultPresentationHelper.buildNamedResultPresentation(
         Strings.entityLabels.restaurant,
         (row) => SearchResultPresenter.buildLocationSummary(
            row,
            Strings.entityLabels.restaurant
         )
      ),
      pavilion: SearchResultPresentationHelper.buildNamedResultPresentation(
         Strings.entityLabels.pavilion,
         (row) => row.region
            ? Strings.search.region(row.region)
            : Strings.entityLabels.pavilion
      ),
   };

   static getSearchResultPresentation(row) {
      return SearchResultPresenter.SEARCH_RESULT_PRESENTATIONS[row.type]
         ?? SearchResultPresenter.DEFAULT_SEARCH_RESULT_PRESENTATION;
   }

   static createSearchImageRowRenderer({
      presentation,
      imageDirectory,
      getInfoLink = () => null,
      onTitleClick = null,
      shouldEnableTitleClick = null,
   } = {}) {
      const getImageName = presentation.getImageName ?? presentation.getTitle;

      return ResultRenderer.createDefaultSelectorRowLeftRenderer({
         getTitle: presentation.getTitle,
         getTitleSuffix: presentation.getTitleSuffix,
         getSubtitle: presentation.getSubtitle,
         getImageSrc: (row) => SearchResultPresenter.buildSearchDetailImageSrc(
            imageDirectory,
            getImageName(row)
         ),
         getInfoLink,
         onTitleClick,
         shouldEnableTitleClick,
      });
   }

   static createSearchImageRowRenderers(configs = []) {
      return configs.reduce((renderers, {
         type,
         imageDirectory,
         getInfoLink = () => null,
         onTitleClick = null,
      }) => {
         renderers[type] = SearchResultPresenter.createSearchImageRowRenderer({
            presentation: SearchResultPresenter.SEARCH_RESULT_PRESENTATIONS[type],
            imageDirectory,
            getInfoLink,
            onTitleClick,
         });

         return renderers;
      }, {});
   }

   static getRestaurantMenuLink(row) {
      return StoredSelectionNormalizer.normalizeStoredLink(row.menu_link);
   }
}
