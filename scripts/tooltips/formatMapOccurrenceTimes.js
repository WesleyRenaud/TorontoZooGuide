import { asTrimmedString } from '../api/normalizeValues.js';
import { JoinedTimesFormatter } from '../shared/joinedTimesFormatter.js';

export function formatMapOccurrenceTimes(item = {}) {
   return JoinedTimesFormatter.format(item.times) || asTrimmedString(item.start_time);
}
