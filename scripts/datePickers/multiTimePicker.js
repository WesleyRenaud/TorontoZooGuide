import { ValueNormalizer } from '../api/valueNormalizer.js';
import { initTimePicker } from './consoleDatePickers.js';
import { initFlatpickr } from './flatpickr.js';
import { TimePickerEnterCommit } from './timePickerEnterCommit.js';

function resetPickerSelection(instance) {
   instance?.setDate?.([], false);
}

function createMultiTimeCommitController({
   inputEl,
   onCommitTime,
}) {
   function commitTime(time, instance) {
      const normalizedTime = ValueNormalizer.asTrimmedString(time);

      if (!normalizedTime) {
         return false;
      }

      onCommitTime?.(normalizedTime);
      inputEl.value = '';
      resetPickerSelection(instance);
      return true;
   }

   function commitResolvedTime(instance) {
      return commitTime(
         TimePickerEnterCommit.resolveOpenTimePickerValue(inputEl, instance),
         instance
      );
   }

   function commitAfterInputSettles(instance, pendingTime) {
      setTimeout(() => {
         if (
            !ValueNormalizer.asTrimmedString(inputEl.value)
            && ValueNormalizer.asTrimmedString(pendingTime)
         ) {
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
         && !ValueNormalizer.asTrimmedString(inputEl?.value)
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

         const pendingTime = ValueNormalizer.asTrimmedString(inputEl?.value);

         if (pendingTime) {
            controller.commitAfterInputSettles(picker, pendingTime);
         }
      }, 0);
   });
}

export class MultiTimePicker {
   static initMultiTimePicker(
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
            const pendingTime = ValueNormalizer.asTrimmedString(inputEl?.value);

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
}
