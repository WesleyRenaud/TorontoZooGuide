import { FocusFromParser } from '../focus/focusFromParser.js';
import { DateContext } from '../map/dateContext.js';
import { MapControlsBinder } from '../map/mapControlsBinder.js';
import { ExploreFilter } from '../search/exploreFilter.js';
import { SearchController } from '../search/searchController.js';

export class MapPageBootstrap {
   static getMapPageElements() {
      return {
         mapInner: document.getElementById('mapInner'),
         mapPreset: document.getElementById('mapPreset'),
         mapDateInput: document.getElementById('mapDate'),
         showMapLabelsCheckbox: document.getElementById('showMapLabels'),
         includeOffDisplayCheckbox: document.getElementById('includeOffDisplayAnimals'),
         includeClosedRestaurantsCheckbox: document.getElementById('includeClosedRestaurants'),
         includeClosedRestroomsCheckbox: document.getElementById('includeClosedRestrooms'),
         includeClosedGiftShopsCheckbox: document.getElementById('includeClosedGiftShops'),
         includeClosedAttractionsCheckbox: document.getElementById('includeClosedAttractions'),
         transportationRoutesEl: document.getElementById('transportationRoutes'),
         animalSearchInput: document.getElementById('animalSearch'),
         animalSearchResultsEl: document.getElementById('animalSearchResults'),
         exploreUpdatesListEl: document.getElementById('exploreUpdatesList'),
         tooltipEl: document.getElementById('tooltip'),
         hoverTooltipEl: document.getElementById('hoverTooltip'),
      };
   }

   static hasRequiredMapPageElements({
      mapInner,
      mapPreset,
      mapDateInput,
      tooltipEl,
   } = {}) {
      return Boolean(mapInner && mapPreset && mapDateInput && tooltipEl);
   }

   static isCoordinateEditingEnabled() {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get('editCoords') === '1';
   }

   static getSelectedTransportationRoute() {
      return Array.from(document.querySelectorAll('input[name="transportationRoute-zoomobile"]'))
         .find((radio) => radio.checked)
         ?.value ?? 'none';
   }

   static clearAnimalSearchResults(resultsEl) {
      resultsEl?.replaceChildren();
   }

   static createMapDateContextGetter({
      mapPreset,
      mapDateInput,
   } = {}) {
      return async () => {
         const preset = mapPreset?.value || '';
         const dateStr = mapDateInput?.value?.trim?.() || '';
         return await DateContext.buildMapDateContext(preset, dateStr);
      };
   }

   static createRuntimeOptions(elements, {
      getSelectedTypes,
      updates,
   } = {}) {
      return {
         mapInner: elements.mapInner,
         tooltipEl: elements.tooltipEl,
         hoverTooltipEl: elements.hoverTooltipEl,
         showMapLabelsCheckbox: elements.showMapLabelsCheckbox,
         enableCoordinateEditing: MapPageBootstrap.isCoordinateEditingEnabled(),
         getIncludeOffDisplay: () => elements.includeOffDisplayCheckbox?.checked ?? false,
         getIncludeClosedRestaurants: () => elements.includeClosedRestaurantsCheckbox?.checked ?? false,
         getIncludeClosedRestrooms: () => elements.includeClosedRestroomsCheckbox?.checked ?? false,
         getIncludeClosedGiftShops: () => elements.includeClosedGiftShopsCheckbox?.checked ?? false,
         getIncludeClosedAttractions: () => elements.includeClosedAttractionsCheckbox?.checked ?? false,
         getTransportationRoute: () => MapPageBootstrap.getSelectedTransportationRoute(),
         getSelectedTypes,
         onDateContextChange: (dateCtx) => updates?.refresh?.(dateCtx),
      };
   }

   static initMapExploreFilter({
      updater,
      getSearch,
      animalSearchResultsEl,
   } = {}) {
      return ExploreFilter.initExploreTypeFilter({
         onChange: () => {
            updater.refetchWithCurrentControls(null);
            getSearch()?.refresh?.();
         },
         onAnimalsUnchecked: () => {
            MapPageBootstrap.clearAnimalSearchResults(animalSearchResultsEl);
         },
      });
   }

   static initMapSearch({
      elements,
      explore,
      updater,
   } = {}) {
      return SearchController.initSearch({
         inputEl: elements.animalSearchInput,
         resultsEl: elements.animalSearchResultsEl,
         getIncludeFlags: () => ({
            ...explore.buildSearchIncludeFlags(),
            includeClosedRestaurants: elements.includeClosedRestaurantsCheckbox?.checked ?? false,
            includeClosedRestrooms: elements.includeClosedRestroomsCheckbox?.checked ?? false,
            includeClosedGiftShops: elements.includeClosedGiftShopsCheckbox?.checked ?? false,
            includeClosedAttractions: elements.includeClosedAttractionsCheckbox?.checked ?? false,
         }),
         getContext: MapPageBootstrap.createMapDateContextGetter(elements),
         onFocusRow: (row) => updater.focusFromSearchRow(row),
      });
   }

   static initMapPageControls({
      elements,
      updater,
      getSearch,
      earliestSelectableNoon,
   } = {}) {
      MapControlsBinder.initMapControls({
         mapPreset: elements.mapPreset,
         mapDateInput: elements.mapDateInput,
         includeOffDisplayCheckbox: elements.includeOffDisplayCheckbox,
         includeClosedRestaurantsCheckbox: elements.includeClosedRestaurantsCheckbox,
         includeClosedRestroomsCheckbox: elements.includeClosedRestroomsCheckbox,
         includeClosedGiftShopsCheckbox: elements.includeClosedGiftShopsCheckbox,
         includeClosedAttractionsCheckbox: elements.includeClosedAttractionsCheckbox,
         transportationRouteRadios: document.querySelectorAll('input[name="transportationRoute-zoomobile"]'),
         earliestSelectableNoon,
         onUpdate: (preset, dateStr) => {
            updater.updateMap(preset, dateStr, null);
            getSearch()?.refresh?.();
         },
      });
   }

   static initMapDeepLinkFocus(updater) {
      FocusFromParser.initFocusFromQuery({
         onFocus: (rowOrSpec) => {
            updater.focusFromDeepLink(rowOrSpec);
         },
      });
   }

   static triggerInitialMapUpdate(mapPreset) {
      mapPreset.dispatchEvent(new Event('change'));
   }
}
