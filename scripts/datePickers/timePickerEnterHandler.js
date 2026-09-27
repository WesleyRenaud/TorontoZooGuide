import { ValueNormalizer } from '../api/valueNormalizer.js';
import { OpenPickerTimeHelper } from './openPickerTimeHelper.js';
import { ReadOpenPickerFormatter } from './readOpenPickerFormatter.js';

export class TimePickerEnterHandler {
   static resolveOpenTimePickerValue(inputEl, instance) {
      return ValueNormalizer.asTrimmedString(inputEl?.value)
         || ReadOpenPickerFormatter.readOpenPickerTime(instance)
         || '';
   }

   static resolvePickerControlsValue(inputEl, instance) {
      // The hour/minute spinners only write back to the input on blur, so a
      // freshly typed minute is visible in the controls but not the input.
      return OpenPickerTimeHelper.readTimeFromPickerControls(
         instance,
         OpenPickerTimeHelper.getPickerDateFormat(instance)
      ) || TimePickerEnterHandler.resolveOpenTimePickerValue(inputEl, instance);
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

      const makeOnEnter = (resolveTime) => (event) => {
         if (event.key !== 'Enter') {
            return;
         }

         event.preventDefault();
         event.stopImmediatePropagation();

         const time = resolveTime(inputEl, instance);

         if (!time) {
            return;
         }

         onEnterCommit(time, instance);
      };

      if (!inputEl.__tzgTimeEnterWired) {
         inputEl.__tzgTimeEnterWired = true;
         inputEl.addEventListener(
            'keydown',
            makeOnEnter(TimePickerEnterHandler.resolveOpenTimePickerValue),
            true
         );
      }

      if (
         instance.calendarContainer
         && !instance.__tzgTimeEnterWired
      ) {
         instance.__tzgTimeEnterWired = true;
         instance.calendarContainer.addEventListener(
            'keydown',
            makeOnEnter(TimePickerEnterHandler.resolvePickerControlsValue),
            true
         );
      }
   }
}
