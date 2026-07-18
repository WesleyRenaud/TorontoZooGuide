import { initTimePicker } from '../../../datePickers/consoleDatePickers.js';
import { el } from '../dom.js';
import {
   formatClockTime,
   parseDurationMinutes,
} from '../format.js';

function createFieldLabel(text) {
   return el('label', 'schedule-item-field-label', text);
}

function readPickerTimeValue(instance, dateStr, inputEl) {
   return formatClockTime(dateStr || instance?.input?.value || inputEl.value || '');
}

export function makeScheduleItemTimeFields(strings = {}) {
   const timeField = el('div', 'schedule-item-field schedule-item-time-field');
   const durationField = el('div', 'schedule-item-field schedule-item-duration-field');
   const timeLabel = createFieldLabel(strings.timeLabel ?? '');
   const durationLabel = createFieldLabel(strings.durationLabel ?? '');
   const timeInput = document.createElement('input');
   const durationInput = document.createElement('input');
   let selectedStartTime = '';
   let isFixedTimeMode = false;
   let flatpickrInstance = null;

   timeInput.className = 'schedule-item-time-input';
   timeInput.type = 'text';
   timeInput.placeholder = strings.timePlaceholder ?? '--:-- --';
   timeInput.autocomplete = 'off';

   durationInput.className = 'schedule-item-duration-input';
   durationInput.type = 'number';
   durationInput.min = '1';
   durationInput.step = '1';
   durationInput.placeholder = strings.durationPlaceholder ?? '';

   function clearTimeFieldValues() {
      selectedStartTime = '';
      timeInput.value = '';
      durationInput.value = '';
      flatpickrInstance?.clear();
   }

   function syncFixedTimeFieldPresentation() {
      timeField.classList.toggle('is-disabled', isFixedTimeMode);
      durationField.classList.toggle('is-disabled', isFixedTimeMode);
      timeLabel.classList.toggle('is-disabled', isFixedTimeMode);
      durationLabel.classList.toggle('is-disabled', isFixedTimeMode);
   }

   function syncTimeInputDisabledState() {
      const disabled = isFixedTimeMode;

      timeInput.disabled = disabled;
      timeInput.readOnly = disabled;
      timeInput.setAttribute('aria-disabled', String(disabled));
      flatpickrInstance?.set('clickOpens', !disabled);
   }

   function syncDurationFieldState() {
      const disabled = isFixedTimeMode;

      durationInput.disabled = disabled;
      durationInput.setAttribute('aria-disabled', String(disabled));
   }

   function commitPickerTime(_selectedDates, dateStr, instance) {
      if (isFixedTimeMode) {
         return;
      }

      const pickerInstance = instance ?? flatpickrInstance;

      selectedStartTime = readPickerTimeValue(pickerInstance, dateStr, timeInput);
      timeInput.value = selectedStartTime;
   }

   function resolveSelectedStartTime() {
      if (isFixedTimeMode) {
         return '';
      }

      return selectedStartTime || readPickerTimeValue(flatpickrInstance, '', timeInput);
   }

   timeField.append(timeLabel, timeInput);
   durationField.append(durationLabel, durationInput);
   syncDurationFieldState();

   initTimePicker(timeInput, {
      allowInput: false,
      onChange: commitPickerTime,
      onClose: commitPickerTime,
      onReady(_selectedDates, _dateStr, instance) {
         flatpickrInstance = instance;
         instance.calendarContainer.classList.add('schedule-item-time-picker');
         syncTimeInputDisabledState();
      },
   });

   function setFixedTimeScheduleMode({ enabled = false } = {}) {
      isFixedTimeMode = enabled;
      clearTimeFieldValues();
      syncTimeInputDisabledState();
      syncDurationFieldState();
      syncFixedTimeFieldPresentation();
   }

   return {
      fields: [timeField, durationField],
      getScheduleTimeOptions() {
         if (isFixedTimeMode) {
            return {
               startTime: '',
               durationMinutes: null,
            };
         }

         const startTime = resolveSelectedStartTime();
         const durationMinutes = parseDurationMinutes(durationInput.value);

         return {
            startTime,
            durationMinutes,
         };
      },
      reset() {
         setFixedTimeScheduleMode({ enabled: false });
      },
      setFixedTimeScheduleMode,
   };
}
