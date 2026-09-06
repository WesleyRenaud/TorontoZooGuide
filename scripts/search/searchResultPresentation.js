import { DetailImageSrc } from '../assets/detailImageSrc.js';
import { AnimalSelectorModel } from '../itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { ResultRenderer } from '../itinerary/selectors/base/resultRenderer.js';
import { StoredSelection } from '../itinerary/selectors/base/storedSelection.js';
import { GuardiansTalkSelectorModel } from '../itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { WildEncounterSelectorModel } from '../itinerary/selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { Strings } from '../strings.js';

const SEARCH_DETAIL_IMAGE_BASE_PATH = '../images/details';

function buildNamedResultPresentation(fallbackTitle, getSubtitle) {
   return {
      getTitle: (row) => row.name || fallbackTitle,
      getSubtitle,
   };
}

const DEFAULT_SEARCH_RESULT_PRESENTATION = {
   getTitle: AnimalSelectorModel.getAnimalTitleLine,
   getSubtitle: AnimalSelectorModel.getAnimalSubtitle,
};

export class SearchResultPresentation {
   static buildSearchDetailImageSrc(imageDirectory, name) {
      return DetailImageSrc.buildDetailImageSrc(imageDirectory, name, {
         basePath: SEARCH_DETAIL_IMAGE_BASE_PATH,
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
      transportationStation: buildNamedResultPresentation(
         Strings.entityLabels.transportationStation,
         () => null
      ),
      attraction: buildNamedResultPresentation(
         Strings.entityLabels.attraction,
         AttractionSelectorModel.getAttractionSubtitle
      ),
      giftShop: buildNamedResultPresentation(
         Strings.entityLabels.giftShop,
         (row) => SearchResultPresentation.buildLocationSummary(
            row,
            Strings.entityLabels.giftShop
         )
      ),
      restroom: {
         getTitle: (row) => row.title || Strings.entityLabels.restroom,
         getSubtitle: () => null,
      },
      restaurant: buildNamedResultPresentation(
         Strings.entityLabels.restaurant,
         (row) => SearchResultPresentation.buildLocationSummary(
            row,
            Strings.entityLabels.restaurant
         )
      ),
      pavilion: buildNamedResultPresentation(
         Strings.entityLabels.pavilion,
         (row) => row.region
            ? Strings.search.region(row.region)
            : Strings.entityLabels.pavilion
      ),
   };

   static getSearchResultPresentation(row) {
      return SearchResultPresentation.SEARCH_RESULT_PRESENTATIONS[row.type]
         ?? DEFAULT_SEARCH_RESULT_PRESENTATION;
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
         getImageSrc: (row) => SearchResultPresentation.buildSearchDetailImageSrc(
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
         renderers[type] = SearchResultPresentation.createSearchImageRowRenderer({
            presentation: SearchResultPresentation.SEARCH_RESULT_PRESENTATIONS[type],
            imageDirectory,
            getInfoLink,
            onTitleClick,
         });

         return renderers;
      }, {});
   }

   static getRestaurantMenuLink(row) {
      return StoredSelection.normalizeStoredLink(row.menu_link);
   }
}
