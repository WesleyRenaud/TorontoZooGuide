import {
   normalizeStoredString,
} from './base/storedSelection.js';
import { createScheduledOccurrenceSelectorController } from './createScheduledOccurrenceSelector.js';

const STORAGE_KEY = 'tzg.itineraryGuardiansTalks';

function getTalkLocation(row) {
   return row.location ?? '';
}

function getTalkTimeOfDay(row) {
   return row.time_of_day ?? '';
}

export function createItineraryGuardiansTalkSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish,
   onClose,
} = {}) {
   return createScheduledOccurrenceSelectorController({
      mountEl,
      onPrev,
      onNext,
      onFinish,
      onClose,

      storageKey: STORAGE_KEY,
      responseKey: 'guardians_talks',
      searchFlag: 'includeGuardiansTalks',
      imageDirectory: 'guardians-talks',
      defaultTitle: 'Talk',
      heading: 'Meet the Guardians',
      subtitle: 'Search and add talks to your plan.',
      emptyText: 'No Meet the Guardians talks found for this day',

      primaryLabel: 'Location',
      getPrimaryValue: getTalkLocation,
      getTimeOfDay: getTalkTimeOfDay,
      emptyStoredFields: {
         location: '',
         timeOfDay: '',
      },
      readStoredFields: (item) => ({
         location: normalizeStoredString(item.location),
         timeOfDay: normalizeStoredString(item.timeOfDay),
      }),
      buildSelectionFields: (row) => ({
         location: getTalkLocation(row),
         timeOfDay: getTalkTimeOfDay(row),
      }),
   });
}
