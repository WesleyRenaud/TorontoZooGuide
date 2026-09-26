import { DateSelectionModel } from './dateSelectionModel.js';
import { DateSelectorPickerBinder } from './dateSelectorPickerBinder.js';
import { DateSelectorTimeFields } from './dateSelectorTimeFields.js';
import { DateSelectorView } from './dateSelectorView.js';
import { ItineraryService } from '../itineraryService.js';
import { ItineraryTimeView } from '../panel/components/itineraryTimeView.js';
import { Strings } from '../../strings.js';
import { VisitDateValidator } from '../../visitDates/visitDateValidator.js';

export class DateSelector {
   static createItineraryDateSelectorController({
   mountEl,
   initialDate = null,
   initialArrivalTime = null,
   initialDepartureTime = null,
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
         buildView = DateSelectorView.buildDateSelectorView,
         createPicker = DateSelectorPickerBinder.createDatePickerBinding,
         getTodayFn = VisitDateValidator.getToday,
         getZooHoursFn = ItineraryService.getZooHours,
         makeTimeInput = ItineraryTimeView.makeItineraryTimeInput,
      } = deps;

      let elements = null;
      let picker = null;
      let arrivalTime = initialArrivalTime;
      let departureTime = initialDepartureTime;
      let zooHours = null;

      const earliestFloor = earliestSelectableDate ?? getTodayFn();

      function syncInputValue(date = model.getDate()) {
         if (!elements?.inputEl || !date) {
            return;
         }

         elements.inputEl.value = DateSelectionModel.formatVisitDateLong(date);
      }

      function mountTimeFields() {
         DateSelectorTimeFields.mount({
            containerEl: elements?.timesMountEl,
            arrivalTime,
            departureTime,
            zooHours,
            strings: Strings,
            makeTimeInput,
            onArrivalTimeChange: (nextArrivalTime) => {
               arrivalTime = nextArrivalTime;
            },
            onDepartureTimeChange: (nextDepartureTime) => {
               departureTime = nextDepartureTime;
            },
            getArrivalTime: () => arrivalTime,
            getDepartureTime: () => departureTime,
         });
      }

      async function refreshTimeFields(date) {
         if (!elements?.timesMountEl) {
            return;
         }

         const nextZooHours = await getZooHoursFn(VisitDateValidator.toISODate(date));

         if (date.getTime() !== model.getDate().getTime()) {
            return;
         }

         zooHours = nextZooHours;
         mountTimeFields();
      }

      const model = DateSelectionModel.createDateSelectionModel({
         initialDate,
         syncInputValue,
         onDateChanged: (date) => {
            void refreshTimeFields(date);
         },
         earliestDateFloor: earliestFloor,
         getTodayFn,
      });

      function commitDateSelection(callback) {
         const saved = model.persistCurrentDate();

         if (!saved) {
            return;
         }

         if (!DateSelectorTimeFields.areVisitTimesValid(
            arrivalTime,
            departureTime,
            zooHours
         )) {
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

         elements = buildView(Strings);

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

         ensureView();
         model.setDate(model.getDisplayDate(), { updateInput: false, persist: false });
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
         getArrivalTime: () => arrivalTime,
         getDepartureTime: () => departureTime,
      };
   }
}
