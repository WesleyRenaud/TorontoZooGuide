import {
   removeItemFromItineraryRequest,
   unscheduleItineraryItemRequest,
} from '../../api/itineraryApi.js';
import { showScheduleItemModule } from './components/showScheduleItemModule.js';
import { removeAnimalFromItineraryAnimalDraft } from '../draftStorage.js';
import { isItinerarySuccess } from '../itineraryErrorTypes.js';
import { requiresRemoveItineraryItemConfirmation } from '../itineraryEventTypes.js';
import {
   dispatchItineraryUpdated,
   getItinerary,
} from '../itineraryService.js';
import { showRemoveItineraryItemConfirmation } from './removeItineraryItemConfirmation.js';
import { buildSchedulableEventTypes } from './scheduleItemTypes.js';

async function notifyItineraryUpdated({
   result,
   dispatchUpdated = dispatchItineraryUpdated,
   loadItinerary = getItinerary,
} = {}) {
   if (!isItinerarySuccess(result?.errorType)) {
      return false;
   }

   dispatchUpdated(await loadItinerary());
   return true;
}

export function openScheduleItemModule(
   {
      itinerary = {},
      eventTypes = [],
      onScheduled = null,
      preselectedRow = null,
   } = {},
   deps = {}
) {
   const showModule = deps.showScheduleItemModule ?? showScheduleItemModule;

   showModule({
      itinerary,
      eventTypes,
      onScheduled,
      preselectedRow,
   });
}

export function buildItineraryPanelScheduleHandlers(
   itinerary = {},
   {
      onPanelRefresh = null,
      deps = {},
   } = {}
) {
   const {
      openModule = openScheduleItemModule,
      unscheduleItem = unscheduleItineraryItemRequest,
      removeItem = removeItemFromItineraryRequest,
      removeAnimalDraft = removeAnimalFromItineraryAnimalDraft,
      requiresRemoveConfirmation = requiresRemoveItineraryItemConfirmation,
      showRemoveConfirmation = showRemoveItineraryItemConfirmation,
      buildEventTypes = buildSchedulableEventTypes,
      notifyUpdated = notifyItineraryUpdated,
   } = deps;

   return {
      onScheduleItineraryItem: (pick) => {
         openModule({
            itinerary,
            eventTypes: buildEventTypes(itinerary.itineraryConfig),
            onScheduled: onPanelRefresh,
            preselectedRow: pick?.row ?? null,
         }, deps);
      },
      onUnscheduleItineraryItem: async ({ itemType, key }) => {
         const result = await unscheduleItem({ itemType, key });
         await notifyUpdated({ result });

         if (typeof onPanelRefresh === 'function') {
            await onPanelRefresh();
         }
      },
      onRemoveItineraryItem: ({ itemType, key }) => {
         const performRemove = async () => {
            const result = await removeItem({ itemType, key });
            removeAnimalDraft(itemType, key);
            await notifyUpdated({ result });

            if (typeof onPanelRefresh === 'function') {
               await onPanelRefresh();
            }
         };

         if (requiresRemoveConfirmation(itemType, itinerary.itineraryConfig)) {
            showRemoveConfirmation({
               onConfirm: performRemove,
            });
            return;
         }

         void performRemove();
      },
   };
}
