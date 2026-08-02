import { asTrimmedStringList } from '../api/normalizeValues.js';

export function formatJoinedTimes(times) {
   return asTrimmedStringList(times).join(', ');
}
