import { VisitDateFlatpickr } from '../visitDates/visitDateFlatpickr.js';
import { VisitDateRules } from '../visitDates/visitDateRules.js';

export class MapControlsBinder {
   static blurMapDateInput(mapDateInput) {
      mapDateInput?.blur();
      document.activeElement?.blur?.();
   }

   static closeMapDatePicker(fp, mapDateInput) {
      fp?.close();
      MapControlsBinder.blurMapDateInput(mapDateInput);
   }

   static isSpecificDayPreset(mapPreset) {
      return mapPreset?.value === 'specific-day';
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

         onUpdate('specific-day', dateStr);
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
   } = {}) {
      const floor = earliestSelectableNoon ?? VisitDateRules.getToday();

      return VisitDateFlatpickr.initVisitDateFlatpickr(mapDateInput, {
         defaultDate: floor,
         earliestNoon: floor,
         clickOpens: false,
         onChange: (_safeDate, isoDate, instance) => {
            instance.close();
            MapControlsBinder.blurMapDateInput(mapDateInput);

            if (MapControlsBinder.isSpecificDayPreset(mapPreset)) {
               onSpecificDayChange(isoDate);
            }
         },
         onClose: () => {
            MapControlsBinder.blurMapDateInput(mapDateInput);
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
      MapControlsBinder.closeMapDatePicker(fp, mapDateInput);

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

      const fp = MapControlsBinder.initMapDatePicker(mapDateInput, {
         mapPreset,
         earliestSelectableNoon,
         onSpecificDayChange: (dateStr) => {
            onUpdate('specific-day', dateStr);
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
         fp?.open();
      });

      mapDateInput.addEventListener('focus', () => {
         MapControlsBinder.blurMapDateInput(mapDateInput);
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
