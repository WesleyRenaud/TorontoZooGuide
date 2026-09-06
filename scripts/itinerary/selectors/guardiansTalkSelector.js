import { CreateScheduledOccurrenceSelector } from './createScheduledOccurrenceSelector.js';
import { GuardiansTalkSelectorModel } from './guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { Strings } from '../../strings.js';

const STORAGE_KEY = 'tzg.itineraryGuardiansTalks';

export class GuardiansTalkSelector {
   static createItineraryGuardiansTalkSelectorController({
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
         responseKey: 'guardians_talks',
         searchFlag: 'includeGuardiansTalks',
         imageDirectory: 'guardians-talks',
         defaultTitle: Strings.itinerary.selectors.talkFallback,
         heading: Strings.site.nav.meetTheGuardians,
         subtitle: Strings.itinerary.selectors.guardiansTalkSubtitle,
         emptyText: Strings.itinerary.emptyText.guardiansTalks,

         getName: GuardiansTalkSelectorModel.getGuardiansTalkName,
         getId: GuardiansTalkSelectorModel.getGuardiansTalkId,
         getPrimaryValue: GuardiansTalkSelectorModel.getGuardiansTalkLocation,
         getTimeOfDay: GuardiansTalkSelectorModel.getGuardiansTalkScheduleStart,
         emptyStoredFields: {
            location: '',
            start_time: '',
            end_time: '',
         },
         readStoredFields: GuardiansTalkSelectorModel.readGuardiansTalkStoredFields,
         buildSelectionFields: GuardiansTalkSelectorModel.buildGuardiansTalkSelectionFields,
      });
   }
}
