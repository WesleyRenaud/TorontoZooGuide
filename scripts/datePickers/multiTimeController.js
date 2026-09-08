import { ValueNormalizer } from '../api/valueNormalizer.js';
import { ConsoleDateFactory } from './consoleDateFactory.js';
import { FlatpickrAdapter } from './flatpickrAdapter.js';
import { MultiTimePickerHelper } from './multiTimePickerHelper.js';

export class MultiTimeController {
   static initMultiTimePicker(
      inputEl,
      {
         onCommitTime = null,
         onRemoveLastTime = null,
      } = {},
      initFlatpickrFn = FlatpickrAdapter.initFlatpickr
   ) {
      if (!inputEl) {
         return null;
      }

      const controller = MultiTimePickerHelper.createMultiTimeCommitController({
         inputEl,
         onCommitTime,
      });

      const picker = ConsoleDateFactory.initTimePicker(inputEl, {
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

      MultiTimePickerHelper.wireMultiTimeInputEvents(inputEl, picker, controller, {
         onRemoveLastTime,
      });

      return picker;
   }
}
