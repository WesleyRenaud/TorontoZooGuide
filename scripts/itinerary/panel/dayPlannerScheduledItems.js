import { parseClockTimeMinutes } from './dayPlannerSchedule.js';
import {
   buildGuardiansRows,
   buildWildRows,
} from './rows.js';

function getScheduledMaximumDuration(item) {
   const maximumDuration = Number(item?.maximum_duration);
   return Number.isFinite(maximumDuration) && maximumDuration > 0 ? maximumDuration : null;
}

function hasItineraryScheduleTimes(item) {
   return Boolean(item.start_time && item.end_time);
}

function buildScheduledItemRows(items, buildRows, getDurationMinutes) {
   return items.map((item, index) => {
      const [row] = buildRows([item]);
      const startMinutes = parseClockTimeMinutes(item.start_time);
      const maximumDuration = getDurationMinutes(item);

      return {
         index,
         item,
         row,
         startMinutes,
         maximumDuration,
      };
   }).filter((scheduledItem) => (
      scheduledItem.row
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

function mergeScheduledItemsByStart(scheduledItems = []) {
   return scheduledItems.reduce((itemsByStartMap, scheduledItem) => {
      const items = itemsByStartMap.get(scheduledItem.startMinutes) ?? [];
      items.push(scheduledItem);
      itemsByStartMap.set(scheduledItem.startMinutes, items);
      return itemsByStartMap;
   }, new Map());
}

export function buildScheduledItemRowsContext(
   {
      animals = [],
      attractions = [],
      guardiansTalks = [],
      wildEncounters = [],
   } = {},
   slotStarts = []
) {
   const slotStartSet = new Set(slotStarts);
   const guardiansTalkRows = buildScheduledItemRows(
      guardiansTalks,
      buildGuardiansRows,
      getScheduledMaximumDuration
   ).filter((scheduledItem) => slotStartSet.has(scheduledItem.startMinutes));
   const wildEncounterRows = buildScheduledItemRows(
      wildEncounters,
      buildWildRows,
      getScheduledMaximumDuration
   ).filter((scheduledItem) => slotStartSet.has(scheduledItem.startMinutes));
   const scheduledItems = [
      ...guardiansTalkRows,
      ...wildEncounterRows,
   ];

   return {
      itemsByStart: mergeScheduledItemsByStart(scheduledItems),
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
