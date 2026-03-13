import { initFlatpickr } from '../ui/flatpickr.js';

export function initMapControls
   ({
      mapPreset,
      mapDateInput,
      includeOffDisplayCheckbox,
      includeSeasonalRestaurantsCheckbox,
      includeSeasonalGiftShopsCheckbox,
      includeClosedAttractionsCheckbox,
      zoomobileRouteTypeRadios,
      onUpdate
   }) {

   if (!mapPreset || !mapDateInput || !onUpdate) {
      console.warn('[controls] missing elements:', { mapPreset, mapDateInput, onUpdate });
      return;
   }

   const fp = initFlatpickr(mapDateInput, {
      defaultDate: new Date(),
      dateFormat: 'Y-m-d',
      minDate: 'today',
      onChange: (_, dateStr) => {
         if (mapPreset.value === 'specific-day') onUpdate('specific-day', dateStr);
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
      } else {
         onUpdate(preset, null);
      }
   }

   mapPreset.addEventListener('change', () => {
      const preset = mapPreset.value;

      if (!preset) {
         mapDateInput.style.display = 'none';
         return;
      }

      if (preset === 'specific-day') {
         mapDateInput.style.display = 'inline-block';
         onUpdate('specific-day', currentDateStr());
      } else {
         mapDateInput.style.display = 'none';
         onUpdate(preset, null);
      }
   });

   mapDateInput.addEventListener('change', () => {
      if (mapPreset.value === 'specific-day') onUpdate('specific-day', currentDateStr());
   });

   if (includeOffDisplayCheckbox) {
      includeOffDisplayCheckbox.addEventListener('change', () => {
         refetch();
      });
   }

   if (includeSeasonalRestaurantsCheckbox) {
      includeSeasonalRestaurantsCheckbox.addEventListener('change', () => {
         refetch();
      });
   }

   if (includeSeasonalGiftShopsCheckbox) {
      includeSeasonalGiftShopsCheckbox.addEventListener('change', () => {
         refetch();
      });
   }

   if (includeClosedAttractionsCheckbox) {
      includeClosedAttractionsCheckbox.addEventListener('change', () => {
         refetch();
      });
   }

   if ( zoomobileRouteTypeRadios ) {
      Array.from(zoomobileRouteTypeRadios || []).forEach(r => r.addEventListener('change', () => {
         refetch();
      }));
   }
}