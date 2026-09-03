import { ValueNormalizer } from '../api/valueNormalizer.js';

export class JoinedTimesFormatter {
   static format(times) {
      return ValueNormalizer.asTrimmedStringList(times).join(', ');
   }
}
