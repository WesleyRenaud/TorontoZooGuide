import { ValueNormalizer } from '../api/valueNormalizer.js';
import { ExploreFilter } from './exploreFilter.js';
import { Strings } from '../strings.js';

export class ExploreFilterBinder {
   static TRANSPORTATION_ROUTE_SELECTOR = 'input[name="transportationRoute-zoomobile"]:checked';

   static DEFAULT_SELECTED_TYPES = ['animal'];

   static getSelectedTransportationRoute() {
      const checked = document.querySelector(ExploreFilterBinder.TRANSPORTATION_ROUTE_SELECTOR);
      return checked?.value ?? 'none';
   }

   static hasTransportationRoute(transportationRoute) {
      return transportationRoute !== 'none';
   }

   static createFallbackExploreFilter() {
      return {
         getSelectedTypes: () => [...ExploreFilterBinder.DEFAULT_SELECTED_TYPES],
         buildSearchIncludeFlags: () => ExploreFilter.buildExploreSearchIncludeFlags(
            ExploreFilterBinder.DEFAULT_SELECTED_TYPES,
            'none'
         ),
      };
   }

   static getFilterRefs(multiSelect) {
      const dropdown = multiSelect.querySelector('.multi-select-dropdown');

      return {
         button: multiSelect.querySelector('.multi-select-button'),
         dropdown,
         checkboxes: Array.from(dropdown?.querySelectorAll('input[type="checkbox"]') ?? []),
         chipContainer: multiSelect.querySelector('.selected-values'),
      };
   }

   static getCheckboxLabel(checkbox) {
      return ValueNormalizer.asTrimmedString(checkbox.closest('label')?.textContent)
         || checkbox.value;
   }

   static createNoSelectionChip() {
      const chip = document.createElement('span');
      chip.className = 'filter-none';
      chip.textContent = Strings.map.transportationRoute.none;
      return chip;
   }

   static createFilterChip(label) {
      const chip = document.createElement('span');
      chip.className = 'filter-chip';
      chip.textContent = label;
      return chip;
   }

   static getSelectedCheckboxes(checkboxes) {
      return checkboxes.filter((checkbox) => checkbox.checked);
   }

   static getSelectedTypeValues(checkboxes, transportationRoute) {
      const selected = ExploreFilterBinder.getSelectedCheckboxes(checkboxes)
         .map((checkbox) => String(checkbox.value || ''));

      if (ExploreFilterBinder.hasTransportationRoute(transportationRoute) && !selected.includes('transportationRoute')) {
         selected.push('transportationRoute');
      }

      return selected;
   }

   static renderSelectedChips(chipContainer, checkboxes) {
      if (!chipContainer) {
         return;
      }

      const selectedLabels = ExploreFilterBinder.getSelectedCheckboxes(checkboxes)
         .map(ExploreFilterBinder.getCheckboxLabel);

      if (selectedLabels.length === 0) {
         chipContainer.replaceChildren(ExploreFilterBinder.createNoSelectionChip());
         return;
      }

      chipContainer.replaceChildren(...selectedLabels.map(ExploreFilterBinder.createFilterChip));
   }

   static createExploreFilterState({
      checkboxes,
      getTransportationRoute,
   } = {}) {
      function getCurrentSelection() {
         const transportationRoute = getTransportationRoute();

         return {
            transportationRoute,
            selectedTypes: ExploreFilterBinder.getSelectedTypeValues(checkboxes, transportationRoute),
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

   static bindDropdownEvents({
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

   static bindCheckboxEvents({
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
}
