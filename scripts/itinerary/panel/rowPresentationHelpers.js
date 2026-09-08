import { Strings } from '../../strings.js';

export class RowPresentationHelpers {
   static buildTimeFieldLine(value) {
      if (!value) {
         return '';
      }

      return `${Strings.labels.time}: ${value}`;
   }
}
