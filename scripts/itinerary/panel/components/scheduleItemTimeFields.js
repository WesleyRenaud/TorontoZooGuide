import { ConsoleDatePickers } from '../../../datePickers/consoleDatePickers.js';
import { el } from '../dom.js';
import { Format } from '../format.js';

function createFieldLabel(text) {
   return el('label', 'schedule-item-field-label', text);
}

function readPickerTimeValue(instance, dateStr, inputEl) {
   return Format.formatClockTime(dateStr || instance?.input?.value || inputEl.value || '');
}

export class ScheduleItemTimeFields {
   static makeScheduleItemTimeFields(strings = {}) {
      const timeField = el('div', 'schedule-item-field schedule-item-time-field');
      const durationField = el('div', 'schedule-item-field schedule-item-duration-field');
      const timeLabel = createFieldLabel(strings.timeLabel ?? '');
      const durationLabel = createFieldLabel(strings.durationLabel ?? '');
      const timeInput = document.createElement('input');
      const durationInput = document.createElement('input');
      let selectedStartTime = '';
      let areTimesLocked = false;
      let isDurationLocked = false;
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
         timeField.classList.toggle('is-disabled', areTimesLocked);
         timeLabel.classList.toggle('is-disabled', areTimesLocked);
      }

      function syncFixedDurationFieldPresentation() {
         durationField.classList.toggle('is-disabled', areTimesLocked || isDurationLocked);
         durationLabel.classList.toggle('is-disabled', areTimesLocked || isDurationLocked);
      }

      function syncTimeInputDisabledState() {
         const disabled = areTimesLocked;

         timeInput.disabled = disabled;
         timeInput.readOnly = disabled;
         timeInput.setAttribute('aria-disabled', String(disabled));
         flatpickrInstance?.set('clickOpens', !disabled);
      }

      function syncDurationFieldState() {
         const disabled = areTimesLocked || isDurationLocked;

         durationInput.disabled = disabled;
         durationInput.setAttribute('aria-disabled', String(disabled));
      }

      function commitPickerTime(_selectedDates, dateStr, instance) {
         if (areTimesLocked) {
            return;
         }

         const pickerInstance = instance ?? flatpickrInstance;

         selectedStartTime = readPickerTimeValue(pickerInstance, dateStr, timeInput);
         timeInput.value = selectedStartTime;
      }

      function resolveSelectedStartTime() {
         if (areTimesLocked) {
            return '';
         }

         return selectedStartTime || readPickerTimeValue(flatpickrInstance, '', timeInput);
      }

      timeField.append(timeLabel, timeInput);
      durationField.append(durationLabel, durationInput);
      syncDurationFieldState();
      syncFixedDurationFieldPresentation();

      ConsoleDatePickers.initTimePicker(timeInput, {
         allowInput: false,
         onChange: commitPickerTime,
         onClose: commitPickerTime,
         onReady(_selectedDates, _dateStr, instance) {
            flatpickrInstance = instance;
            instance.calendarContainer.classList.add('schedule-item-time-picker');
            syncTimeInputDisabledState();
         },
      });

      function setFixedTimeScheduleMode({ lockTimes = false } = {}) {
         areTimesLocked = lockTimes;

         if (lockTimes) {
            isDurationLocked = false;
         }

         clearTimeFieldValues();
         syncTimeInputDisabledState();
         syncDurationFieldState();
         syncFixedTimeFieldPresentation();
         syncFixedDurationFieldPresentation();
      }

      function setFixedDurationScheduleMode({
         lockDuration = false,
         durationMinutes = null,
      } = {}) {
         isDurationLocked = lockDuration;

         if (lockDuration) {
            areTimesLocked = false;
            durationInput.value = durationMinutes != null
               ? String(durationMinutes)
               : '';
         }
         else {
            durationInput.value = '';
         }

         syncTimeInputDisabledState();
         syncDurationFieldState();
         syncFixedTimeFieldPresentation();
         syncFixedDurationFieldPresentation();
      }

      return {
         fields: [timeField, durationField],
         getScheduleTimeOptions() {
            if (areTimesLocked || isDurationLocked) {
               return {
                  startTime: areTimesLocked ? '' : resolveSelectedStartTime(),
                  durationMinutes: null,
               };
            }

            const startTime = resolveSelectedStartTime();
            const durationMinutes = Format.parseDurationMinutes(durationInput.value);

            return {
               startTime,
               durationMinutes,
            };
         },
         reset() {
            setFixedTimeScheduleMode({ lockTimes: false });
            setFixedDurationScheduleMode({ lockDuration: false });
         },
         setFixedDurationScheduleMode,
         setFixedTimeScheduleMode,
      };
   }
}
