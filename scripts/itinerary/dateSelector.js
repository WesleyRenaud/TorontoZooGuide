// scripts/itinerary/dateSelector.js
const STORAGE_KEY = 'tzg.itineraryDateISO';

function toISODate(d) {
   // YYYY-MM-DD in local time
   const y = d.getFullYear();
   const m = String(d.getMonth() + 1).padStart(2, '0');
   const day = String(d.getDate()).padStart(2, '0');
   return `${y}-${m}-${day}`;
}

function formatLong(d) {
   // e.g. Sunday, March 1, 2026
   return d.toLocaleDateString(undefined, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
   });
}

export function createItineraryDateSelectorController({
   mountEl,
   initialDate = null,
   onSave,
   onFinish,
   onCancel,
} = {}) {
   let root = null;
   let inputEl = null;
   let fp = null;
   let currentDate = null;

   function getSavedDate() {
      const iso = localStorage.getItem(STORAGE_KEY);
      if (!iso) return null;
      const d = new Date(`${iso}T12:00:00`);
      return Number.isFinite(d.getTime()) ? d : null;
   }

   function setDate(d, { updateInput = true, persist = false } = {}) {
      if (!d || !Number.isFinite(d.getTime())) return;
      currentDate = d;

      if (updateInput && inputEl) inputEl.value = formatLong(d);

      if (persist) localStorage.setItem(STORAGE_KEY, toISODate(d));
   }

   function persistCurrentDate() {
      if (!currentDate) return null;
      setDate(currentDate, { persist: true, updateInput: true });
      return { iso: toISODate(currentDate), dateObj: currentDate };
   }

   function build() {
      root = document.createElement('div');
      root.className = 'itin-overlay';
      root.innerHTML = `
         <section class="itin-card" role="dialog" aria-modal="true" aria-label="Itinerary Builder">
            <div class="itin-card-topbar">
               <div class="itin-top-title">Itinerary Builder</div>
            </div>

            <div class="itin-card-body">
               <h1 class="itin-h1">Set Visit Date</h1>
               <p class="itin-subtitle">Choose the date for your visit.</p>

               <div class="itin-field-label">Visit Date</div>
               <input class="itin-date-input" type="text" inputmode="none" autocomplete="off" />
            </div>

            <div class="itin-card-actions">
               <div class="itin-actions-right">
                  <button class="itin-next" type="button">Next</button>
                  <button class="itin-next itin-finish" type="button">Finish</button>
               </div>
            </div>
         </section>
      `;

      inputEl = root.querySelector('.itin-date-input');

      root.querySelector('.itin-next')?.addEventListener('click', () => {
         const saved = persistCurrentDate();
         if (!saved) return;
         onSave?.(saved.iso, saved.dateObj);
      });

      root.querySelector('.itin-finish')?.addEventListener('click', () => {
         const saved = persistCurrentDate();
         if (!saved) return;
         onFinish?.(saved.iso, saved.dateObj);
      });

      fp = flatpickr(inputEl, {
         allowInput: false,
         dateFormat: 'Y-m-d',
         monthSelectorType: 'static',
         defaultDate: currentDate || new Date(),
         onReady: (_sel, _str, instance) => {
            const d = instance.selectedDates?.[0] || new Date();
            setDate(d, { updateInput: true, persist: false });
         },
         onChange: (selectedDates) => {
            const d = selectedDates?.[0];
            if (d) setDate(d, { updateInput: true, persist: false });
         },
      });

      inputEl.addEventListener('click', () => fp?.open());
   }

   function show() {
      if (!mountEl) return;

      if (!root) {
         build();
      }

      const saved = getSavedDate();
      setDate(initialDate || saved || new Date(), { updateInput: true, persist: false });

      if (fp && currentDate) fp.setDate(currentDate, true);

      mountEl.innerHTML = '';
      mountEl.appendChild(root);
   }

   function hide() {
      if (!mountEl) return;
      mountEl.innerHTML = '';
   }

   function getDate() {
      return currentDate;
   }

   return { show, hide, getDate, setDate };
}