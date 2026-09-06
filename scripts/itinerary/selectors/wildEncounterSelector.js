import { CreateScheduledOccurrenceSelector } from './createScheduledOccurrenceSelector.js';
import { Strings } from '../../strings.js';
import { WildEncounterSelectorModel } from './wildEncounterSelector/wildEncounterSelectorModel.js';

const STORAGE_KEY = 'tzg.itineraryWildEncounters';

export class WildEncounterSelector {
   static createItineraryWildEncounterSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish,
   onClose,
} = {}) {
      return CreateScheduledOccurrenceSelector.createScheduledOccurrenceSelectorController({
         mountEl,
         onPrev,
         onNext,
         onFinish,
         onClose,

         storageKey: STORAGE_KEY,
         responseKey: 'wild_encounters',
         searchFlag: 'includeWildEncounters',
         imageDirectory: 'wild-encounters',
         defaultTitle: Strings.entityLabels.wildEncounter,
         heading: Strings.site.nav.wildEncounters,
         subtitle: Strings.itinerary.selectors.wildEncounterSubtitle,
         emptyText: Strings.itinerary.emptyText.wildEncounters,

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
}
