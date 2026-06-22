import { createScheduledOccurrenceSelectorController } from './createScheduledOccurrenceSelector.js';
import { APP_STRINGS } from '../../strings.js';
import {
   buildWildEncounterSelectionFields,
   getWildEncounterId,
   getWildEncounterLink,
   getWildEncounterMeetingSpot,
   getWildEncounterName,
   getWildEncounterScheduleStart,
   readWildEncounterStoredFields,
} from './wildEncounterSelector/model.js';

const STORAGE_KEY = 'tzg.itineraryWildEncounters';

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

      getName: getWildEncounterName,
      getId: getWildEncounterId,
      getPrimaryValue: getWildEncounterMeetingSpot,
      getTimeOfDay: getWildEncounterScheduleStart,
      getLink: getWildEncounterLink,
      emptyStoredFields: {
         meeting_spot: '',
         start_time: '',
         end_time: '',
      },
      readStoredFields: readWildEncounterStoredFields,
      buildSelectionFields: buildWildEncounterSelectionFields,
   });
}
