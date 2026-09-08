import { ExploreFilterBinder } from './exploreFilterBinder.js';
import { ItemType } from '../shared/enums/itemType.js';

export class ExploreFilter {
   static TYPE_FILTER_ID = 'typeFilter';

   static SEARCH_INCLUDE_FLAGS = [
      ['includeAnimals', ItemType.ANIMAL],
      ['includePavilions', ItemType.PAVILION],
      ['includeRestaurants', ItemType.RESTAURANT],
      ['includeRestrooms', ItemType.RESTROOM],
      ['includeGiftShops', ItemType.GIFT_SHOP],
      ['includeAttractions', ItemType.ATTRACTION],
      ['includeGuardiansTalks', ItemType.GUARDIANS_TALK],
      ['includeWildEncounters', ItemType.WILD_ENCOUNTER],
   ];

   static buildExploreSearchIncludeFlags(selectedTypes, transportationRoute) {
      const selectedTypeSet = new Set(selectedTypes);

      return {
         ...Object.fromEntries(
            ExploreFilter.SEARCH_INCLUDE_FLAGS.map(([flag, type]) => [
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
      multiSelect = document.getElementById(ExploreFilter.TYPE_FILTER_ID),
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
