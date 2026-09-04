import { ConsoleDatePickers } from '../../../datePickers/consoleDatePickers.js';
import { el } from '../dom.js';
import { Format } from '../format.js';
import { common } from '../../../strings/common.js';
import { createValidationBubbleController } from '../../../validationBubble.js';

function readPickerTimeValue(instance, dateStr, inputEl) {
   return Format.formatClockTime(dateStr || instance?.input?.value || inputEl.value || '');
}

export function makeItineraryTimeInput({
   label,
   value = '',
   onChange = null,
   clearAriaLabel = '',
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
   let committedValue = value ? Format.formatClockTime(value) : '';
   let flatpickrInstance = null;
   let latestPickerValue = committedValue;
   let suppressNextCloseSave = false;
   let outsidePointerDownHandler = null;
   const clearButton = document.createElement('button');

   clearButton.type = 'button';
   clearButton.className = 'itinerary-day-time-clear-btn';
   clearButton.setAttribute('aria-label', clearAriaLabel);
   clearButton.textContent = common.closeSymbol;
   clearButton.hidden = !onChange;

   function syncClearButtonState() {
      if (!onChange) {
         clearButton.hidden = true;
         clearButton.disabled = true;
         return;
      }

      clearButton.hidden = false;
      clearButton.disabled = !committedValue;
   }

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
         syncClearButtonState();
      }
      catch (error) {
         if (error?.name !== 'ItineraryTimeChangeCancelledError') {
            console.error('Failed to update itinerary time:', error);
         }

         rejectInvalidTime(nextValue);
      }
      finally {
         input.disabled = !onChange;
      }
   }

   async function clearCommittedTime() {
      if (!committedValue || !onChange) {
         return;
      }

      input.disabled = true;
      validationBubble.dismiss();
      await onChange('');
      committedValue = '';
      latestPickerValue = '';
      input.value = '';
      syncPickerToCommittedValue();
      syncClearButtonState();
      input.disabled = !onChange;
   }

   function isPickerTarget(target) {
      return (
         field.contains?.(target)
         || flatpickrInstance?.calendarContainer?.contains?.(target)
      );
   }

   function commitPickerValueAfterOutsideClick() {
      requestAnimationFrame(() => {
         if (flatpickrInstance?.isOpen) {
            suppressNextCloseSave = true;
            flatpickrInstance.close();
         }

         saveSelectedTime(null, '', flatpickrInstance);
      });
   }

   function unbindOutsidePointerDown() {
      if (!outsidePointerDownHandler) {
         return;
      }

      document.removeEventListener(
         'mousedown',
         outsidePointerDownHandler,
         true
      );
      outsidePointerDownHandler = null;
   }

   function bindOutsidePointerDown() {
      unbindOutsidePointerDown();
      outsidePointerDownHandler = (event) => {
         if (isPickerTarget(event.target)) {
            return;
         }

         commitPickerValueAfterOutsideClick();
      };

      document.addEventListener('mousedown', outsidePointerDownHandler, true);
   }

   function handlePickerClose(selectedDates, dateStr, instance) {
      unbindOutsidePointerDown();

      if (suppressNextCloseSave) {
         suppressNextCloseSave = false;
         return;
      }

      saveSelectedTime(selectedDates, dateStr, instance);
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
   clearButton.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      clearCommittedTime();
   });
   inputWrap.appendChild(input);
   inputWrap.appendChild(clearButton);
   syncClearButtonState();
   flatpickrInstance = ConsoleDatePickers.initTimePicker(input, {
      allowInput: false,
      onChange(_selectedDates, dateStr, instance) {
         latestPickerValue = readPickerTimeValue(instance, dateStr, input);
      },
      onOpen: () => {
         validationBubble.dismiss();
         bindOutsidePointerDown();
      },
      onClose: handlePickerClose,
      onReady(_selectedDates, _dateStr, instance) {
         flatpickrInstance = instance;
         instance.calendarContainer.classList.add('itinerary-day-time-picker');
      },
      ...timePickerOptions,
   });

   return field;
}
