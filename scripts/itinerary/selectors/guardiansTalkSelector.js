import { createScheduledOccurrenceSelectorController } from './createScheduledOccurrenceSelector.js';
import {
   buildGuardiansTalkSelectionFields,
   getGuardiansTalkId,
   getGuardiansTalkLocation,
   getGuardiansTalkName,
   getGuardiansTalkScheduleStart,
   readGuardiansTalkStoredFields,
} from './guardiansTalkSelector/model.js';
import { APP_STRINGS } from '../../strings.js';

const STORAGE_KEY = 'tzg.itineraryGuardiansTalks';

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

      getName: getGuardiansTalkName,
      getId: getGuardiansTalkId,
      getPrimaryValue: getGuardiansTalkLocation,
      getTimeOfDay: getGuardiansTalkScheduleStart,
      emptyStoredFields: {
         location: '',
         start_time: '',
         end_time: '',
      },
      readStoredFields: readGuardiansTalkStoredFields,
      buildSelectionFields: buildGuardiansTalkSelectionFields,
   });
}
