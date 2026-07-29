import { initTimePicker } from './consoleDatePickers.js';
import { initFlatpickr } from './flatpickr.js';
import { resolveOpenTimePickerValue } from './timePickerEnterCommit.js';

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

   function commitResolvedTime(instance) {
      return commitTime(resolveOpenTimePickerValue(inputEl, instance), instance);
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
      }
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
      onEnterCommit(time, instance) {
         controller.commitTime(time, instance);
         instance?.close?.();
      },
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
