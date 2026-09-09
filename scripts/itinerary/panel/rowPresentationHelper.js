import { Strings } from '../../strings.js';

export class RowPresentationHelper {
   static buildTimeFieldLine(value) {
      if (!value) {
         return '';
      }

      return Strings.format.labeledValue(Strings.labels.time, value);
   }
}
