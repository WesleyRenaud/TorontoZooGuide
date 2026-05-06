import { APP_STRINGS } from '../strings.js';

const TYPE_FILTER_ID = 'typeFilter';
const ZOOMOBILE_ROUTE_SELECTOR = 'input[name="zoomobileRoute"]:checked';
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

function getSelectedZoomobileRoute() {
   const checked = document.querySelector(ZOOMOBILE_ROUTE_SELECTOR);
   return checked?.value ?? 'none';
}

function hasZoomobileRoute(zoomobileRoute) {
   return zoomobileRoute !== 'none';
}

export function buildExploreSearchIncludeFlags(selectedTypes, zoomobileRoute) {
   const selectedTypeSet = new Set(selectedTypes);

   return {
      ...Object.fromEntries(
         SEARCH_INCLUDE_FLAGS.map(([flag, type]) => [
            flag,
            selectedTypeSet.has(type),
         ])
      ),
      includeZoomobileStations: hasZoomobileRoute(zoomobileRoute),
   };
}

function createFallbackExploreFilter() {
   return {
      getSelectedTypes: () => [...DEFAULT_SELECTED_TYPES],
      buildSearchIncludeFlags: () => buildExploreSearchIncludeFlags(DEFAULT_SELECTED_TYPES, 'none'),
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
   return checkbox.closest('label')?.textContent?.trim() || checkbox.value;
}

function createNoSelectionChip() {
   const chip = document.createElement('span');
   chip.className = 'filter-none';
   chip.textContent = APP_STRINGS.map.zoomobileRoute.none;
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

function getSelectedTypeValues(checkboxes, zoomobileRoute) {
   const selected = getSelectedCheckboxes(checkboxes)
      .map((checkbox) => String(checkbox.value || ''));

   if (hasZoomobileRoute(zoomobileRoute) && !selected.includes('zoomobileRoute')) {
      selected.push('zoomobileRoute');
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
   getZoomobileRoute,
} = {}) {
   function getCurrentSelection() {
      const zoomobileRoute = getZoomobileRoute();

      return {
         zoomobileRoute,
         selectedTypes: getSelectedTypeValues(checkboxes, zoomobileRoute),
      };
   }

   function getSelectedTypes() {
      return getCurrentSelection().selectedTypes;
   }

   function buildSearchIncludeFlags() {
      const { selectedTypes, zoomobileRoute } = getCurrentSelection();
      return buildExploreSearchIncludeFlags(selectedTypes, zoomobileRoute);
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

export function initExploreTypeFilter({
   onChange,
   onAnimalsUnchecked,
   multiSelect = document.getElementById(TYPE_FILTER_ID),
   getZoomobileRoute = getSelectedZoomobileRoute,
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
      getZoomobileRoute,
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
