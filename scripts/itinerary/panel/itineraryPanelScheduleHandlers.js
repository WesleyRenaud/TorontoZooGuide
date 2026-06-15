import {
   removeItemFromItineraryRequest,
   unscheduleItineraryItemRequest,
} from '../../api/itineraryApi.js';
import { showScheduleItemModule } from './components/showScheduleItemModule.js';
import { removeAnimalFromItineraryAnimalDraft } from '../draftStorage.js';
import { requiresRemoveItineraryItemConfirmation } from '../itineraryEventTypes.js';
import { showRemoveItineraryItemConfirmation } from './removeItineraryItemConfirmation.js';
import { buildSchedulableEventTypes } from './scheduleItemTypes.js';

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
         await unscheduleItem({ itemType, key });

         if (typeof onPanelRefresh === 'function') {
            await onPanelRefresh();
         }
      },
      onRemoveItineraryItem: ({ itemType, key }) => {
         const performRemove = async () => {
            await removeItem({ itemType, key });
            removeAnimalDraft(itemType, key);

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
