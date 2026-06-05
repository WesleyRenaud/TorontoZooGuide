import { getPointPillStripPlacementBand } from '../dayPlannerTimelineMetrics.js';
import {
   makeOpenPill,
   makeScheduledPill,
} from './dayPlannerTimePill.js';
import { el } from '../dom.js';
import { normalizeVisitBoundaryEventTypes } from '../../itineraryEventTypes.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';
import {
   isScheduleItemModuleItemType,
   ScheduleItemKind,
} from '../../../shared/enums/scheduleItemKind.js';

const timelinePlacementsByGridLine = new WeakMap();
const SCHEDULED_PILL_DYNAMIC_GAP_PX = 12;
const SCHEDULED_PILL_DYNAMIC_MIN_WIDTH_PX = 112;

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

function findPlacementForStrip(
   gridLine,
   offsetFraction,
   horizontalOffsetIndex = 0
) {
   const offsetKey = String(offsetFraction);
   const horizontalOffsetKey = String(horizontalOffsetIndex);

   return getTimelinePlacements(gridLine).find((placement) => (
      String(placement.anchorOffsetFraction) === offsetKey
      && String(placement.horizontalOffsetIndex ?? 0) === horizontalOffsetKey
   )) ?? null;
}

function expandPlacementForScheduledPill(
   gridLine,
   offsetFraction,
   durationMinutes,
   horizontalOffsetIndex = 0
) {
   const existingPlacement = findPlacementForStrip(
      gridLine,
      offsetFraction,
      horizontalOffsetIndex
   );

   if (!existingPlacement) {
      return;
   }

   const durationFraction = durationMinutes / TIMELINE_SLOT_MINUTES;

   existingPlacement.durationFraction = Math.max(
      existingPlacement.durationFraction,
      durationFraction
   );
}

function readStripHorizontalOffsetIndex(strip) {
   const rawValue = strip.getAttribute?.('data-horizontal-offset-index')
      ?? strip.attributes?.['data-horizontal-offset-index']
      ?? '0';

   const parsedValue = Number.parseInt(rawValue, 10);

   return Number.isFinite(parsedValue) && parsedValue > 0 ? parsedValue : 0;
}

function readNumericAttribute(element, attributeName) {
   const rawValue = element.getAttribute?.(attributeName)
      ?? element.attributes?.[attributeName];
   const parsedValue = Number.parseFloat(rawValue);

   return Number.isFinite(parsedValue) ? parsedValue : null;
}

function readStripVisualRange(strip) {
   const rect = strip.getBoundingClientRect?.();

   if (
      rect
      && Number.isFinite(rect.top)
      && Number.isFinite(rect.bottom)
      && rect.bottom > rect.top
   ) {
      return {
         start: rect.top,
         end: rect.bottom,
      };
   }

   const start = readNumericAttribute(strip, 'data-visual-start-minutes');
   const end = readNumericAttribute(strip, 'data-visual-end-minutes');

   if (Number.isFinite(start) && Number.isFinite(end) && end > start) {
      return {
         start,
         end,
      };
   }

   return null;
}

function visualRangesOverlap(leftRange, rightRange) {
   return Boolean(
      leftRange
      && rightRange
      && leftRange.start < rightRange.end
      && rightRange.start < leftRange.end
   );
}

function findPrimaryPillInStrip(strip) {
   for (const child of strip.children ?? []) {
      if (
         child.classList?.contains('itinerary-day-scheduled-pill')
         || child.classList?.contains('itinerary-day-open-pill')
      ) {
         return child;
      }
   }

   return null;
}

function measurePillWidth(pill) {
   const rect = pill?.getBoundingClientRect?.();

   if (rect && Number.isFinite(rect.width) && rect.width > 0) {
      return rect.width;
   }

   if (Number.isFinite(pill?.offsetWidth) && pill.offsetWidth > 0) {
      return pill.offsetWidth;
   }

   return 0;
}

function getStripAvailableWidth(strip) {
   const gridLine = strip.parentElement;
   const rect = gridLine?.getBoundingClientRect?.();

   if (rect && Number.isFinite(rect.width) && rect.width > 0) {
      return Math.max(0, rect.width - 44);
   }

   return 0;
}

function measureStripHorizontalOffsetPx(strip) {
   const gridLineRect = strip.parentElement?.getBoundingClientRect?.();
   const stripRect = strip.getBoundingClientRect?.();

   if (
      gridLineRect
      && stripRect
      && Number.isFinite(gridLineRect.left)
      && Number.isFinite(stripRect.left)
   ) {
      return Math.max(0, stripRect.left - gridLineRect.left - 22);
   }

   return 0;
}

function applyDynamicScheduledOffset(strip, offsetPx) {
   const roundedOffset = Math.max(0, Math.round(offsetPx));

   strip.setAttribute('data-dynamic-horizontal-offset', 'true');
   strip.style.setProperty(
      '--itinerary-pill-dynamic-horizontal-offset',
      `${roundedOffset}px`
   );
}

function isScheduledPillStrip(strip) {
   return (
      strip.getAttribute?.('data-scheduled-column')
      ?? strip.attributes?.['data-scheduled-column']
   ) === 'true';
}

function isPillStrip(strip) {
   return strip?.classList?.contains('itinerary-day-pill-strip')
      || strip?.className === 'itinerary-day-pill-strip';
}

function compareScheduledStripEntriesForCompaction(leftEntry, rightEntry) {
   const leftStart = leftEntry.visualRange?.start ?? Number.POSITIVE_INFINITY;
   const rightStart = rightEntry.visualRange?.start ?? Number.POSITIVE_INFINITY;
   const startDelta = leftStart - rightStart;

   if (startDelta !== 0) {
      return startDelta;
   }

   const leftEnd = leftEntry.visualRange?.end ?? Number.POSITIVE_INFINITY;
   const rightEnd = rightEntry.visualRange?.end ?? Number.POSITIVE_INFINITY;
   const endDelta = leftEnd - rightEnd;

   if (endDelta !== 0) {
      return endDelta;
   }

   return leftEntry.horizontalOffsetIndex - rightEntry.horizontalOffsetIndex;
}

export function compactScheduledPillStripOffsets(timeline) {
   if (!timeline?.querySelectorAll) {
      return;
   }

   const strips = [...timeline.querySelectorAll('.itinerary-day-pill-strip')]
      .filter(isPillStrip)
      .map((strip) => ({
         strip,
         horizontalOffsetIndex: readStripHorizontalOffsetIndex(strip),
         isScheduled: isScheduledPillStrip(strip),
         visualRange: readStripVisualRange(strip),
      }));
   const dynamicOffsets = new Map();
   const placedEntries = strips.filter((entry) => !entry.isScheduled);

   placedEntries.forEach((entry) => {
      dynamicOffsets.set(entry.strip, measureStripHorizontalOffsetPx(entry.strip));
   });

   strips
      .filter((entry) => entry.isScheduled)
      .sort(compareScheduledStripEntriesForCompaction)
      .forEach((entry) => {
         const blockers = placedEntries.filter((candidate) => (
            candidate.horizontalOffsetIndex <= entry.horizontalOffsetIndex
            && visualRangesOverlap(candidate.visualRange, entry.visualRange)
         ));
         const requestedOffset = blockers.reduce((maxOffset, blocker) => {
            const blockerOffset = dynamicOffsets.get(blocker.strip) ?? 0;
            const blockerWidth = measurePillWidth(findPrimaryPillInStrip(blocker.strip));

            if (blockerWidth <= 0) {
               return maxOffset;
            }

            return Math.max(
               maxOffset,
               blockerOffset + blockerWidth + SCHEDULED_PILL_DYNAMIC_GAP_PX
            );
         }, 0);
         const availableWidth = getStripAvailableWidth(entry.strip);
         const clampedOffset = availableWidth > SCHEDULED_PILL_DYNAMIC_MIN_WIDTH_PX
            ? Math.min(
               requestedOffset,
               availableWidth - SCHEDULED_PILL_DYNAMIC_MIN_WIDTH_PX
            )
            : requestedOffset;

         dynamicOffsets.set(
            entry.strip,
            clampedOffset > 0
               ? clampedOffset
               : measureStripHorizontalOffsetPx(entry.strip)
         );

         if (clampedOffset > 0) {
            applyDynamicScheduledOffset(entry.strip, clampedOffset);
         }

         placedEntries.push(entry);
      });
}

export function scheduleScheduledPillStripCompaction(timeline) {
   if (!timeline) {
      return;
   }

   const compactTimeline = () => compactScheduledPillStripOffsets(timeline);
   const requestFrame = globalThis.requestAnimationFrame
      ?? globalThis.window?.requestAnimationFrame;

   if (typeof requestFrame === 'function') {
      requestFrame(compactTimeline);
   }
   else {
      compactTimeline();
   }

}

function findPillStrip(gridLine, offsetFraction = 0, horizontalOffsetIndex = 0) {
   const offsetKey = String(offsetFraction);
   const horizontalOffsetKey = String(horizontalOffsetIndex);

   for (const child of gridLine.children) {
      if (child.className !== 'itinerary-day-pill-strip') {
         continue;
      }

      const childOffset = child.getAttribute?.('data-offset-fraction')
         ?? child.attributes?.['data-offset-fraction']
         ?? '0';
      const childHorizontalOffset = String(readStripHorizontalOffsetIndex(child));

      if (
         childOffset === offsetKey
         && childHorizontalOffset === horizontalOffsetKey
      ) {
         return child;
      }
   }

   return null;
}

function resolveStripPlacementBand(
   gridLine,
   offsetFraction = 0,
   durationMinutes = null
) {
   const pointBand = getPointPillStripPlacementBand(gridLine, offsetFraction);

   if (Number.isFinite(durationMinutes) && durationMinutes > 0) {
      return {
         offsetFraction: pointBand.offsetFraction,
         durationFraction: Math.max(
            pointBand.durationFraction,
            durationMinutes / TIMELINE_SLOT_MINUTES
         ),
      };
   }

   return pointBand;
}

function getOrCreatePillStrip(
   gridLine,
   offsetFraction = 0,
   {
      durationMinutes = null,
      horizontalOffsetIndex = null,
   } = {}
) {
   const placementBand = resolveStripPlacementBand(
      gridLine,
      offsetFraction,
      durationMinutes
   );
   const placements = getTimelinePlacements(gridLine);
   const isPointPillStrip = !Number.isFinite(durationMinutes) || durationMinutes <= 0;
   const hasPresetHorizontalOffsetIndex = Number.isFinite(horizontalOffsetIndex);
   const resolvedHorizontalOffsetIndex = hasPresetHorizontalOffsetIndex
      ? horizontalOffsetIndex
      : computeTimelineHorizontalOffsetIndex(
         placements,
         placementBand.offsetFraction,
         placementBand.durationFraction
      );

   if (isPointPillStrip) {
      const existingStrip = findPillStrip(gridLine, offsetFraction, 0);

      if (existingStrip) {
         return existingStrip;
      }
   }
   else {
      const existingStrip = findPillStrip(
         gridLine,
         offsetFraction,
         resolvedHorizontalOffsetIndex
      );

      if (existingStrip) {
         return existingStrip;
      }
   }

   const pillStrip = el('div', 'itinerary-day-pill-strip');

   if (offsetFraction > 0) {
      pillStrip.setAttribute('data-offset-fraction', String(offsetFraction));
      pillStrip.style.setProperty(
         '--itinerary-pill-offset-fraction',
         String(offsetFraction)
      );
   }

   applyHorizontalOffsetIndex(pillStrip, resolvedHorizontalOffsetIndex);

   if (!isPointPillStrip) {
      markScheduledPillStrip(pillStrip);
   }

   registerTimelinePlacement(gridLine, {
      ...placementBand,
      anchorOffsetFraction: offsetFraction,
      horizontalOffsetIndex: resolvedHorizontalOffsetIndex,
   });
   gridLine.appendChild(pillStrip);

   return pillStrip;
}

function findFirstScheduledPillInStrip(strip) {
   for (const child of strip.children) {
      if (child.classList?.contains('itinerary-day-scheduled-pill')) {
         return child;
      }
   }

   return null;
}

function insertPointPillInStrip(strip, pill) {
   const firstScheduledPill = findFirstScheduledPillInStrip(strip);

   if (firstScheduledPill) {
      strip.insertBefore(pill, firstScheduledPill);
      return;
   }

   strip.appendChild(pill);
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

   const pill = makeOpenPill(label, pillOptions);

   if (!pill) {
      return;
   }

   insertPointPillInStrip(
      getOrCreatePillStrip(gridLine, offsetFraction),
      pill
   );
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

export function resolveGroupedScheduledPillOptions(
   scheduledItems = [],
   scheduleHandlers = {},
   strings = {}
) {
   const menuItems = mergeScheduledPillMenuItems(
      scheduledItems,
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

export function appendScheduledDurationPill(
   gridLine,
   {
      label,
      offsetFraction = 0,
      durationMinutes,
      startTime,
      endTime,
      menuItems = [],
      menuAriaLabel = '',
      onLabelClick = null,
      horizontalOffsetIndex = null,
      visualStartMinutes = null,
      visualEndMinutes = null,
   }
) {
   const pill = makeScheduledPill(label, durationMinutes, {
      startTime,
      endTime,
      menuItems,
      menuAriaLabel,
      onLabelClick,
   });

   if (!pill) {
      return;
   }

   const strip = getOrCreatePillStrip(gridLine, offsetFraction, {
      durationMinutes,
      horizontalOffsetIndex,
   });

   if (Number.isFinite(visualStartMinutes) && Number.isFinite(visualEndMinutes)) {
      strip.setAttribute('data-visual-start-minutes', String(visualStartMinutes));
      strip.setAttribute('data-visual-end-minutes', String(visualEndMinutes));
   }

   expandPlacementForScheduledPill(
      gridLine,
      offsetFraction,
      durationMinutes,
      readStripHorizontalOffsetIndex(strip)
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

   if (
      marker.kind === boundaries.arrival
      && typeof timeHandlers.onArrivalTimeChange === 'function'
   ) {
      return {
         menuAriaLabel: strings.arrivalTimeMenuAria,
         removeLabel: strings.remove,
         onRemove: () => timeHandlers.onArrivalTimeChange(''),
      };
   }

   if (
      marker.kind === boundaries.departure
      && typeof timeHandlers.onDepartureTimeChange === 'function'
   ) {
      return {
         menuAriaLabel: strings.departureTimeMenuAria,
         removeLabel: strings.remove,
         onRemove: () => timeHandlers.onDepartureTimeChange(''),
      };
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
