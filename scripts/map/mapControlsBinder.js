import { Strings } from '../strings.js';
import { VisitDateAdapter } from '../visitDates/visitDateAdapter.js';
import { VisitDateValidator } from '../visitDates/visitDateValidator.js';

export class MapControlsBinder {
   static MAP_DATE_OPEN_KEYS = new Set(['Enter', ' ', 'ArrowDown']);

   static blurMapDateInput(mapDateInput) {
      mapDateInput?.blur();
      document.activeElement?.blur?.();
   }

   static closeMapDatePicker(fp) {
      if (fp?.isOpen) {
         fp.close();
      }
   }

   static finishMapDatePicker(mapDateInput, keyboardState) {
      if (keyboardState?.returnFocus) {
         mapDateInput?.focus?.();
         return;
      }

      MapControlsBinder.blurMapDateInput(mapDateInput);
   }

   static openMapDatePickerFromKeyboard(fp, keyboardState) {
      keyboardState.returnFocus = true;

      if (!fp) {
         return;
      }

      fp.open();

      const dayToFocus = fp.selectedDateElem ?? fp.todayDateElem;
      dayToFocus?.focus();
   }

   static isSpecificDayPreset(mapPreset) {
      return mapPreset?.value === Strings.map.presetIds.specificDay;
   }

   static getCurrentDateStr(mapDateInput, fp) {
      return mapDateInput?.value || fp?.input?.value || '';
   }

   static syncDateInputVisibility(mapPreset, mapDateInput) {
      mapDateInput.style.display = MapControlsBinder.isSpecificDayPreset(mapPreset)
         ? 'inline-block'
         : 'none';
   }

   static updateMapForCurrentControls({
      mapPreset,
      mapDateInput,
      fp,
      onUpdate,
   } = {}) {
      const preset = mapPreset?.value || '';

      if (!preset) {
         return;
      }

      if (MapControlsBinder.isSpecificDayPreset(mapPreset)) {
         const dateStr = MapControlsBinder.getCurrentDateStr(mapDateInput, fp);

         if (!dateStr) {
            return;
         }

         onUpdate(Strings.map.presetIds.specificDay, dateStr);
         return;
      }

      const anchorIso = MapControlsBinder.getCurrentDateStr(mapDateInput, fp) || null;
      onUpdate(preset, anchorIso);
   }

   static bindChangeListeners(inputs, onChange) {
      Array.from(inputs || [])
         .filter(Boolean)
         .forEach((input) => {
            input.addEventListener('change', onChange);
         });
   }

   static initMapDatePicker(mapDateInput, {
      mapPreset,
      onSpecificDayChange,
      earliestSelectableNoon,
      keyboardState = {},
   } = {}) {
      const floor = earliestSelectableNoon ?? VisitDateValidator.getToday();

      return VisitDateAdapter.initVisitDateFlatpickr(mapDateInput, {
         defaultDate: floor,
         earliestNoon: floor,
         clickOpens: false,
         onChange: (_safeDate, isoDate, instance) => {
            instance.close();
            MapControlsBinder.finishMapDatePicker(mapDateInput, keyboardState);

            if (MapControlsBinder.isSpecificDayPreset(mapPreset)) {
               onSpecificDayChange(isoDate);
            }
         },
         onClose: () => {
            MapControlsBinder.finishMapDatePicker(mapDateInput, keyboardState);
         },
      });
   }

   static handlePresetChange({
      mapPreset,
      mapDateInput,
      fp,
      onUpdate,
   } = {}) {
      MapControlsBinder.syncDateInputVisibility(mapPreset, mapDateInput);
      MapControlsBinder.closeMapDatePicker(fp);

      if (!mapPreset?.value) {
         return;
      }

      MapControlsBinder.updateMapForCurrentControls({
         mapPreset,
         mapDateInput,
         fp,
         onUpdate,
      });
   }

   static initMapControls({
   mapPreset,
   mapDateInput,
   includeOffDisplayCheckbox,
   includeClosedRestaurantsCheckbox,
   includeClosedRestroomsCheckbox,
   includeClosedGiftShopsCheckbox,
   includeClosedAttractionsCheckbox,
   transportationRouteRadios,
   earliestSelectableNoon,
   onUpdate,
} = {}) {
      if (!mapPreset || !mapDateInput || !onUpdate) {
         console.warn('[controls] missing elements:', { mapPreset, mapDateInput, onUpdate });
         return null;
      }

      const keyboardState = { returnFocus: false };
      const fp = MapControlsBinder.initMapDatePicker(mapDateInput, {
         mapPreset,
         earliestSelectableNoon,
         keyboardState,
         onSpecificDayChange: (dateStr) => {
            onUpdate(Strings.map.presetIds.specificDay, dateStr);
         },
      });

      const refetch = () => MapControlsBinder.updateMapForCurrentControls({
         mapPreset,
         mapDateInput,
         fp,
         onUpdate,
      });

      mapPreset.addEventListener('change', () => {
         MapControlsBinder.handlePresetChange({
            mapPreset,
            mapDateInput,
            fp,
            onUpdate,
         });
      });

      mapDateInput.addEventListener('mousedown', (event) => {
         if (!MapControlsBinder.isSpecificDayPreset(mapPreset)) {
            return;
         }

         event.preventDefault();
         keyboardState.returnFocus = false;
         fp?.open();
      });

      mapDateInput.addEventListener('keydown', (event) => {
         if (
            !MapControlsBinder.MAP_DATE_OPEN_KEYS.has(event.key)
            || !MapControlsBinder.isSpecificDayPreset(mapPreset)
         ) {
            return;
         }

         event.preventDefault();
         event.stopPropagation();
         MapControlsBinder.openMapDatePickerFromKeyboard(fp, keyboardState);
      });

      MapControlsBinder.bindChangeListeners([
         includeOffDisplayCheckbox,
         includeClosedRestaurantsCheckbox,
         includeClosedRestroomsCheckbox,
         includeClosedGiftShopsCheckbox,
         includeClosedAttractionsCheckbox,
      ], refetch);

      MapControlsBinder.bindChangeListeners(transportationRouteRadios, refetch);

      MapControlsBinder.syncDateInputVisibility(mapPreset, mapDateInput);

      return {
         flatpickr: fp,
         refetch,
      };
   }
}
