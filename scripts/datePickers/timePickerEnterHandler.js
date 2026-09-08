import { ValueNormalizer } from '../api/valueNormalizer.js';
import { ReadOpenPickerFormatter } from './readOpenPickerFormatter.js';

export class TimePickerEnterHandler {
   static resolveOpenTimePickerValue(inputEl, instance) {
      return ValueNormalizer.asTrimmedString(inputEl?.value)
         || ReadOpenPickerFormatter.readOpenPickerTime(instance)
         || '';
   }

   static commitTimeToInput(time, instance, inputEl) {
      if (typeof instance?.setDate === 'function') {
         instance.setDate(time, true);
      }
      else if (inputEl) {
         inputEl.value = time;
      }

      instance?.close?.();
   }

   static wireTimePickerEnterCommit(inputEl, instance, onEnterCommit) {
      if (!inputEl || !instance || typeof onEnterCommit !== 'function') {
         return;
      }

      const onEnter = (event) => {
         if (event.key !== 'Enter') {
            return;
         }

         event.preventDefault();
         event.stopImmediatePropagation();

         const time = TimePickerEnterHandler.resolveOpenTimePickerValue(inputEl, instance);

         if (!time) {
            return;
         }

         onEnterCommit(time, instance);
      };

      if (!inputEl.__tzgTimeEnterWired) {
         inputEl.__tzgTimeEnterWired = true;
         inputEl.addEventListener('keydown', onEnter, true);
      }

      if (
         instance.calendarContainer
         && !instance.__tzgTimeEnterWired
      ) {
         instance.__tzgTimeEnterWired = true;
         instance.calendarContainer.addEventListener('keydown', onEnter, true);
      }
   }
}
