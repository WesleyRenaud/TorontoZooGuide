import { ValueNormalizer } from '../api/valueNormalizer.js';
import { Strings } from '../strings.js';

export class JoinedTimesFormatter {
   static format(times) {
      return ValueNormalizer.asTrimmedStringList(times).join(Strings.format.listJoin);
   }
}
