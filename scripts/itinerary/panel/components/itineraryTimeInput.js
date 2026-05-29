import { initTimePicker } from '../../../datePickers/consoleDatePickers.js';
import { el } from '../dom.js';
import { formatClockTime } from '../format.js';
import { createValidationBubbleController } from '../../../validationBubble.js';

function readPickerTimeValue(instance, dateStr, inputEl) {
   return formatClockTime(dateStr || instance?.input?.value || inputEl.value || '');
}

export function makeItineraryTimeInput({
   label,
   value = '',
   onChange = null,
   timePickerOptions = {},
   validateTime = null,
   resolveInvalidMessage = null,
   invalidMessage = '',
}) {
   const field = el('label', 'itinerary-day-time-control');
   const labelText = el('span', 'itinerary-day-time-control-label', label);
   const form = el('form', 'itinerary-day-time-form');
   const inputWrap = el('div', 'itinerary-day-time-input-wrap');
   const input = el('input', 'itinerary-day-time-input');
   const validationBubble = createValidationBubbleController({
      anchorEl: inputWrap,
   });
   let committedValue = value ? formatClockTime(value) : '';
   let flatpickrInstance = null;
   let latestPickerValue = committedValue;

   function syncPickerToCommittedValue() {
      if (!flatpickrInstance) {
         return;
      }

      if (committedValue) {
         flatpickrInstance.setDate(committedValue, false);
         return;
      }

      flatpickrInstance.clear(false);
   }

   function rejectInvalidTime(nextValue) {
      input.value = committedValue;
      latestPickerValue = committedValue;
      syncPickerToCommittedValue();
      requestAnimationFrame(() => {
         validationBubble.show(
            resolveInvalidMessage?.(nextValue) ?? invalidMessage
         );
      });
   }

   async function saveSelectedTime(_selectedDates, dateStr, instance) {
      if (instance) {
         flatpickrInstance = instance;
      }

      const nextValue = readPickerTimeValue(instance, dateStr, input)
         || latestPickerValue;

      if (nextValue === committedValue) {
         validationBubble.dismiss();
         return;
      }

      if (validateTime && !validateTime(nextValue)) {
         rejectInvalidTime(nextValue);
         return;
      }

      try {
         input.disabled = true;
         validationBubble.dismiss();
         await onChange?.(nextValue || null);
         committedValue = nextValue;
         latestPickerValue = nextValue;
      }
      catch (error) {
         console.error('Failed to update itinerary time:', error);
         rejectInvalidTime(nextValue);
      }
      finally {
         input.disabled = !onChange;
      }
   }

   input.type = 'text';
   input.value = committedValue;
   input.placeholder = '--:-- --';
   input.disabled = !onChange;
   form.noValidate = true;
   form.addEventListener('submit', (event) => {
      event.preventDefault();
   });
   field.append(labelText, form);
   form.appendChild(inputWrap);
   inputWrap.appendChild(input);
   flatpickrInstance = initTimePicker(input, {
      allowInput: false,
      onChange(_selectedDates, dateStr, instance) {
         latestPickerValue = readPickerTimeValue(instance, dateStr, input);
      },
      onOpen: () => {
         validationBubble.dismiss();
      },
      onClose: saveSelectedTime,
      onReady(_selectedDates, _dateStr, instance) {
         flatpickrInstance = instance;
         instance.calendarContainer.classList.add('itinerary-day-time-picker');
      },
      ...timePickerOptions,
   });

   return field;
}
