import { ExploreFilterBinder } from './exploreFilterBinder.js';

const TYPE_FILTER_ID = 'typeFilter';

const SEARCH_INCLUDE_FLAGS = [
   ['includeAnimals', 'animal'],
   ['includePavilions', 'pavilion'],
   ['includeRestaurants', 'restaurant'],
   ['includeRestrooms', 'restroom'],
   ['includeGiftShops', 'giftShop'],
   ['includeAttractions', 'attraction'],
   ['includeGuardiansTalks', 'guardiansTalk'],
   ['includeWildEncounters', 'wildEncounter'],
];

export class ExploreFilter {
   static buildExploreSearchIncludeFlags(selectedTypes, transportationRoute) {
      const selectedTypeSet = new Set(selectedTypes);

      return {
         ...Object.fromEntries(
            SEARCH_INCLUDE_FLAGS.map(([flag, type]) => [
               flag,
               selectedTypeSet.has(type),
            ])
         ),
         includeTransportationStations: ExploreFilterBinder.hasTransportationRoute(transportationRoute),
         ...(ExploreFilterBinder.hasTransportationRoute(transportationRoute) ? { transportationRoute } : {}),
      };
   }

   static initExploreTypeFilter({
      onChange,
      onAnimalsUnchecked,
      multiSelect = document.getElementById(TYPE_FILTER_ID),
      getTransportationRoute = ExploreFilterBinder.getSelectedTransportationRoute,
   } = {}) {
      if (!multiSelect) {
         return ExploreFilterBinder.createFallbackExploreFilter();
      }

      const {
         button,
         dropdown,
         checkboxes,
         chipContainer,
      } = ExploreFilterBinder.getFilterRefs(multiSelect);

      const state = ExploreFilterBinder.createExploreFilterState({
         checkboxes,
         getTransportationRoute,
      });

      const updateSelectedChips = () => {
         ExploreFilterBinder.renderSelectedChips(chipContainer, checkboxes);
      };

      ExploreFilterBinder.bindDropdownEvents({
         multiSelect,
         button,
         dropdown,
      });

      ExploreFilterBinder.bindCheckboxEvents({
         checkboxes,
         getSelectedTypes: state.getSelectedTypes,
         onAnimalsUnchecked,
         onChange,
         onSelectionChanged: updateSelectedChips,
      });

      updateSelectedChips();

      return state;
   }
}
