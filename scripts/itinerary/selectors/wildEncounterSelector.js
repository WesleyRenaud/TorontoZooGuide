import {
   normalizeStoredLink,
   normalizeStoredString,
} from './base/storedSelection.js';
import { createScheduledOccurrenceSelectorController } from './createScheduledOccurrenceSelector.js';
import { APP_STRINGS } from '../../strings.js';

const STORAGE_KEY = 'tzg.itineraryWildEncounters';

function getWildEncounterMeetingSpot(row) {
   return row.meeting_spot ?? '';
}

function getWildEncounterScheduleStart(row) {
   return normalizeStoredString(row?.start_time);
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
      defaultTitle: APP_STRINGS.entityLabels.wildEncounter,
      heading: APP_STRINGS.site.nav.wildEncounters,
      subtitle: APP_STRINGS.itinerary.selectors.wildEncounterSubtitle,
      emptyText: APP_STRINGS.itinerary.emptyText.wildEncounters,

      primaryLabel: APP_STRINGS.itinerary.selectors.meetingSpot,
      getPrimaryValue: getWildEncounterMeetingSpot,
      getTimeOfDay: getWildEncounterScheduleStart,
      getLink: getWildEncounterLink,
      emptyStoredFields: {
         meeting_spot: '',
         start_time: '',
         end_time: '',
      },
      readStoredFields: (item) => ({
         meeting_spot: normalizeStoredString(item.meeting_spot),
         start_time: normalizeStoredString(item.start_time),
         end_time: normalizeStoredString(item.end_time),
      }),
      buildSelectionFields: (row) => ({
         meeting_spot: getWildEncounterMeetingSpot(row),
         start_time: getWildEncounterScheduleStart(row),
         end_time: normalizeStoredString(row?.end_time),
      }),
   });
}
