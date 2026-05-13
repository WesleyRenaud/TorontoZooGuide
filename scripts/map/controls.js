import { initVisitDateFlatpickr } from '../visitDates/visitDateFlatpickr.js';
import { getToday } from '../visitDates/visitDateRules.js';

function blurMapDateInput(mapDateInput) {
   mapDateInput?.blur();
   document.activeElement?.blur?.();
}

function closeMapDatePicker(fp, mapDateInput) {
   fp?.close();
   blurMapDateInput(mapDateInput);
}

function isSpecificDayPreset(mapPreset) {
   return mapPreset?.value === 'specific-day';
}

function getCurrentDateStr(mapDateInput, fp) {
   return mapDateInput?.value || fp?.input?.value || '';
}

function syncDateInputVisibility(mapPreset, mapDateInput) {
   mapDateInput.style.display = isSpecificDayPreset(mapPreset)
      ? 'inline-block'
      : 'none';
}

function updateMapForCurrentControls({
   mapPreset,
   mapDateInput,
   fp,
   onUpdate,
} = {}) {
   const preset = mapPreset?.value || '';

   if (!preset) {
      return;
   }

   if (isSpecificDayPreset(mapPreset)) {
      const dateStr = getCurrentDateStr(mapDateInput, fp);

      if (!dateStr) {
         return;
      }

      onUpdate('specific-day', dateStr);
      return;
   }

   onUpdate(preset, null);
}

function bindChangeListeners(inputs, onChange) {
   Array.from(inputs || [])
      .filter(Boolean)
      .forEach((input) => {
         input.addEventListener('change', onChange);
      });
}

function initMapDatePicker(mapDateInput, {
   mapPreset,
   onSpecificDayChange,
   earliestSelectableNoon,
} = {}) {
   const floor = earliestSelectableNoon ?? getToday();

   return initVisitDateFlatpickr(mapDateInput, {
      defaultDate: floor,
      earliestNoon: floor,
      clickOpens: false,
      onChange: (_safeDate, isoDate, instance) => {
         instance.close();
         blurMapDateInput(mapDateInput);

         if (isSpecificDayPreset(mapPreset)) {
            onSpecificDayChange(isoDate);
         }
      },
      onClose: () => {
         blurMapDateInput(mapDateInput);
      },
   });
}

function handlePresetChange({
   mapPreset,
   mapDateInput,
   fp,
   onUpdate,
} = {}) {
   syncDateInputVisibility(mapPreset, mapDateInput);
   closeMapDatePicker(fp, mapDateInput);

   if (!mapPreset?.value) {
      return;
   }

   updateMapForCurrentControls({
      mapPreset,
      mapDateInput,
      fp,
      onUpdate,
   });
}

export function initMapControls({
   mapPreset,
   mapDateInput,
   includeOffDisplayCheckbox,
   includeClosedRestaurantsCheckbox,
   includeClosedRestroomsCheckbox,
   includeClosedGiftShopsCheckbox,
   includeClosedAttractionsCheckbox,
   zoomobileRouteRadios,
   earliestSelectableNoon,
   onUpdate,
} = {}) {
   if (!mapPreset || !mapDateInput || !onUpdate) {
      console.warn('[controls] missing elements:', { mapPreset, mapDateInput, onUpdate });
      return null;
   }

   const fp = initMapDatePicker(mapDateInput, {
      mapPreset,
      earliestSelectableNoon,
      onSpecificDayChange: (dateStr) => {
         onUpdate('specific-day', dateStr);
      },
   });

   const refetch = () => updateMapForCurrentControls({
      mapPreset,
      mapDateInput,
      fp,
      onUpdate,
   });

   mapPreset.addEventListener('change', () => {
      handlePresetChange({
         mapPreset,
         mapDateInput,
         fp,
         onUpdate,
      });
   });

   mapDateInput.addEventListener('mousedown', (event) => {
      if (!isSpecificDayPreset(mapPreset)) {
         return;
      }

      event.preventDefault();
      fp?.open();
   });

   mapDateInput.addEventListener('focus', () => {
      blurMapDateInput(mapDateInput);
   });

   bindChangeListeners([
      includeOffDisplayCheckbox,
      includeClosedRestaurantsCheckbox,
      includeClosedRestroomsCheckbox,
      includeClosedGiftShopsCheckbox,
      includeClosedAttractionsCheckbox,
   ], refetch);

   bindChangeListeners(zoomobileRouteRadios, refetch);

   syncDateInputVisibility(mapPreset, mapDateInput);

   return {
      flatpickr: fp,
      refetch,
   };
}
