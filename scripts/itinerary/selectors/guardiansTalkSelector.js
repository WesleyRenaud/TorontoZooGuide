import { CreateScheduledOccurrenceSelector } from './createScheduledOccurrenceSelector.js';
import { GuardiansTalkSelectorModel } from './guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { APP_STRINGS } from '../../strings.js';

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
         defaultTitle: APP_STRINGS.itinerary.selectors.talkFallback,
         heading: APP_STRINGS.site.nav.meetTheGuardians,
         subtitle: APP_STRINGS.itinerary.selectors.guardiansTalkSubtitle,
         emptyText: APP_STRINGS.itinerary.emptyText.guardiansTalks,

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
