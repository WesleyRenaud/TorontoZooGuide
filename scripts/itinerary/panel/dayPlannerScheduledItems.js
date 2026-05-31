import { parseClockTimeMinutes } from './dayPlannerSchedule.js';
import {
   computeMarkerOffsetFraction,
   findTimelineAnchorSlot,
   findTimelineSlotEndMinutes,
} from './dayPlannerTimelineMarkers.js';
import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from './rows.js';

function getScheduledMaximumDuration(item) {
   const maximumDuration = Number(item?.maximum_duration);
   return Number.isFinite(maximumDuration) && maximumDuration > 0 ? maximumDuration : null;
}

function getDurationMinutesFromScheduleTimes(item) {
   return (
      parseClockTimeMinutes(item.end_time) - parseClockTimeMinutes(item.start_time)
   );
}

function hasItineraryScheduleTimes(item) {
   return Boolean(item.start_time && item.end_time);
}

function getScheduledItemLabel(item) {
   return String(item?.species || item?.name || '').trim();
}

function buildScheduledItemRows(items, buildRows, getDurationMinutes) {
   return items.map((item, index) => {
      const [row] = buildRows([item]);
      const startMinutes = parseClockTimeMinutes(item.start_time);
      const maximumDuration = getDurationMinutes(item);
      const label = getScheduledItemLabel(item);

      return {
         index,
         item,
         row,
         label,
         startMinutes,
         maximumDuration,
      };
   }).filter((scheduledItem) => (
      scheduledItem.row
      && scheduledItem.label
      && Number.isFinite(scheduledItem.startMinutes)
      && Number.isFinite(scheduledItem.maximumDuration)
   ));
}

function buildItineraryScheduledItemIndexes(items = []) {
   const indexes = new Set();

   items.forEach((item, index) => {
      if (!hasItineraryScheduleTimes(item)) {
         return;
      }

      indexes.add(index);
   });

   return indexes;
}

function mergeScheduledItemsByAnchorSlot(
   scheduledItems = [],
   slotStarts = [],
   closeMinutes = null
) {
   const sortedSlotStarts = [...slotStarts].sort((left, right) => left - right);

   return scheduledItems.reduce((itemsByAnchorMap, scheduledItem) => {
      const anchorSlot = findTimelineAnchorSlot(
         scheduledItem.startMinutes,
         sortedSlotStarts
      );

      if (!Number.isFinite(anchorSlot)) {
         return itemsByAnchorMap;
      }

      const slotEndMinutes = findTimelineSlotEndMinutes(
         anchorSlot,
         sortedSlotStarts,
         closeMinutes
      );
      const offsetFraction = computeMarkerOffsetFraction(
         scheduledItem.startMinutes,
         anchorSlot,
         slotEndMinutes
      );
      const items = itemsByAnchorMap.get(anchorSlot) ?? [];

      items.push({
         ...scheduledItem,
         offsetFraction,
      });
      itemsByAnchorMap.set(anchorSlot, items);

      return itemsByAnchorMap;
   }, new Map());
}

export function buildScheduledItemRowsContext(
   {
      animals = [],
      attractions = [],
      guardiansTalks = [],
      wildEncounters = [],
   } = {},
   slotStarts = [],
   closeMinutes = null
) {
   const guardiansTalkRows = buildScheduledItemRows(
      guardiansTalks,
      buildGuardiansRows,
      getScheduledMaximumDuration
   );
   const wildEncounterRows = buildScheduledItemRows(
      wildEncounters,
      buildWildRows,
      getScheduledMaximumDuration
   );
   const animalRows = buildScheduledItemRows(
      animals,
      buildAnimalRows,
      getDurationMinutesFromScheduleTimes
   );
   const attractionRows = buildScheduledItemRows(
      attractions,
      buildAttractionRows,
      getDurationMinutesFromScheduleTimes
   );
   const scheduledItems = [
      ...guardiansTalkRows,
      ...wildEncounterRows,
      ...animalRows,
      ...attractionRows,
   ];

   return {
      itemsByStart: mergeScheduledItemsByAnchorSlot(
         scheduledItems,
         slotStarts,
         closeMinutes
      ),
      scheduledAnimalIndexes: buildItineraryScheduledItemIndexes(animals),
      scheduledAttractionIndexes: buildItineraryScheduledItemIndexes(attractions),
      scheduledGuardiansTalkIndexes: new Set(
         guardiansTalkRows.map((scheduledItem) => scheduledItem.index)
      ),
      scheduledWildEncounterIndexes: new Set(
         wildEncounterRows.map((scheduledItem) => scheduledItem.index)
      ),
   };
}

export function buildScheduledItinerary(
   itinerary = {},
   {
      scheduledAnimalIndexes = new Set(),
      scheduledAttractionIndexes = new Set(),
      scheduledGuardiansTalkIndexes = new Set(),
      scheduledWildEncounterIndexes = new Set(),
   } = {}
) {
   return {
      animals: itinerary.animals.filter((_, index) => (
         scheduledAnimalIndexes.has(index)
      )),
      attractions: itinerary.attractions.filter((_, index) => (
         scheduledAttractionIndexes.has(index)
      )),
      guardiansTalks: itinerary.guardiansTalks.filter((_, index) => (
         scheduledGuardiansTalkIndexes.has(index)
      )),
      wildEncounters: itinerary.wildEncounters.filter((_, index) => (
         scheduledWildEncounterIndexes.has(index)
      )),
   };
}

export function buildUnscheduledItinerary(
   itinerary = {},
   {
      scheduledAnimalIndexes = new Set(),
      scheduledAttractionIndexes = new Set(),
      scheduledGuardiansTalkIndexes = new Set(),
      scheduledWildEncounterIndexes = new Set(),
   } = {}
) {
   return {
      ...itinerary,
      animals: (itinerary.animals ?? []).filter((_, index) => (
         !scheduledAnimalIndexes.has(index)
      )),
      attractions: (itinerary.attractions ?? []).filter((_, index) => (
         !scheduledAttractionIndexes.has(index)
      )),
      guardiansTalks: (itinerary.guardiansTalks ?? []).filter((_, index) => (
         !scheduledGuardiansTalkIndexes.has(index)
      )),
      wildEncounters: (itinerary.wildEncounters ?? []).filter((_, index) => (
         !scheduledWildEncounterIndexes.has(index)
      )),
   };
}
