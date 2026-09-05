import { ItineraryApi } from '../../api/itineraryApi.js';
import { ShowScheduleItemModule } from './components/showScheduleItemModule.js';
import { DraftStorage } from '../draftStorage.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItineraryEventTypes } from '../itineraryEventTypes.js';
import {
   dispatchItineraryUpdated,
   getItinerary,
} from '../itineraryService.js';
import { RemoveItineraryItemConfirmation } from './removeItineraryItemConfirmation.js';

async function notifyItineraryUpdated({
   result,
   dispatchUpdated = dispatchItineraryUpdated,
   loadItinerary = getItinerary,
} = {}) {
   if (!ItineraryErrorTypes.isItinerarySuccess(result?.errorType)) {
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
   const showModule = deps.showScheduleItemModule ?? ShowScheduleItemModule.showScheduleItemModule;

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
      unscheduleItem = ItineraryApi.unscheduleItineraryItemRequest,
      removeItem = ItineraryApi.removeItemFromItineraryRequest,
      removeAnimalDraft = DraftStorage.removeAnimalFromItineraryAnimalDraft,
      requiresRemoveConfirmation = ItineraryEventTypes.requiresRemoveItineraryItemConfirmation,
      showRemoveConfirmation = RemoveItineraryItemConfirmation.showRemoveItineraryItemConfirmation,
      buildEventTypes = ItineraryEventTypes.buildSchedulableEventTypes,
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
               itemType,
               key,
               onConfirm: performRemove,
            });
            return;
         }

         void performRemove();
      },
   };
}
