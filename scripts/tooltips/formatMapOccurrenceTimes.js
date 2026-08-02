import { asTrimmedString } from '../api/normalizeValues.js';
import { formatJoinedTimes } from '../shared/formatJoinedTimes.js';

export function formatMapOccurrenceTimes(item = {}) {
   return formatJoinedTimes(item.times) || asTrimmedString(item.start_time);
}
