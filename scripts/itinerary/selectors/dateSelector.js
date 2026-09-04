import {
   createDateSelectionModel,
   formatVisitDateLong,
} from './dateSelectionModel.js';
import { createDatePickerBinding } from './dateSelectorPickerBinding.js';
import { buildDateSelectorView } from './dateSelectorView.js';
import { APP_STRINGS } from '../../strings.js';
import { VisitDateRules } from '../../visitDates/visitDateRules.js';

export function createItineraryDateSelectorController({
   mountEl,
   initialDate = null,
   earliestSelectableDate = null,
   hideNextButton = false,
   titleText = null,
   subtitleText = null,
   onSave,
   onFinish,
   onClose,
   deps = {},
} = {}) {
   const {
      buildView = buildDateSelectorView,
      createPicker = createDatePickerBinding,
      getTodayFn = VisitDateRules.getToday,
   } = deps;

   let elements = null;
   let picker = null;

   const earliestFloor = earliestSelectableDate ?? getTodayFn();

   function syncInputValue(date = model.getDate()) {
      if (!elements?.inputEl) {
         return;
      }

      elements.inputEl.value = date ? formatVisitDateLong(date) : '';
   }

   const model = createDateSelectionModel({
      initialDate,
      syncInputValue,
      earliestDateFloor: earliestFloor,
      getTodayFn,
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

      elements = buildView(APP_STRINGS);

      if (titleText && elements.root) {
         elements.root.querySelector('.itin-h1').textContent = titleText;
      }

      if (subtitleText && elements.root) {
         elements.root.querySelector('.itin-subtitle').textContent = subtitleText;
      }

      bindDomEvents();
      picker = createPicker({
         inputEl: elements.inputEl,
         getDate: model.getDate,
         setDate: model.setDate,
         syncInputValue,
         earliestDateFloor: earliestFloor,
         getTodayFn,
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

      if (elements.nextButtonEl) {
         elements.nextButtonEl.hidden = hideNextButton;
      }

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
