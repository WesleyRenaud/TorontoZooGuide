import { BulkScheduleItineraryNotEnoughTimeFragment } from './bulkScheduleItineraryNotEnoughTimeFragment.js';
import { DayPlannerBuilder } from './components/dayPlannerBuilder.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { DayPlannerActionPresenter } from './dayPlannerActionPresenter.js';
import { FixedTimeItemLongWaitFragment } from './fixedTimeItemLongWaitFragment.js';
import { ItineraryBuildWarningsFragment } from './itineraryBuildWarningsFragment.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItineraryEventTypes } from '../itineraryEventTypes.js';
import { ItineraryPanelScheduleHandler } from './itineraryPanelScheduleHandler.js';
import { ItineraryService } from '../itineraryService.js';
import { Strings } from '../../strings.js';

export class ItineraryPanelContentHelper {
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
         openModule = ItineraryPanelScheduleHandler.openScheduleItemModule,
         bulkSchedule = ItineraryService.bulkScheduleItinerary,
         unscheduleAll = ItineraryService.unscheduleAllItineraryItems,
         hasNotEnoughTimeIssue = BulkScheduleItineraryNotEnoughTimeFragment.hasBulkScheduleItineraryNotEnoughTimeIssue,
         hasMultipleBuildWarnings = ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings,
         showBuildWarningsConfirmation = ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation,
         requiresLongWaitConfirmation = ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation,
         showLongWaitConfirmation = FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation,
         setActionFeedback = DayPlannerActionPresenter.setPendingDayPlannerActionFeedback,
         buildEventTypes = ItineraryEventTypes.buildSchedulableEventTypes,
         buildScheduleHandlers = ItineraryPanelScheduleHandler.buildItineraryPanelScheduleHandlers,
         makeDayPlanner = DayPlannerBuilder.makeDayPlannerPreview,
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

               const mountEl = ItineraryPanelFragment.getItineraryPanelMountEl() ?? document.body;
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
                           ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings(result.issues)
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
