import { createScheduledOccurrenceSelectorController } from './createScheduledOccurrenceSelector.js';
import { APP_STRINGS } from '../../strings.js';
import { WildEncounterSelectorModel } from './wildEncounterSelector/wildEncounterSelectorModel.js';

const STORAGE_KEY = 'tzg.itineraryWildEncounters';

export function createItineraryWildEncounterSelectorController({
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
      responseKey: 'wild_encounters',
      searchFlag: 'includeWildEncounters',
      imageDirectory: 'wild-encounters',
      defaultTitle: APP_STRINGS.entityLabels.wildEncounter,
      heading: APP_STRINGS.site.nav.wildEncounters,
      subtitle: APP_STRINGS.itinerary.selectors.wildEncounterSubtitle,
      emptyText: APP_STRINGS.itinerary.emptyText.wildEncounters,

      getName: WildEncounterSelectorModel.getWildEncounterName,
      getId: WildEncounterSelectorModel.getWildEncounterId,
      getPrimaryValue: WildEncounterSelectorModel.getWildEncounterMeetingSpot,
      getTimeOfDay: WildEncounterSelectorModel.getWildEncounterScheduleStart,
      getLink: WildEncounterSelectorModel.getWildEncounterLink,
      emptyStoredFields: {
         meeting_spot: '',
         start_time: '',
         end_time: '',
      },
      readStoredFields: WildEncounterSelectorModel.readWildEncounterStoredFields,
      buildSelectionFields: WildEncounterSelectorModel.buildWildEncounterSelectionFields,
   });
}
