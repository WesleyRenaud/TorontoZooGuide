import { ValueNormalizer } from '../api/valueNormalizer.js';
import { JoinedTimesFormatter } from '../shared/joinedTimesFormatter.js';

export class MapOccurrenceTimesFormatter {
   static format(item = {}) {
      return JoinedTimesFormatter.format(item.times)
         || ValueNormalizer.asTrimmedString(item.start_time);
   }
}
