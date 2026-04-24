import {
   normalizeStoredLink,
   normalizeStoredString,
} from './base/storedSelection.js';
import { createScheduledOccurrenceSelectorController } from './createScheduledOccurrenceSelector.js';

const STORAGE_KEY = 'tzg.itineraryWildEncounters';

function getWildEncounterMeetingSpot(row) {
   return row.meeting_spot ?? '';
}

function getWildEncounterTimeOfDay(row) {
   return row.time_of_day ?? '';
}

function getWildEncounterLink(row) {
   return normalizeStoredLink(row?.link);
}

export function createItineraryWildEncounterSelectorController({
   mountEl,
   onPrev,
   onFinish,
   onClose,
} = {}) {
   return createScheduledOccurrenceSelectorController({
      mountEl,
      onPrev,
      onFinish,
      onClose,
      hideNextButton: true,

      storageKey: STORAGE_KEY,
      responseKey: 'wild_encounters',
      searchFlag: 'includeWildEncounters',
      imageDirectory: 'wild-encounters',
      defaultTitle: 'Wild Encounter',
      heading: 'Wild Encounters',
      subtitle: 'Search and add wild encounters to your plan.',
      emptyText: 'No wild encounters found for this day',

      primaryLabel: 'Meeting Spot',
      getPrimaryValue: getWildEncounterMeetingSpot,
      getTimeOfDay: getWildEncounterTimeOfDay,
      getLink: getWildEncounterLink,
      emptyStoredFields: {
         meetingSpot: '',
         timeOfDay: '',
      },
      readStoredFields: (item) => ({
         meetingSpot: normalizeStoredString(item.meetingSpot),
         timeOfDay: normalizeStoredString(item.timeOfDay),
      }),
      buildSelectionFields: (row) => ({
         meetingSpot: getWildEncounterMeetingSpot(row),
         timeOfDay: getWildEncounterTimeOfDay(row),
      }),
   });
}
