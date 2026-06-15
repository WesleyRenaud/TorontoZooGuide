import { getPointPillStripPlacementBand } from '../dayPlannerTimelineMetrics.js';
import { el } from '../dom.js';
import { normalizeVisitBoundaryEventTypes } from '../../itineraryEventTypes.js';
import {
   makeBoundaryMarker,
   makeOpenPill,
} from './openTimelinePill.js';
import { makeScheduledPill } from './scheduledTimelinePill.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';
import {
   isScheduleItemModuleItemType,
   ScheduleItemKind,
} from '../../../shared/enums/scheduleItemKind.js';

const timelinePlacementsByGridLine = new WeakMap();

function getTimelinePlacements(gridLine) {
   let placements = timelinePlacementsByGridLine.get(gridLine);

   if (!placements) {
      placements = [];
      timelinePlacementsByGridLine.set(gridLine, placements);
   }

   return placements;
}

export function computeTimelineHorizontalOffsetIndex(
   placements = [],
   offsetFraction = 0,
   durationFraction = 0
) {
   const placementStart = offsetFraction;
   const placementEnd = offsetFraction + durationFraction;
   let maxIndex = -1;

   for (const placement of placements) {
      const placedEnd = placement.offsetFraction + placement.durationFraction;

      if (placementStart < placedEnd && placement.offsetFraction < placementEnd) {
         maxIndex = Math.max(maxIndex, placement.horizontalOffsetIndex);
      }
   }

   return maxIndex >= 0 ? maxIndex + 1 : 0;
}

function applyHorizontalOffsetIndex(element, horizontalOffsetIndex) {
   element.setAttribute('data-horizontal-offset-index', String(horizontalOffsetIndex));
   element.style.setProperty(
      '--itinerary-pill-horizontal-offset-index',
      String(horizontalOffsetIndex)
   );
}

function markScheduledPillStrip(pillStrip) {
   pillStrip.setAttribute('data-scheduled-column', 'true');
}

function registerTimelinePlacement(
   gridLine,
   {
      offsetFraction,
      durationFraction,
      horizontalOffsetIndex,
      anchorOffsetFraction,
   }
) {
   getTimelinePlacements(gridLine).push({
      offsetFraction,
      durationFraction,
      horizontalOffsetIndex,
      anchorOffsetFraction,
   });
}

function isScheduledPillStrip(strip) {
   return (
      strip.getAttribute?.('data-scheduled-column')
      ?? strip.attributes?.['data-scheduled-column']
   ) === 'true';
}

function findPointPillStrip(gridLine, offsetFraction = 0) {
   const offsetKey = String(offsetFraction);

   for (const child of gridLine.children) {
      if (child.className !== 'itinerary-day-pill-strip' || isScheduledPillStrip(child)) {
         continue;
      }

      const childOffset = child.getAttribute?.('data-offset-fraction')
         ?? child.attributes?.['data-offset-fraction']
         ?? '0';

      if (childOffset === offsetKey) {
         return child;
      }
   }

   return null;
}

function resolveStripPlacementBand(
   gridLine,
   offsetFraction = 0,
   durationMinutes = null,
   slotSpanMinutes = TIMELINE_SLOT_MINUTES
) {
   const pointBand = getPointPillStripPlacementBand(gridLine, offsetFraction);

   if (Number.isFinite(durationMinutes) && durationMinutes > 0) {
      const slotSpan = Number.isFinite(slotSpanMinutes) && slotSpanMinutes > 0
         ? slotSpanMinutes
         : TIMELINE_SLOT_MINUTES;

      return {
         offsetFraction: pointBand.offsetFraction,
         durationFraction: durationMinutes / slotSpan,
      };
   }

   return pointBand;
}

function getOrCreatePointPillStrip(gridLine, offsetFraction = 0) {
   const existingStrip = findPointPillStrip(gridLine, offsetFraction);

   if (existingStrip) {
      return existingStrip;
   }

   const placementBand = resolveStripPlacementBand(gridLine, offsetFraction);
   const pillStrip = el('div', 'itinerary-day-pill-strip');

   if (offsetFraction > 0) {
      pillStrip.setAttribute('data-offset-fraction', String(offsetFraction));
      pillStrip.style.setProperty(
         '--itinerary-pill-offset-fraction',
         String(offsetFraction)
      );
   }

   applyHorizontalOffsetIndex(pillStrip, 0);
   registerTimelinePlacement(gridLine, {
      ...placementBand,
      anchorOffsetFraction: offsetFraction,
      horizontalOffsetIndex: 0,
   });
   gridLine.appendChild(pillStrip);

   return pillStrip;
}

function applyPointPillStripPlacement(pillStrip, placement = '') {
   if (!pillStrip || !placement) {
      return;
   }

   pillStrip.setAttribute('data-visit-boundary-placement', placement);
}

function createScheduledPillStrip(
   gridLine,
   offsetFraction = 0,
   durationMinutes = 0,
   slotSpanMinutes = TIMELINE_SLOT_MINUTES
) {
   const placementBand = resolveStripPlacementBand(
      gridLine,
      offsetFraction,
      durationMinutes,
      slotSpanMinutes
   );
   const pillStrip = el('div', 'itinerary-day-pill-strip');

   if (offsetFraction > 0) {
      pillStrip.setAttribute('data-offset-fraction', String(offsetFraction));
      pillStrip.style.setProperty(
         '--itinerary-pill-offset-fraction',
         String(offsetFraction)
      );
   }

   markScheduledPillStrip(pillStrip);
   registerTimelinePlacement(gridLine, {
      ...placementBand,
      anchorOffsetFraction: offsetFraction,
      horizontalOffsetIndex: 0,
   });
   gridLine.appendChild(pillStrip);

   return pillStrip;
}

export function appendTimelinePill(
   gridLine,
   label,
   offsetFraction = 0,
   pillOptions = {}
) {
   if (!label) {
      return;
   }

   const pill = pillOptions.visitBoundaryPlacement
      ? makeBoundaryMarker(label, pillOptions)
      : makeOpenPill(label, pillOptions);

   if (!pill) {
      return;
   }

   const strip = getOrCreatePointPillStrip(gridLine, offsetFraction);

   applyPointPillStripPlacement(strip, pillOptions.visitBoundaryPlacement);
   insertPointPillInStrip(strip, pill);
}

function insertPointPillInStrip(strip, pill) {
   strip.appendChild(pill);
}

function buildScheduledPillMenuItems(
   scheduledItem = {},
   scheduleHandlers = {},
   strings = {}
) {
   const {
      scheduleItemKind,
      scheduleItemKey,
      scheduleItemEventType,
   } = scheduledItem;
   const menuItems = [];

   if (
      typeof scheduleHandlers.onUnscheduleItineraryItem === 'function'
      && scheduleItemKind !== ScheduleItemKind.EVENT.kind
   ) {
      if (
         isScheduleItemModuleItemType(scheduleItemKind)
         && scheduleItemKey
      ) {
         menuItems.push({
            label: strings.unschedule,
            onAction: () => scheduleHandlers.onUnscheduleItineraryItem({
               itemType: scheduleItemKind,
               key: scheduleItemKey,
            }),
         });
      }
   }

   if (typeof scheduleHandlers.onRemoveItineraryItem === 'function') {
      if (
         scheduleItemKind === ScheduleItemKind.EVENT.kind
         && scheduleItemEventType
      ) {
         menuItems.push({
            label: strings.remove,
            onAction: () => scheduleHandlers.onRemoveItineraryItem({
               itemType: scheduleItemEventType,
               key: '',
            }),
         });
      }
      else if (scheduleItemKey) {
         menuItems.push({
            label: strings.remove,
            onAction: () => scheduleHandlers.onRemoveItineraryItem({
               itemType: scheduleItemKind,
               key: scheduleItemKey,
            }),
         });
      }
   }

   return menuItems;
}

export function resolveScheduledPillOptions(
   scheduledItem = {},
   scheduleHandlers = {},
   strings = {}
) {
   const menuItems = buildScheduledPillMenuItems(
      scheduledItem,
      scheduleHandlers,
      strings
   );

   if (!menuItems.length) {
      return {};
   }

   return {
      menuAriaLabel: strings.scheduledItemMenuAria,
      menuItems,
   };
}

function mergeScheduledPillMenuItems(items = [], scheduleHandlers = {}, strings = {}) {
   const menuItems = [];

   items.forEach((scheduledItem) => {
      menuItems.push(
         ...buildScheduledPillMenuItems(scheduledItem, scheduleHandlers, strings)
      );
   });

   return menuItems;
}

export function buildGroupedScheduledPillItems(
   scheduledItems = [],
   scheduleHandlers = {},
   strings = {},
   resolveItemLabelClick = () => null
) {
   return scheduledItems.map((scheduledItem) => ({
      label: scheduledItem.label,
      startTime: scheduledItem.item?.start_time ?? '',
      endTime: scheduledItem.item?.end_time ?? '',
      onLabelClick: resolveItemLabelClick(scheduledItem),
      menuItems: buildScheduledPillMenuItems(
         scheduledItem,
         scheduleHandlers,
         strings
      ),
   }));
}

export function resolveGroupedScheduledPillOptions(
   scheduledItems = [],
   scheduleHandlers = {},
   strings = {},
   resolveItemLabelClick = () => null
) {
   const groupItems = buildGroupedScheduledPillItems(
      scheduledItems,
      scheduleHandlers,
      strings,
      resolveItemLabelClick
   );
   const menuItems = mergeScheduledPillMenuItems(
      scheduledItems,
      scheduleHandlers,
      strings
   );

   if (!menuItems.length && groupItems.length <= 1) {
      return {};
   }

   return {
      menuAriaLabel: strings.scheduledItemMenuAria,
      menuItems,
      groupItems,
   };
}

export function appendScheduledDurationPill(
   gridLine,
   {
      label,
      offsetFraction = 0,
      durationMinutes,
      displayDurationMinutes = durationMinutes,
      slotSpanMinutes = TIMELINE_SLOT_MINUTES,
      startTime,
      endTime,
      groupItems = [],
      menuItems = [],
      menuAriaLabel = '',
      onLabelClick = null,
   }
) {
   const pill = makeScheduledPill(label, durationMinutes, {
      startTime,
      endTime,
      groupItems,
      menuItems,
      menuAriaLabel,
      onLabelClick,
      slotSpanMinutes,
      displayDurationMinutes,
   });

   if (!pill) {
      return;
   }

   const strip = createScheduledPillStrip(
      gridLine,
      offsetFraction,
      displayDurationMinutes,
      slotSpanMinutes
   );

   strip.appendChild(pill);
}

function resolveTimePillOptions(
   marker,
   timeHandlers = {},
   strings = {},
   visitBoundaryEventTypes = {}
) {
   const boundaries = normalizeVisitBoundaryEventTypes(visitBoundaryEventTypes);

   if (marker.kind === boundaries.arrival) {
      const options = {
         menuAriaLabel: strings.arrivalTimeMenuAria,
         removeLabel: strings.remove,
         visitBoundaryPlacement: 'ends-at-anchor',
      };

      if (typeof timeHandlers.onArrivalTimeChange === 'function') {
         options.onRemove = () => timeHandlers.onArrivalTimeChange('');
      }

      return options;
   }

   if (marker.kind === boundaries.departure) {
      const options = {
         menuAriaLabel: strings.departureTimeMenuAria,
         removeLabel: strings.remove,
         visitBoundaryPlacement: 'starts-at-anchor',
      };

      if (typeof timeHandlers.onDepartureTimeChange === 'function') {
         options.onRemove = () => timeHandlers.onDepartureTimeChange('');
      }

      return options;
   }

   return {};
}

export function appendItineraryTimeMarkers(
   gridLine,
   markersByAnchorSlot,
   slotStart,
   timeHandlers = {},
   strings = {},
   visitBoundaryEventTypes = {}
) {
   (markersByAnchorSlot.get(slotStart) ?? []).forEach((marker) => {
      appendTimelinePill(
         gridLine,
         marker.label,
         marker.offsetFraction,
         resolveTimePillOptions(
            marker,
            timeHandlers,
            strings,
            visitBoundaryEventTypes
         )
      );
   });
}

export function computeStripHorizontalOffsetIndex(
   placedStrips,
   offsetFraction,
   pointPillVerticalSpanFraction
) {
   return computeTimelineHorizontalOffsetIndex(
      placedStrips.map((strip) => ({
         offsetFraction: strip.offsetFraction,
         durationFraction: pointPillVerticalSpanFraction,
         horizontalOffsetIndex: strip.horizontalOffsetIndex,
      })),
      offsetFraction,
      pointPillVerticalSpanFraction
   );
}

export const computeSpanHorizontalOffsetIndex = computeTimelineHorizontalOffsetIndex;
