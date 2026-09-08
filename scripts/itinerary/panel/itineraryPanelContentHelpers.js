import { BulkScheduleItineraryNotEnoughTimeConfirmation } from './bulkScheduleItineraryNotEnoughTimeConfirmation.js';
import { DayPlanner } from './components/dayPlanner.js';
import { ItineraryPanelPopup } from './components/itineraryPanelPopup.js';
import { DayPlannerActionFeedback } from './dayPlannerActionFeedback.js';
import { FixedTimeItemLongWaitConfirmation } from './fixedTimeItemLongWaitConfirmation.js';
import { ItineraryBuildWarningsConfirmation } from './itineraryBuildWarningsConfirmation.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItineraryEventTypes } from '../itineraryEventTypes.js';
import { ItineraryPanelScheduleHandlers } from './itineraryPanelScheduleHandlers.js';
import { ItineraryService } from '../itineraryService.js';
import { Strings } from '../../strings.js';

export class ItineraryPanelContentHelpers {
   static appendDayPlannerViewWithHours(
      dayPlannerView,
      zooHours,
      itinerary = {},
      timeHandlers = {},
      {
         onPanelRefresh = null,
         deps = {},
      } = {}
   ) {
      const {
         openModule = ItineraryPanelScheduleHandlers.openScheduleItemModule,
         bulkSchedule = ItineraryService.bulkScheduleItinerary,
         unscheduleAll = ItineraryService.unscheduleAllItineraryItems,
         hasNotEnoughTimeIssue = BulkScheduleItineraryNotEnoughTimeConfirmation.hasBulkScheduleItineraryNotEnoughTimeIssue,
         hasMultipleBuildWarnings = ItineraryBuildWarningsConfirmation.hasMultipleItineraryBuildWarnings,
         showBuildWarningsConfirmation = ItineraryBuildWarningsConfirmation.showItineraryBuildWarningsConfirmation,
         requiresLongWaitConfirmation = ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation,
         showLongWaitConfirmation = FixedTimeItemLongWaitConfirmation.showFixedTimeItemLongWaitConfirmation,
         setActionFeedback = DayPlannerActionFeedback.setPendingDayPlannerActionFeedback,
         buildEventTypes = ItineraryEventTypes.buildSchedulableEventTypes,
         buildScheduleHandlers = ItineraryPanelScheduleHandlers.buildItineraryPanelScheduleHandlers,
         makeDayPlanner = DayPlanner.makeDayPlannerPreview,
         genericErrorMessage = Strings.itinerary.errors.generic,
      } = deps;

      const scheduleHandlers = buildScheduleHandlers(itinerary, {
         onPanelRefresh,
         deps,
      });

      const queueActionFeedback = async (feedback) => {
         setActionFeedback(feedback);

         if (typeof onPanelRefresh === 'function') {
            await onPanelRefresh();
         }
      };

      dayPlannerView.appendChild(
         makeDayPlanner(zooHours, itinerary, timeHandlers, {
            onScheduleItemClick: () => {
               openModule({
                  itinerary,
                  eventTypes: buildEventTypes(itinerary.itineraryConfig),
                  onScheduled: onPanelRefresh,
               }, deps);
            },
            onRebuildScheduleClick: async () => {
               const applyRebuildResult = async (result) => {
                  if (result.errorType) {
                     await queueActionFeedback({
                        variant: 'error',
                        message: result.message || genericErrorMessage,
                     });
                     return;
                  }

                  if (typeof onPanelRefresh === 'function') {
                     await onPanelRefresh();
                  }

                  if (hasNotEnoughTimeIssue(result.issues)) {
                     await queueActionFeedback({
                        variant: 'error',
                        message: (
                           Strings.itinerary.confirmation
                              .bulkScheduleItineraryNotEnoughTimeMessage
                        ),
                     });
                     return;
                  }

                  await queueActionFeedback({
                     variant: 'success',
                     message: Strings.itinerary.dayPlanner.rebuildScheduleSuccess,
                  });
               };

               const mountEl = ItineraryPanelPopup.getItineraryPanelMountEl() ?? document.body;
               const confirmRebuildWithOptions = (confirmedOptions) => (
                  async () => {
                     try {
                        await applyRebuildResult(
                           await bulkSchedule(confirmedOptions)
                        );
                     }
                     catch (err) {
                        console.error('Failed to rebuild schedule:', err);
                        await queueActionFeedback({
                           variant: 'error',
                           message: err?.message || genericErrorMessage,
                        });
                     }
                  }
               );

               try {
                  const result = await bulkSchedule();

                  if (hasMultipleBuildWarnings(result.issues)) {
                     showBuildWarningsConfirmation({
                        issues: result.issues,
                        mountEl,
                        onConfirm: confirmRebuildWithOptions(
                           ItineraryBuildWarningsConfirmation.buildConfirmedOptionsFromBuildWarnings(result.issues)
                        ),
                     });
                     return;
                  }

                  if (requiresLongWaitConfirmation(result.errorType)) {
                     showLongWaitConfirmation({
                        issues: result.issues,
                        mountEl,
                        onConfirm: confirmRebuildWithOptions({
                           confirmingFixedTimeItemLongWait: true,
                        }),
                     });
                     return;
                  }

                  await applyRebuildResult(result);
               }
               catch (err) {
                  console.error('Failed to rebuild schedule:', err);
                  await queueActionFeedback({
                     variant: 'error',
                     message: err?.message || genericErrorMessage,
                  });
               }
            },
            onUnscheduleAllItemsClick: async () => {
               try {
                  const result = await unscheduleAll();

                  if (result.errorType) {
                     await queueActionFeedback({
                        variant: 'error',
                        message: result.message || genericErrorMessage,
                     });
                     return;
                  }

                  await queueActionFeedback({
                     variant: 'success',
                     message: Strings.itinerary.dayPlanner.unscheduleAllSuccess,
                  });
               }
               catch (err) {
                  console.error('Failed to unschedule all items:', err);
                  await queueActionFeedback({
                     variant: 'error',
                     message: err?.message || genericErrorMessage,
                  });
               }
            },
            scheduleHandlers,
         })
      );
   }
}
