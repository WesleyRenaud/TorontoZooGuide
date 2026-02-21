export function initMapControls({ mapPreset, mapDateInput, includeOffDisplayCheckbox, includeSeasonalRestaurantsCheckbox, onUpdate }) {
   if (!mapPreset || !mapDateInput || !onUpdate) {
      console.warn('[controls] missing elements:', { mapPreset, mapDateInput, onUpdate });
      return;
   }

   // Try to init flatpickr, but never let it break controls
   let fp = null;
   try {
      const fpFn = window.flatpickr; // important: read from window
      if (typeof fpFn === 'function') {
         fp = fpFn(mapDateInput, {
            defaultDate: new Date(),
            dateFormat: 'Y-m-d',
            allowInput: true,
            clickOpens: true,
            minDate: 'today',
            monthSelectorType: 'static',
            onChange: (_, dateStr) => {
               if (mapPreset.value === 'specific-day') onUpdate('specific-day', dateStr);
            },
         });
      } else {
         console.warn('[controls] window.flatpickr not available; using plain input');
      }
   } catch (err) {
      console.error('[controls] flatpickr init failed; using plain input', err);
   }

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

   // If you don't have flatpickr, this still updates on manual typing/choosing a date
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
}