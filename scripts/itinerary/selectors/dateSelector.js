import { DATE_KEY } from '../../pages/itineraryWizard/keys.js';

function toISODate(d) {
   const y = d.getFullYear();
   const m = String(d.getMonth() + 1).padStart(2, '0');
   const day = String(d.getDate()).padStart(2, '0');
   return `${y}-${m}-${day}`;
}

function formatLong(d) {
   return d.toLocaleDateString(undefined, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
   });
}

function getToday() {
   const today = new Date();
   return new Date(today.getFullYear(), today.getMonth(), today.getDate(), 12, 0, 0, 0);
}

function getMaxDate(daysAhead = 90) {
   const today = getToday();
   const max = new Date(today);
   max.setDate(today.getDate() + daysAhead);
   return max;
}

function normalizeDate(d) {
   if (!d || !Number.isFinite(d.getTime())) return null;
   return new Date(d.getFullYear(), d.getMonth(), d.getDate(), 12, 0, 0, 0);
}

function isBeforeToday(d) {
   const candidate = normalizeDate(d);
   if (!candidate) return false;
   return candidate < getToday();
}

function isAfterMaxDate(d, daysAhead = 90) {
   const candidate = normalizeDate(d);
   if (!candidate) return false;
   return candidate > getMaxDate(daysAhead);
}

export function createItineraryDateSelectorController({
   mountEl,
   initialDate = null,
   onSave,
   onFinish,
   onCancel,
   onClose,
} = {}) {
   let root = null;
   let inputEl = null;
   let fp = null;
   let currentDate = null;

   function getSavedDate() {
      const iso = localStorage.getItem(DATE_KEY);
      if (!iso) return null;
      const d = new Date(`${iso}T12:00:00`);
      return Number.isFinite(d.getTime()) ? d : null;
   }

   function setDate(d, { updateInput = true, persist = false } = {}) {
      const normalized = normalizeDate(d);
      if (!normalized) return;
      if (isBeforeToday(normalized)) return;
      if (isAfterMaxDate(normalized, 90)) return;

      currentDate = normalized;

      if (updateInput && inputEl) {
         inputEl.value = formatLong(normalized);
      }

      if (persist) {
         localStorage.setItem(DATE_KEY, toISODate(normalized));
      }
   }

   function persistCurrentDate() {
      if (!currentDate) return null;
      if (isBeforeToday(currentDate)) return null;
      if (isAfterMaxDate(currentDate, 90)) return null;

      setDate(currentDate, { persist: true, updateInput: true });

      return {
         date: toISODate(currentDate),
         dateObj: currentDate,
      };
   }

   function build() {
      root = document.createElement('div');
      root.className = 'itin-overlay';
      root.innerHTML = `
         <section class="itin-card" role="dialog" aria-modal="true" aria-label="Itinerary Builder">
            <div class="itin-card-topbar itin-card-topbar-with-close">
               <div class="itin-top-title">Itinerary Builder</div>
               <button class="itin-close" type="button" aria-label="Close itinerary builder">×</button>
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
         onSave?.(saved.date, saved.dateObj);
      });

      root.querySelector('.itin-finish')?.addEventListener('click', () => {
         const saved = persistCurrentDate();
         if (!saved) return;
         onFinish?.(saved.date, saved.dateObj);
      });

      root.querySelector('.itin-close')?.addEventListener('click', () => {
         onClose?.();
      });

      fp = flatpickr(inputEl, {
         allowInput: false,
         dateFormat: 'Y-m-d',
         monthSelectorType: 'static',
         minDate: getToday(),
         maxDate: getMaxDate(90),
         defaultDate: currentDate || getToday(),
         onReady: (_sel, _str, instance) => {
            const d = instance.selectedDates?.[0] || getToday();
            setDate(d, { updateInput: true, persist: false });
         },
         onChange: selectedDates => {
            const d = selectedDates?.[0];
            if (d) {
               setDate(d, { updateInput: true, persist: false });
            }
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
      const today = getToday();
      const maxDate = getMaxDate(90);
      const selected = initialDate || saved || today;

      let safeDate = normalizeDate(selected) || today;

      if (isBeforeToday(safeDate)) {
         safeDate = today;
      }

      if (isAfterMaxDate(safeDate, 90)) {
         safeDate = maxDate;
      }

      setDate(safeDate, { updateInput: true, persist: false });

      if (fp && currentDate) {
         fp.set('minDate', today);
         fp.set('maxDate', maxDate);
         fp.setDate(currentDate, true);
      }

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