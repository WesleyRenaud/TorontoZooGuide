import { asTrimmedStringList } from '../api/normalizeValues.js';

export class JoinedTimesFormatter {
   static format(times) {
      return asTrimmedStringList(times).join(', ');
   }
}
