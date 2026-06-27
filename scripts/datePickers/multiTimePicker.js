import { initTimePicker } from './consoleDatePickers.js';
import { initFlatpickr } from './flatpickr.js';
import { readOpenPickerTime } from './readOpenPickerTime.js';

function resetPickerSelection(instance) {
   instance?.setDate?.([], false);
}

function createMultiTimeCommitController({
   inputEl,
   onCommitTime,
}) {
   function commitTime(time, instance) {
      const normalizedTime = time?.trim() ?? '';

      if (!normalizedTime) {
         return false;
      }

      onCommitTime?.(normalizedTime);
      inputEl.value = '';
      resetPickerSelection(instance);
      return true;
   }

   function resolveCommitTime(instance) {
      return inputEl?.value?.trim() || readOpenPickerTime(instance);
   }

   function commitResolvedTime(instance) {
      return commitTime(resolveCommitTime(instance), instance);
   }

   function commitAfterInputSettles(instance, pendingTime) {
      setTimeout(() => {
         if (!inputEl.value.trim() && pendingTime.trim()) {
            commitTime(pendingTime, instance);
            return;
         }

         commitResolvedTime(instance);
      }, 0);
   }

   return {
      commitTime,
      commitResolvedTime,
      commitAfterInputSettles,
      handleEnterKey(instance, event) {
         if (event.key !== 'Enter') {
            return;
         }

         event.preventDefault();
         event.stopImmediatePropagation();
         commitResolvedTime(instance);
         instance?.close?.();
      },
   };
}

function wireMultiTimeInputEvents(inputEl, picker, controller, {
   onRemoveLastTime = null,
} = {}) {
   inputEl.addEventListener('keydown', (event) => {
      if (
         event.key === 'Backspace'
         && !inputEl?.value?.trim()
         && onRemoveLastTime?.()
      ) {
         event.preventDefault();
         event.stopImmediatePropagation();
         picker?.close?.();
         return;
      }

      controller.handleEnterKey(picker, event);
   }, true);

   inputEl.addEventListener('blur', () => {
      setTimeout(() => {
         if (picker?.isOpen) {
            return;
         }

         const pendingTime = inputEl?.value?.trim() ?? '';

         if (pendingTime) {
            controller.commitAfterInputSettles(picker, pendingTime);
         }
      }, 0);
   });
}

export function initMultiTimePicker(
   inputEl,
   {
      onCommitTime = null,
      onRemoveLastTime = null,
   } = {},
   initFlatpickrFn = initFlatpickr
) {
   if (!inputEl) {
      return null;
   }

   const controller = createMultiTimeCommitController({
      inputEl,
      onCommitTime,
   });

   const picker = initTimePicker(inputEl, {
      onClose(_selectedDates, _dateStr, instance) {
         const pendingTime = inputEl?.value?.trim() ?? '';

         if (pendingTime) {
            controller.commitAfterInputSettles(instance, pendingTime);
         }
      },
   }, initFlatpickrFn);

   wireMultiTimeInputEvents(inputEl, picker, controller, {
      onRemoveLastTime,
   });

   return picker;
}
