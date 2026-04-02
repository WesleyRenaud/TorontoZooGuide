import { DATE_KEY } from '../../pages/itineraryWizard/keys.js';
import { initVisitDateFlatpickr } from '../../shared/visitDateFlatpickr.js';
import {
   DEFAULT_DAYS_AHEAD,
   toISODate,
   getToday,
   getMaxDate,
   normalizeDate,
   isBeforeToday,
   isAfterMaxDate,
   clampToAllowedVisitDate,
} from '../../shared/visitDateRules.js';

function formatLong(d) {
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
      if (isAfterMaxDate(normalized, DEFAULT_DAYS_AHEAD)) return;

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
      if (isAfterMaxDate(currentDate, DEFAULT_DAYS_AHEAD)) return null;

      setDate(currentDate, { persist: true, updateInput: true });

      return {
         date: toISODate(currentDate),
         dateObj: currentDate,
      };
   }

   function closePicker() {
      fp?.close();
      inputEl?.blur();
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
               <input
                  class="itin-date-input"
                  type="text"
                  inputmode="none"
                  autocomplete="off"
                  readonly
               />
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
         closePicker();
         onSave?.(saved.date, saved.dateObj);
      });

      root.querySelector('.itin-finish')?.addEventListener('click', () => {
         const saved = persistCurrentDate();
         if (!saved) return;
         closePicker();
         onFinish?.(saved.date, saved.dateObj);
      });

      root.querySelector('.itin-close')?.addEventListener('click', () => {
         closePicker();
         onClose?.();
      });

      fp = initVisitDateFlatpickr(inputEl, {
         defaultDate: currentDate || getToday(),
         clickOpens: true,
         onReady: (safeDate, _isoDate, instance) => {
            setDate(safeDate, { updateInput: true, persist: false });
            instance.input.value = formatLong(safeDate);
         },
         onChange: (safeDate, _isoDate, instance) => {
            setDate(safeDate, { updateInput: true, persist: false });
            instance.input.value = formatLong(safeDate);
            instance.close();
            inputEl?.blur();
         },
         onClose: () => {
            inputEl?.blur();
         }
      });
   }

   function show() {
      if (!mountEl) return;

      if (!root) {
         build();
      }

      const saved = getSavedDate();
      const today = getToday();
      const maxDate = getMaxDate(DEFAULT_DAYS_AHEAD);
      const selected = initialDate || saved || today;

      const safeDate = clampToAllowedVisitDate(
         selected,
         DEFAULT_DAYS_AHEAD
      );

      setDate(safeDate, { updateInput: true, persist: false });

      if (fp && currentDate) {
         fp.set('minDate', today);
         fp.set('maxDate', maxDate);
         fp.setDate(currentDate, false);
         inputEl.value = formatLong(currentDate);
         closePicker();
      }

      mountEl.innerHTML = '';
      mountEl.appendChild(root);
   }

   function hide() {
      closePicker();

      if (!mountEl) return;
      mountEl.innerHTML = '';
   }

   function getDate() {
      return currentDate;
   }

   return { show, hide, getDate, setDate };
}