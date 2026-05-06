import {
   getStoredItineraryDate,
   setStoredItineraryDate,
} from '../draftStorage.js';
import { APP_STRINGS } from '../../strings.js';
import { initVisitDateFlatpickr } from '../../visitDates/visitDateFlatpickr.js';
import {
   DEFAULT_DAYS_AHEAD,
   toISODate,
   getToday,
   getMaxDate,
   normalizeDate,
   isBeforeToday,
   isAfterMaxDate,
   clampToAllowedVisitDate,
} from '../../visitDates/visitDateRules.js';

function formatLong(d) {
   return d.toLocaleDateString(undefined, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
   });
}

function readSavedDateFromStorage() {
   const iso = getStoredItineraryDate();

   if (!iso) {
      return null;
   }

   const savedDate = new Date(`${iso}T12:00:00`);
   return Number.isFinite(savedDate.getTime()) ? savedDate : null;
}

function isSelectableVisitDate(date) {
   if (!date) {
      return false;
   }

   if (isBeforeToday(date)) {
      return false;
   }

   if (isAfterMaxDate(date, DEFAULT_DAYS_AHEAD)) {
      return false;
   }

   return true;
}

function createDateSelectionModel({
   initialDate = null,
   syncInputValue = () => {},
} = {}) {
   let currentDate = null;

   function persistDate(date) {
      setStoredItineraryDate(toISODate(date));
   }

   function setDate(date, { updateInput = true, persist = false } = {}) {
      const normalized = normalizeDate(date);

      if (!isSelectableVisitDate(normalized)) {
         return false;
      }

      currentDate = normalized;

      if (updateInput) {
         syncInputValue(normalized);
      }

      if (persist) {
         persistDate(normalized);
      }

      return true;
   }

   function buildCurrentDatePayload() {
      if (!isSelectableVisitDate(currentDate)) {
         return null;
      }

      return {
         date: toISODate(currentDate),
         dateObj: currentDate,
      };
   }

   function persistCurrentDate() {
      if (!setDate(currentDate, { persist: true, updateInput: true })) {
         return null;
      }

      return buildCurrentDatePayload();
   }

   function getDisplayDate() {
      const savedDate = readSavedDateFromStorage();
      const selectedDate = initialDate || savedDate || getToday();

      return clampToAllowedVisitDate(selectedDate, DEFAULT_DAYS_AHEAD);
   }

   function getDate() {
      return currentDate;
   }

   return {
      getDate,
      setDate,
      persistCurrentDate,
      getDisplayDate,
   };
}

function createButton({
   className,
   text,
   ariaLabel = null,
} = {}) {
   const button = document.createElement('button');
   button.className = className;
   button.type = 'button';
   button.textContent = text;

   if (ariaLabel) {
      button.setAttribute('aria-label', ariaLabel);
   }

   return button;
}

function buildDateSelectorView() {
   const root = document.createElement('div');
   root.className = 'itin-overlay';

   const card = document.createElement('section');
   card.className = 'itin-card';
   card.setAttribute('role', 'dialog');
   card.setAttribute('aria-modal', 'true');
   card.setAttribute('aria-label', APP_STRINGS.itinerary.selectors.builderTitle);

   const topbar = document.createElement('div');
   topbar.className = 'itin-card-topbar itin-card-topbar-with-close';

   const topTitle = document.createElement('div');
   topTitle.className = 'itin-top-title';
   topTitle.textContent = APP_STRINGS.itinerary.selectors.builderTitle;

   const closeButtonEl = createButton({
      className: 'itin-close',
      text: APP_STRINGS.common.closeSymbol,
      ariaLabel: APP_STRINGS.itinerary.aria.closeBuilder,
   });

   topbar.append(topTitle, closeButtonEl);

   const body = document.createElement('div');
   body.className = 'itin-card-body';

   const heading = document.createElement('h1');
   heading.className = 'itin-h1';
   heading.textContent = APP_STRINGS.itinerary.selectors.titleDate;

   const subtitle = document.createElement('p');
   subtitle.className = 'itin-subtitle';
   subtitle.textContent = APP_STRINGS.itinerary.selectors.visitDateSubtitle;

   const fieldLabel = document.createElement('div');
   fieldLabel.className = 'itin-field-label';
   fieldLabel.textContent = APP_STRINGS.itinerary.selectors.visitDate;

   const inputEl = document.createElement('input');
   inputEl.className = 'itin-date-input';
   inputEl.type = 'text';
   inputEl.inputMode = 'none';
   inputEl.autocomplete = 'off';
   inputEl.readOnly = true;

   body.append(heading, subtitle, fieldLabel, inputEl);

   const actions = document.createElement('div');
   actions.className = 'itin-card-actions';

   const actionsRight = document.createElement('div');
   actionsRight.className = 'itin-actions-right';

   const nextButtonEl = createButton({
      className: 'itin-next',
      text: APP_STRINGS.itinerary.actions.next,
   });

   const finishButtonEl = createButton({
      className: 'itin-next itin-finish',
      text: APP_STRINGS.itinerary.actions.finish,
   });

   actionsRight.append(nextButtonEl, finishButtonEl);
   actions.append(actionsRight);
   card.append(topbar, body, actions);
   root.appendChild(card);

   return {
      root,
      inputEl,
      nextButtonEl,
      finishButtonEl,
      closeButtonEl,
   };
}

function createDatePickerBinding({
   inputEl,
   getDate,
   setDate,
   syncInputValue,
} = {}) {
   let flatpickrInstance = null;

   function applyPickerDate(date, instance) {
      setDate(date, { updateInput: true, persist: false });
      instance.input.value = formatLong(date);
   }

   function close() {
      flatpickrInstance?.close();
      inputEl?.blur();
   }

   function syncBounds() {
      const currentDate = getDate();

      if (!flatpickrInstance || !currentDate) {
         return;
      }

      flatpickrInstance.set('minDate', getToday());
      flatpickrInstance.set('maxDate', getMaxDate(DEFAULT_DAYS_AHEAD));
      flatpickrInstance.setDate(currentDate, false);
      syncInputValue(currentDate);
      close();
   }

   function init() {
      flatpickrInstance = initVisitDateFlatpickr(inputEl, {
         defaultDate: getDate() || getToday(),
         clickOpens: true,
         onReady: (safeDate, _isoDate, instance) => {
            applyPickerDate(safeDate, instance);
         },
         onChange: (safeDate, _isoDate, instance) => {
            applyPickerDate(safeDate, instance);
            instance.close();
            inputEl?.blur();
         },
         onClose: () => {
            inputEl?.blur();
         },
      });
   }

   return {
      init,
      close,
      syncBounds,
   };
}

export function createItineraryDateSelectorController({
   mountEl,
   initialDate = null,
   onSave,
   onFinish,
   onClose,
} = {}) {
   let elements = null;
   let picker = null;

   function syncInputValue(date = model.getDate()) {
      if (!elements?.inputEl) {
         return;
      }

      elements.inputEl.value = date ? formatLong(date) : '';
   }

   const model = createDateSelectionModel({
      initialDate,
      syncInputValue,
   });

   function commitDateSelection(callback) {
      const saved = model.persistCurrentDate();

      if (!saved) {
         return;
      }

      picker?.close();
      callback?.(saved.date, saved.dateObj);
   }

   function bindDomEvents() {
      elements?.nextButtonEl?.addEventListener('click', () => {
         commitDateSelection(onSave);
      });

      elements?.finishButtonEl?.addEventListener('click', () => {
         commitDateSelection(onFinish);
      });

      elements?.closeButtonEl?.addEventListener('click', () => {
         picker?.close();
         onClose?.();
      });
   }

   function ensureView() {
      if (elements) {
         return;
      }

      elements = buildDateSelectorView();
      bindDomEvents();
      picker = createDatePickerBinding({
         inputEl: elements.inputEl,
         getDate: model.getDate,
         setDate: model.setDate,
         syncInputValue,
      });
      picker.init();
   }

   function show() {
      if (!mountEl) {
         return;
      }

      model.setDate(model.getDisplayDate(), { updateInput: false, persist: false });
      ensureView();
      syncInputValue();
      picker?.syncBounds();

      mountEl.replaceChildren(elements.root);
   }

   function hide() {
      picker?.close();

      if (!mountEl) {
         return;
      }

      mountEl.replaceChildren();
   }

   return {
      show,
      hide,
      getDate: model.getDate,
      setDate: model.setDate,
   };
}
