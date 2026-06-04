import {
   removeItemFromItineraryRequest,
   unscheduleItineraryItemRequest,
} from '../../api/itineraryApi.js';
import {
   hasBulkScheduleAnimalsNotEnoughTimeIssue,
   showBulkScheduleAnimalsNotEnoughTimeNotice,
} from './bulkScheduleAnimalsNotEnoughTimeConfirmation.js';
import { makeActionsBar } from './components/actionsBar.js';
import { renderBuildOnly } from './components/buildOnly.js';
import { makeDateCard } from './components/dateCard.js';
import {
   makeDayPlannerPreview,
   makeItineraryPanelViews,
} from './components/dayPlanner.js';
import { showScheduleItemModule } from './components/scheduleItemModule.js';
import { makeSection } from './components/section.js';
import { clearItineraryDraftStorage } from '../draftStorage.js';
import { removeAnimalFromItineraryAnimalDraft } from '../draftStorage.js';
import { requiresRemoveItineraryItemConfirmation } from '../itineraryEventTypes.js';
import {
   getItineraryPanelViewFromUrl,
   setItineraryPanelViewInUrl,
} from './itineraryPanelViewUrl.js';
import {
   bulkScheduleAnimals,
   clearItinerary,
   getItinerary,
   getZooHours,
   isItineraryEmpty,
   setItineraryArrivalTime,
   setItineraryDepartureTime,
} from '../itineraryService.js';
import { showRemoveItineraryItemConfirmation } from './removeItineraryItemConfirmation.js';
import { buildSchedulableEventTypes } from './scheduleItemTypes.js';
import { buildSectionConfigs } from './sectionConfigs.js';
import { showScheduleItemNotice } from './showScheduleItemNotice.js';
import { APP_STRINGS } from '../../strings.js';
import { resolveEffectiveItineraryHoursDateIso } from '../visitDateEarliest.js';

let latestRenderToken = 0;
let activePanelView = getItineraryPanelViewFromUrl();

function destroyRenderedPanelChildren(bodyEl) {
   Array.from(bodyEl?.children ?? []).forEach((child) => {
      child.__tzgCleanup?.();
   });
}

function clearRenderedPanel(bodyEl) {
   destroyRenderedPanelChildren(bodyEl);
   bodyEl?.replaceChildren();
}

async function clearStoredItinerary() {
   try {
      await clearItinerary();
      clearItineraryDraftStorage();
   }
   catch (err) {
      console.error('Failed to clear itinerary:', err);
   }
}

function openScheduleItemModule({
   itinerary = {},
   eventTypes = [],
   onScheduled = null,
   preselectedRow = null,
} = {}) {
   showScheduleItemModule({
      itinerary,
      eventTypes,
      onScheduled,
      preselectedRow,
   });
}

function makePanelViewShell() {
   return makeItineraryPanelViews({
      activeView: activePanelView,
      onViewChange: (view) => {
         activePanelView = view;
         setItineraryPanelViewInUrl(view);
      },
   });
}

function buildItineraryPanelScheduleHandlers(
   itinerary = {},
   { onPanelRefresh = null } = {}
) {
   return {
      onScheduleItineraryItem: (pick) => {
         openScheduleItemModule({
            itinerary,
            eventTypes: buildSchedulableEventTypes(itinerary.itineraryConfig),
            onScheduled: onPanelRefresh,
            preselectedRow: pick?.row ?? null,
         });
      },
      onUnscheduleItineraryItem: async ({ itemType, key }) => {
         await unscheduleItineraryItemRequest({ itemType, key });

         if (typeof onPanelRefresh === 'function') {
            await onPanelRefresh();
         }
      },
      onRemoveItineraryItem: ({ itemType, key }) => {
         const performRemove = async () => {
            await removeItemFromItineraryRequest({ itemType, key });
            removeAnimalFromItineraryAnimalDraft(itemType, key);

            if (typeof onPanelRefresh === 'function') {
               await onPanelRefresh();
            }
         };

         if (requiresRemoveItineraryItemConfirmation(itemType, itinerary.itineraryConfig)) {
            showRemoveItineraryItemConfirmation({
               onConfirm: performRemove,
            });
            return;
         }

         void performRemove();
      },
   };
}

function appendDayPlannerViewWithHours(
   dayPlannerView,
   zooHours,
   itinerary = {},
   timeHandlers = {},
   { onPanelRefresh = null } = {}
) {
   const scheduleHandlers = buildItineraryPanelScheduleHandlers(itinerary, {
      onPanelRefresh,
   });

   dayPlannerView.appendChild(
      makeDayPlannerPreview(zooHours, itinerary, timeHandlers, {
         onScheduleItemClick: () => {
            openScheduleItemModule({
               itinerary,
               eventTypes: buildSchedulableEventTypes(itinerary.itineraryConfig),
               onScheduled: onPanelRefresh,
            });
         },
         onBulkScheduleAnimalsClick: async () => {
            try {
               const { issues } = await bulkScheduleAnimals();

               if (typeof onPanelRefresh === 'function') {
                  await onPanelRefresh();
               }

               if (hasBulkScheduleAnimalsNotEnoughTimeIssue(issues)) {
                  showBulkScheduleAnimalsNotEnoughTimeNotice();
               }
            }
            catch (err) {
               console.error('Failed to bulk schedule animals:', err);
               showScheduleItemNotice(
                  err?.message || APP_STRINGS.itinerary.errors.generic
               );
            }
         },
         scheduleHandlers,
      })
   );
}

function buildItineraryPanelContent(bodyEl, itinerary, zooHours) {
   const fragment = document.createDocumentFragment();
   const {
      root,
      sharedHeader,
      listView,
      dayPlannerView,
   } = makePanelViewShell();

   sharedHeader.appendChild(
      makeActionsBar({
         onAfterClear: clearStoredItinerary,
      })
   );

   const dateCard = makeDateCard(itinerary);

   if (dateCard) {
      sharedHeader.appendChild(dateCard);
   }

   const scheduleHandlers = buildItineraryPanelScheduleHandlers(itinerary, {
      onPanelRefresh: () => renderItineraryPanelInto(bodyEl),
   });

   buildSectionConfigs(itinerary, {
      onRemoveItem: scheduleHandlers.onRemoveItineraryItem,
   }).forEach((sectionConfig) => {
      listView.appendChild(
         makeSection(sectionConfig)
      );
   });

   appendDayPlannerViewWithHours(
      dayPlannerView,
      zooHours,
      itinerary,
      {
         onArrivalTimeChange: async (arrivalTime) => {
            await setItineraryArrivalTime(arrivalTime);
            await renderItineraryPanelInto(bodyEl);
         },
         onDepartureTimeChange: async (departureTime) => {
            await setItineraryDepartureTime(departureTime);
            await renderItineraryPanelInto(bodyEl);
         },
      },
      {
         onPanelRefresh: () => renderItineraryPanelInto(bodyEl),
      }
   );
   fragment.appendChild(root);

   return fragment;
}

function buildEmptyItineraryPanelContent(bodyEl, zooHours) {
   const {
      root,
      listView,
      dayPlannerView,
   } = makePanelViewShell();

   renderBuildOnly(listView);
   renderBuildOnly(dayPlannerView);
   appendDayPlannerViewWithHours(dayPlannerView, zooHours, {}, {}, {
      onPanelRefresh: () => renderItineraryPanelInto(bodyEl),
   });
   bodyEl.appendChild(root);
}

export async function renderItineraryPanelInto(bodyEl) {
   if (!bodyEl) {
      return;
   }

   const renderToken = ++latestRenderToken;
   const itinerary = await getItinerary();
   const hoursDate = await resolveEffectiveItineraryHoursDateIso(itinerary);
   const zooHours = await getZooHours(hoursDate);

   if (renderToken !== latestRenderToken) {
      return;
   }

   clearRenderedPanel(bodyEl);

   if (!itinerary || isItineraryEmpty(itinerary)) {
      buildEmptyItineraryPanelContent(bodyEl, zooHours);
      return;
   }

   bodyEl.appendChild(
      buildItineraryPanelContent(bodyEl, itinerary, zooHours)
   );
}
