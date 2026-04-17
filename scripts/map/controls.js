import { initVisitDateFlatpickr } from '../visitDates/visitDateFlatpickr.js';

export function initMapControls(
   {
      mapPreset,
      mapDateInput,
      includeOffDisplayCheckbox,
      includeClosedRestaurantsCheckbox,
      includeClosedGiftShopsCheckbox,
      includeClosedAttractionsCheckbox,
      zoomobileRouteRadios,
      onUpdate
   }
) {
   if (!mapPreset || !mapDateInput || !onUpdate) {
      console.warn('[controls] missing elements:', { mapPreset, mapDateInput, onUpdate });
      return;
   }

   const fp = initVisitDateFlatpickr(mapDateInput, {
      defaultDate: new Date(),
      clickOpens: false,
      onChange: (_safeDate, isoDate, instance) => {
         instance.close();
         mapDateInput.blur();
         document.activeElement?.blur?.();

         if (mapPreset.value === 'specific-day') {
            onUpdate('specific-day', isoDate);
         }
      },
      onClose: () => {
         mapDateInput.blur();
         document.activeElement?.blur?.();
      }
   });

   function currentDateStr() {
      return mapDateInput.value || fp?.input?.value || '';
   }

   function refetch() {
      const preset = mapPreset.value;

      if (!preset) return;

      if (preset === 'specific-day') {
         const dateStr = currentDateStr();
         if (!dateStr) return;
         onUpdate('specific-day', dateStr);
      }
      else {
         onUpdate(preset, null);
      }
   }

   mapPreset.addEventListener('change', () => {
      const preset = mapPreset.value;

      if (!preset) {
         mapDateInput.style.display = 'none';
         fp?.close();
         mapDateInput.blur();
         return;
      }

      if (preset === 'specific-day') {
         mapDateInput.style.display = 'inline-block';
         fp?.close();
         mapDateInput.blur();
         onUpdate('specific-day', currentDateStr());
      }
      else {
         mapDateInput.style.display = 'none';
         fp?.close();
         mapDateInput.blur();
         onUpdate(preset, null);
      }
   });

   mapDateInput.addEventListener('mousedown', event => {
      if (mapPreset.value !== 'specific-day') return;

      event.preventDefault();
      fp?.open();
   });

   mapDateInput.addEventListener('focus', () => {
      mapDateInput.blur();
   });

   if (includeOffDisplayCheckbox) {
      includeOffDisplayCheckbox.addEventListener('change', () => {
         refetch();
      });
   }

   if (includeClosedRestaurantsCheckbox) {
      includeClosedRestaurantsCheckbox.addEventListener('change', () => {
         refetch();
      });
   }

   if (includeClosedGiftShopsCheckbox) {
      includeClosedGiftShopsCheckbox.addEventListener('change', () => {
         refetch();
      });
   }

   if (includeClosedAttractionsCheckbox) {
      includeClosedAttractionsCheckbox.addEventListener('change', () => {
         refetch();
      });
   }

   if (zoomobileRouteRadios) {
      Array.from(zoomobileRouteRadios || []).forEach(r => {
         r.addEventListener('change', () => {
            refetch();
         });
      });
   }
}
