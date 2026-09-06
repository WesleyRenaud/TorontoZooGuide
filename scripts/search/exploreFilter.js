import { ValueNormalizer } from '../api/valueNormalizer.js';
import { Strings } from '../strings.js';

const TYPE_FILTER_ID = 'typeFilter';
const TRANSPORTATION_ROUTE_SELECTOR = 'input[name="transportationRoute-zoomobile"]:checked';
const DEFAULT_SELECTED_TYPES = ['animal'];

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

function getSelectedTransportationRoute() {
   const checked = document.querySelector(TRANSPORTATION_ROUTE_SELECTOR);
   return checked?.value ?? 'none';
}

function hasTransportationRoute(transportationRoute) {
   return transportationRoute !== 'none';
}

function createFallbackExploreFilter() {
   return {
      getSelectedTypes: () => [...DEFAULT_SELECTED_TYPES],
      buildSearchIncludeFlags: () => ExploreFilter.buildExploreSearchIncludeFlags(
         DEFAULT_SELECTED_TYPES,
         'none'
      ),
   };
}

function getFilterRefs(multiSelect) {
   const dropdown = multiSelect.querySelector('.multi-select-dropdown');

   return {
      button: multiSelect.querySelector('.multi-select-button'),
      dropdown,
      checkboxes: Array.from(dropdown?.querySelectorAll('input[type="checkbox"]') ?? []),
      chipContainer: multiSelect.querySelector('.selected-values'),
   };
}

function getCheckboxLabel(checkbox) {
   return ValueNormalizer.asTrimmedString(checkbox.closest('label')?.textContent)
      || checkbox.value;
}

function createNoSelectionChip() {
   const chip = document.createElement('span');
   chip.className = 'filter-none';
   chip.textContent = Strings.map.transportationRoute.none;
   return chip;
}

function createFilterChip(label) {
   const chip = document.createElement('span');
   chip.className = 'filter-chip';
   chip.textContent = label;
   return chip;
}

function getSelectedCheckboxes(checkboxes) {
   return checkboxes.filter((checkbox) => checkbox.checked);
}

function getSelectedTypeValues(checkboxes, transportationRoute) {
   const selected = getSelectedCheckboxes(checkboxes)
      .map((checkbox) => String(checkbox.value || ''));

   if (hasTransportationRoute(transportationRoute) && !selected.includes('transportationRoute')) {
      selected.push('transportationRoute');
   }

   return selected;
}

function renderSelectedChips(chipContainer, checkboxes) {
   if (!chipContainer) {
      return;
   }

   const selectedLabels = getSelectedCheckboxes(checkboxes)
      .map(getCheckboxLabel);

   if (selectedLabels.length === 0) {
      chipContainer.replaceChildren(createNoSelectionChip());
      return;
   }

   chipContainer.replaceChildren(...selectedLabels.map(createFilterChip));
}

function createExploreFilterState({
   checkboxes,
   getTransportationRoute,
} = {}) {
   function getCurrentSelection() {
      const transportationRoute = getTransportationRoute();

      return {
         transportationRoute,
         selectedTypes: getSelectedTypeValues(checkboxes, transportationRoute),
      };
   }

   function getSelectedTypes() {
      return getCurrentSelection().selectedTypes;
   }

   function buildSearchIncludeFlags() {
      const { selectedTypes, transportationRoute } = getCurrentSelection();
      return ExploreFilter.buildExploreSearchIncludeFlags(selectedTypes, transportationRoute);
   }

   return { getSelectedTypes, buildSearchIncludeFlags };
}

function bindDropdownEvents({
   multiSelect,
   button,
   dropdown,
} = {}) {
   button?.addEventListener('click', (event) => {
      event.stopPropagation();
      multiSelect.classList.toggle('open');
   });

   dropdown?.addEventListener('click', (event) => {
      event.stopPropagation();
   });

   document.addEventListener('click', () => {
      multiSelect.classList.remove('open');
   });
}

function bindCheckboxEvents({
   checkboxes,
   getSelectedTypes,
   onAnimalsUnchecked,
   onChange,
   onSelectionChanged,
} = {}) {
   checkboxes.forEach((checkbox) => {
      checkbox.addEventListener('change', () => {
         onSelectionChanged?.();

         if (!getSelectedTypes().includes('animal')) {
            onAnimalsUnchecked?.();
         }

         onChange?.();
      });
   });
}

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
         includeTransportationStations: hasTransportationRoute(transportationRoute),
         ...(hasTransportationRoute(transportationRoute) ? { transportationRoute } : {}),
      };
   }

   static initExploreTypeFilter({
      onChange,
      onAnimalsUnchecked,
      multiSelect = document.getElementById(TYPE_FILTER_ID),
      getTransportationRoute = getSelectedTransportationRoute,
   } = {}) {
      if (!multiSelect) {
         return createFallbackExploreFilter();
      }

      const {
         button,
         dropdown,
         checkboxes,
         chipContainer,
      } = getFilterRefs(multiSelect);

      const state = createExploreFilterState({
         checkboxes,
         getTransportationRoute,
      });

      const updateSelectedChips = () => {
         renderSelectedChips(chipContainer, checkboxes);
      };

      bindDropdownEvents({
         multiSelect,
         button,
         dropdown,
      });

      bindCheckboxEvents({
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
