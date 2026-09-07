import { ValueNormalizer } from '../api/valueNormalizer.js';
import { TimePickerEnterCommit } from './timePickerEnterCommit.js';

export class MultiTimePickerHelpers {
   static resetPickerSelection(instance) {
      instance?.setDate?.([], false);
   }

   static createMultiTimeCommitController({
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
         MultiTimePickerHelpers.resetPickerSelection(instance);
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

   static wireMultiTimeInputEvents(inputEl, picker, controller, {
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
}
