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
   const timeInput = document.createElement('input');
   const durationInput = document.createElement('input');
   let selectedStartTime = '';

   timeInput.className = 'schedule-item-time-input';
   timeInput.type = 'text';
   timeInput.placeholder = strings.timePlaceholder ?? '--:-- --';
   timeInput.autocomplete = 'off';

   durationInput.className = 'schedule-item-duration-input';
   durationInput.type = 'number';
   durationInput.min = '1';
   durationInput.step = '1';
   durationInput.placeholder = strings.durationPlaceholder ?? '';
   durationInput.disabled = true;
   durationInput.setAttribute('aria-disabled', 'true');

   function syncDurationFieldState() {
      const hasStartTime = Boolean(selectedStartTime);

      durationInput.disabled = !hasStartTime;
      durationInput.setAttribute('aria-disabled', String(!hasStartTime));

      if (!hasStartTime) {
         durationInput.value = '';
      }
   }

   function commitPickerTime(_selectedDates, dateStr, instance) {
      selectedStartTime = readPickerTimeValue(instance, dateStr, timeInput);
      timeInput.value = selectedStartTime;
      syncDurationFieldState();
   }

   timeField.append(
      createFieldLabel(strings.timeLabel ?? ''),
      timeInput
   );
   durationField.append(
      createFieldLabel(strings.durationLabel ?? ''),
      durationInput
   );

   initTimePicker(timeInput, {
      allowInput: false,
      onClose: commitPickerTime,
      onReady(_selectedDates, _dateStr, instance) {
         instance.calendarContainer.classList.add('schedule-item-time-picker');
      },
   });

   durationInput.addEventListener('input', () => {
      if (!selectedStartTime) {
         durationInput.value = '';
      }
   });

   return {
      fields: [timeField, durationField],
      getScheduleTimeOptions() {
         const durationMinutes = parseDurationMinutes(durationInput.value);

         return {
            startTime: selectedStartTime,
            durationMinutes,
         };
      },
      hasDurationWithoutTime() {
         return !selectedStartTime && parseDurationMinutes(durationInput.value) !== null;
      },
      reset() {
         selectedStartTime = '';
         timeInput.value = '';
         syncDurationFieldState();
      },
   };
}
