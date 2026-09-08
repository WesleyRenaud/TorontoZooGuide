import { ItineraryClient } from '../../api/itineraryClient.js';
import { ShowScheduleItemFragment } from './components/showScheduleItemFragment.js';
import { DraftStore } from '../draftStore.js';
import { ItineraryEventTypes } from '../itineraryEventTypes.js';
import { ItineraryPanelScheduleHandlersHelper } from './itineraryPanelScheduleHandlersHelper.js';
import { RemoveItineraryItemFragment } from './removeItineraryItemFragment.js';

export class ItineraryPanelScheduleHandler {
   static openScheduleItemModule(
   {
      itinerary = {},
      eventTypes = [],
      onScheduled = null,
      preselectedRow = null,
   } = {},
   deps = {}
) {
      const showModule = deps.showScheduleItemModule ?? ShowScheduleItemFragment.showScheduleItemModule;

      showModule({
         itinerary,
         eventTypes,
         onScheduled,
         preselectedRow,
      });
   }

   static buildItineraryPanelScheduleHandlers(
   itinerary = {},
   {
      onPanelRefresh = null,
      deps = {},
   } = {}
) {
      const {
         openModule = ItineraryPanelScheduleHandler.openScheduleItemModule,
         unscheduleItem = ItineraryClient.unscheduleItineraryItemRequest,
         removeItem = ItineraryClient.removeItemFromItineraryRequest,
         removeAnimalDraft = DraftStore.removeAnimalFromItineraryAnimalDraft,
         requiresRemoveConfirmation = ItineraryEventTypes.requiresRemoveItineraryItemConfirmation,
         showRemoveConfirmation = RemoveItineraryItemFragment.showRemoveItineraryItemConfirmation,
         buildEventTypes = ItineraryEventTypes.buildSchedulableEventTypes,
         notifyUpdated = ItineraryPanelScheduleHandlersHelper.notifyItineraryUpdated,
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
}
