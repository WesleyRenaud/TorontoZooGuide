import { hasBulkScheduleAnimalsNotEnoughTimeIssue } from './bulkScheduleAnimalsNotEnoughTimeConfirmation.js';
import { makeActionsBar } from './components/actionsBar.js';
import { renderBuildOnly } from './components/buildOnly.js';
import { makeDateCard } from './components/dateCard.js';
import { makeDayPlannerPreview } from './components/dayPlanner.js';
import { getItineraryPanelMountEl } from './components/popup.js';
import { makeSection } from './components/section.js';
import { setPendingDayPlannerActionFeedback } from './dayPlannerActionFeedback.js';
import { showFixedTimeItemLongWaitConfirmation } from './fixedTimeItemLongWaitConfirmation.js';
import {
   buildConfirmedOptionsFromBuildWarnings,
   hasMultipleItineraryBuildWarnings,
   showItineraryBuildWarningsConfirmation,
} from './itineraryBuildWarningsConfirmation.js';
import { requiresFixedTimeItemLongWaitConfirmation } from '../itineraryErrorTypes.js';
import {
   buildItineraryPanelScheduleHandlers,
   openScheduleItemModule,
} from './itineraryPanelScheduleHandlers.js';
import { makeItineraryPanelViewShell } from './itineraryPanelViewState.js';
import {
   bulkScheduleAnimals,
   unscheduleAllItineraryItems,
} from '../itineraryService.js';
import {
   setItineraryArrivalTime,
   setItineraryDepartureTime,
} from '../itineraryServiceTime.js';
import { buildSchedulableEventTypes } from './scheduleItemTypes.js';
import { buildSectionConfigs } from './sectionConfigs.js';
import { APP_STRINGS } from '../../strings.js';

export function destroyRenderedPanelChildren(bodyEl) {
   Array.from(bodyEl?.children ?? []).forEach((child) => {
      child.__tzgCleanup?.();
   });
}

export function clearRenderedPanel(bodyEl) {
   destroyRenderedPanelChildren(bodyEl);
   bodyEl?.replaceChildren();
}

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
      openModule = openScheduleItemModule,
      bulkSchedule = bulkScheduleAnimals,
      unscheduleAll = unscheduleAllItineraryItems,
      hasNotEnoughTimeIssue = hasBulkScheduleAnimalsNotEnoughTimeIssue,
      hasMultipleBuildWarnings = hasMultipleItineraryBuildWarnings,
      showBuildWarningsConfirmation = showItineraryBuildWarningsConfirmation,
      requiresLongWaitConfirmation = requiresFixedTimeItemLongWaitConfirmation,
      showLongWaitConfirmation = showFixedTimeItemLongWaitConfirmation,
      setActionFeedback = setPendingDayPlannerActionFeedback,
      buildEventTypes = buildSchedulableEventTypes,
      buildScheduleHandlers = buildItineraryPanelScheduleHandlers,
      makeDayPlanner = makeDayPlannerPreview,
      genericErrorMessage = APP_STRINGS.itinerary.errors.generic,
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
                        APP_STRINGS.itinerary.confirmation
                           .bulkScheduleAnimalsNotEnoughTimeMessage
                     ),
                  });
                  return;
               }

               await queueActionFeedback({
                  variant: 'success',
                  message: APP_STRINGS.itinerary.dayPlanner.rebuildScheduleSuccess,
               });
            };

            const mountEl = getItineraryPanelMountEl() ?? document.body;
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
                        buildConfirmedOptionsFromBuildWarnings(result.issues)
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
                  message: APP_STRINGS.itinerary.dayPlanner.unscheduleAllSuccess,
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

export function buildItineraryPanelContent(
   itinerary,
   zooHours,
   {
      onPanelRefresh = null,
      deps = {},
   } = {}
) {
   const {
      makeViewShell = makeItineraryPanelViewShell,
      makeActions = makeActionsBar,
      createDateCard = makeDateCard,
      buildSections = buildSectionConfigs,
      createSection = makeSection,
      buildScheduleHandlers = buildItineraryPanelScheduleHandlers,
      onAfterClear = null,
      setArrivalTime = setItineraryArrivalTime,
      setDepartureTime = setItineraryDepartureTime,
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

export function buildEmptyItineraryPanelContent(
   bodyEl,
   zooHours,
   {
      onPanelRefresh = null,
      deps = {},
   } = {}
) {
   const {
      makeViewShell = makeItineraryPanelViewShell,
      renderEmptyState = renderBuildOnly,
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
