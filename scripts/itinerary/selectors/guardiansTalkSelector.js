import { normalizeStoredString } from './base/storedSelection.js';
import { createScheduledOccurrenceSelectorController } from './createScheduledOccurrenceSelector.js';
import { APP_STRINGS } from '../../strings.js';

const STORAGE_KEY = 'tzg.itineraryGuardiansTalks';

function getTalkLocation(row) {
   return row.location ?? '';
}

function getTalkScheduleStart(row) {
   return normalizeStoredString(row?.start_time);
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
      defaultTitle: APP_STRINGS.itinerary.selectors.talkFallback,
      heading: APP_STRINGS.site.nav.meetTheGuardians,
      subtitle: APP_STRINGS.itinerary.selectors.guardiansTalkSubtitle,
      emptyText: APP_STRINGS.itinerary.emptyText.guardiansTalks,

      primaryLabel: APP_STRINGS.labels.location,
      getPrimaryValue: getTalkLocation,
      getTimeOfDay: getTalkScheduleStart,
      emptyStoredFields: {
         location: '',
         start_time: '',
         end_time: '',
      },
      readStoredFields: (item) => ({
         location: normalizeStoredString(item.location),
         start_time: normalizeStoredString(item.start_time),
         end_time: normalizeStoredString(item.end_time),
      }),
      buildSelectionFields: (row) => ({
         location: getTalkLocation(row),
         start_time: getTalkScheduleStart(row),
         end_time: normalizeStoredString(row?.end_time),
      }),
   });
}
