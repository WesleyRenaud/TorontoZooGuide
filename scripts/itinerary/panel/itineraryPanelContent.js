import { BulkScheduleItineraryNotEnoughTimeConfirmation } from './bulkScheduleItineraryNotEnoughTimeConfirmation.js';
import { ActionsBar } from './components/actionsBar.js';
import { BuildOnly } from './components/buildOnly.js';
import { DateCard } from './components/dateCard.js';
import { DayPlanner } from './components/dayPlanner.js';
import { Popup } from './components/popup.js';
import { Section } from './components/section.js';
import { DayPlannerActionFeedback } from './dayPlannerActionFeedback.js';
import { FixedTimeItemLongWaitConfirmation } from './fixedTimeItemLongWaitConfirmation.js';
import { ItineraryBuildWarningsConfirmation } from './itineraryBuildWarningsConfirmation.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItineraryEventTypes } from '../itineraryEventTypes.js';
import { ItineraryPanelScheduleHandlers } from './itineraryPanelScheduleHandlers.js';
import { ItineraryPanelViewState } from './itineraryPanelViewState.js';
import { ItineraryService } from '../itineraryService.js';
import { ItineraryServiceTime } from '../itineraryServiceTime.js';
import { SectionConfigs } from './sectionConfigs.js';
import { Strings } from '../../strings.js';

function appendDayPlannerViewWithHours(
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

            const mountEl = Popup.getItineraryPanelMountEl() ?? document.body;
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

export class ItineraryPanelContent {
   static destroyRenderedPanelChildren(bodyEl) {
      Array.from(bodyEl?.children ?? []).forEach((child) => {
         child.__tzgCleanup?.();
      });
   }

   static clearRenderedPanel(bodyEl) {
      ItineraryPanelContent.destroyRenderedPanelChildren(bodyEl);
      bodyEl?.replaceChildren();
   }

   static buildItineraryPanelContent(
   itinerary,
   zooHours,
   {
      onPanelRefresh = null,
      deps = {},
   } = {}
) {
      const {
         makeViewShell = ItineraryPanelViewState.makeItineraryPanelViewShell,
         makeActions = ActionsBar.makeActionsBar,
         createDateCard = DateCard.makeDateCard,
         buildSections = SectionConfigs.buildSectionConfigs,
         createSection = Section.makeSection,
         buildScheduleHandlers = ItineraryPanelScheduleHandlers.buildItineraryPanelScheduleHandlers,
         onAfterClear = null,
         setArrivalTime = ItineraryServiceTime.setItineraryArrivalTime,
         setDepartureTime = ItineraryServiceTime.setItineraryDepartureTime,
      } = deps;

      const fragment = document.createDocumentFragment();
      const {
         root,
         sharedHeader,
         listView,
         dayPlannerView,
      } = makeViewShell();

      sharedHeader.appendChild(
         makeActions({
            onAfterClear,
         })
      );

      const dateCard = createDateCard(itinerary);

      if (dateCard) {
         sharedHeader.appendChild(dateCard);
      }

      const scheduleHandlers = buildScheduleHandlers(itinerary, {
         onPanelRefresh,
         deps,
      });

      buildSections(itinerary, {
         onRemoveItem: scheduleHandlers.onRemoveItineraryItem,
      }).forEach((sectionConfig) => {
         listView.appendChild(
            createSection(sectionConfig)
         );
      });

      appendDayPlannerViewWithHours(
         dayPlannerView,
         zooHours,
         itinerary,
         {
            onArrivalTimeChange: async (arrivalTime) => {
               await setArrivalTime(arrivalTime);
               await onPanelRefresh?.();
            },
            onDepartureTimeChange: async (departureTime) => {
               await setDepartureTime(departureTime);
               await onPanelRefresh?.();
            },
         },
         {
            onPanelRefresh,
            deps,
         }
      );
      fragment.appendChild(root);

      return fragment;
   }

   static buildEmptyItineraryPanelContent(
   bodyEl,
   zooHours,
   {
      onPanelRefresh = null,
      deps = {},
   } = {}
) {
      const {
         makeViewShell = ItineraryPanelViewState.makeItineraryPanelViewShell,
         renderEmptyState = BuildOnly.renderBuildOnly,
      } = deps;

      const {
         root,
         listView,
         dayPlannerView,
      } = makeViewShell();

      renderEmptyState(listView);
      renderEmptyState(dayPlannerView);
      appendDayPlannerViewWithHours(dayPlannerView, zooHours, {}, {}, {
         onPanelRefresh,
         deps,
      });
      bodyEl.appendChild(root);
   }
}
