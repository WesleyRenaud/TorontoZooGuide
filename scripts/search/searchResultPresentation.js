import { DetailImageSrc } from '../assets/detailImageSrc.js';
import { AnimalSelectorModel } from '../itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { createDefaultSelectorRowLeftRenderer } from '../itinerary/selectors/base/resultRenderer.js';
import { StoredSelection } from '../itinerary/selectors/base/storedSelection.js';
import { GuardiansTalkSelectorModel } from '../itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { WildEncounterSelectorModel } from '../itinerary/selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { APP_STRINGS } from '../strings.js';

const SEARCH_DETAIL_IMAGE_BASE_PATH = '../images/details';

export function buildSearchDetailImageSrc(imageDirectory, name) {
   return DetailImageSrc.buildDetailImageSrc(imageDirectory, name, {
      basePath: SEARCH_DETAIL_IMAGE_BASE_PATH,
   });
}

export function buildDetailSummary(parts, fallback) {
   const details = parts.filter(Boolean);

   if (details.length === 0) {
      return fallback;
   }

   return `${fallback}\n${details.join(' | ')}`;
}

export function buildLocationSummary(row, fallback) {
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

export const SEARCH_RESULT_PRESENTATIONS = {
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
      APP_STRINGS.entityLabels.transportationStation,
      () => null
   ),
   attraction: buildNamedResultPresentation(
      APP_STRINGS.entityLabels.attraction,
      AttractionSelectorModel.getAttractionSubtitle
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

const DEFAULT_SEARCH_RESULT_PRESENTATION = {
   getTitle: AnimalSelectorModel.getAnimalTitleLine,
   getSubtitle: AnimalSelectorModel.getAnimalSubtitle,
};

export function getSearchResultPresentation(row) {
   return SEARCH_RESULT_PRESENTATIONS[row.type] ?? DEFAULT_SEARCH_RESULT_PRESENTATION;
}

export function createSearchImageRowRenderer({
   presentation,
   imageDirectory,
   getInfoLink = () => null,
   onTitleClick = null,
   shouldEnableTitleClick = null,
} = {}) {
   const getImageName = presentation.getImageName ?? presentation.getTitle;

   return createDefaultSelectorRowLeftRenderer({
      getTitle: presentation.getTitle,
      getTitleSuffix: presentation.getTitleSuffix,
      getSubtitle: presentation.getSubtitle,
      getImageSrc: (row) => buildSearchDetailImageSrc(
         imageDirectory,
         getImageName(row)
      ),
      getInfoLink,
      onTitleClick,
      shouldEnableTitleClick,
   });
}

export function createSearchImageRowRenderers(configs = []) {
   return configs.reduce((renderers, {
      type,
      imageDirectory,
      getInfoLink = () => null,
      onTitleClick = null,
   }) => {
      renderers[type] = createSearchImageRowRenderer({
         presentation: SEARCH_RESULT_PRESENTATIONS[type],
         imageDirectory,
         getInfoLink,
         onTitleClick,
      });

      return renderers;
   }, {});
}

export function getRestaurantMenuLink(row) {
   return StoredSelection.normalizeStoredLink(row.menu_link);
}
