import { ValueNormalizer } from '../api/valueNormalizer.js';
import { ConsoleDatePickers } from './consoleDatePickers.js';
import { Flatpickr } from './flatpickr.js';
import { MultiTimePickerHelpers } from './multiTimePickerHelpers.js';

export class MultiTimePicker {
   static initMultiTimePicker(
      inputEl,
      {
         onCommitTime = null,
         onRemoveLastTime = null,
      } = {},
      initFlatpickrFn = Flatpickr.initFlatpickr
   ) {
      if (!inputEl) {
         return null;
      }

      const controller = MultiTimePickerHelpers.createMultiTimeCommitController({
         inputEl,
         onCommitTime,
      });

      const picker = ConsoleDatePickers.initTimePicker(inputEl, {
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

      MultiTimePickerHelpers.wireMultiTimeInputEvents(inputEl, picker, controller, {
         onRemoveLastTime,
      });

      return picker;
   }
}
