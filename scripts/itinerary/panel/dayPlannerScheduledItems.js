import { parseClockTimeMinutes } from './dayPlannerSchedule.js';
import {
   buildGuardiansRows,
   buildWildRows,
} from './rows.js';

function getScheduledMaximumDuration(item) {
   const maximumDuration = Number(item?.maximum_duration);
   return Number.isFinite(maximumDuration) && maximumDuration > 0 ? maximumDuration : null;
}

function buildScheduledItemRows(items, buildRows) {
   return items.map((item, index) => {
      const [row] = buildRows([item]);
      const maximumDuration = getScheduledMaximumDuration(item);
      return {
         index,
         item,
         row,
         startMinutes: parseClockTimeMinutes(item?.start_time),
         maximumDuration,
      };
   }).filter((scheduledItem) => (
      scheduledItem.row
      && Number.isFinite(scheduledItem.startMinutes)
      && Number.isFinite(scheduledItem.maximumDuration)
   ));
}

export function buildScheduledItemRowsContext(
   {
      guardiansTalks = [],
      wildEncounters = [],
   } = {},
   slotStarts = []
) {
   const slotStartSet = new Set(slotStarts);
   const guardiansTalkRows = buildScheduledItemRows(guardiansTalks, buildGuardiansRows)
      .filter((scheduledItem) => slotStartSet.has(scheduledItem.startMinutes));
   const wildEncounterRows = buildScheduledItemRows(wildEncounters, buildWildRows)
      .filter((scheduledItem) => slotStartSet.has(scheduledItem.startMinutes));
   const scheduledItems = [
      ...guardiansTalkRows,
      ...wildEncounterRows,
   ];
   const itemsByStart = scheduledItems.reduce((itemsByStartMap, scheduledItem) => {
      const items = itemsByStartMap.get(scheduledItem.startMinutes) ?? [];
      items.push(scheduledItem);
      itemsByStartMap.set(scheduledItem.startMinutes, items);
      return itemsByStartMap;
   }, new Map());

   return {
      itemsByStart,
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
      scheduledGuardiansTalkIndexes = new Set(),
      scheduledWildEncounterIndexes = new Set(),
   } = {}
) {
   return {
      animals: [],
      attractions: [],
      guardiansTalks: (itinerary.guardiansTalks ?? []).filter((_, index) => (
         scheduledGuardiansTalkIndexes.has(index)
      )),
      wildEncounters: (itinerary.wildEncounters ?? []).filter((_, index) => (
         scheduledWildEncounterIndexes.has(index)
      )),
   };
}

export function buildUnscheduledItinerary(
   itinerary = {},
   {
      scheduledGuardiansTalkIndexes = new Set(),
      scheduledWildEncounterIndexes = new Set(),
   } = {}
) {
   return {
      ...itinerary,
      guardiansTalks: (itinerary.guardiansTalks ?? []).filter((_, index) => (
         !scheduledGuardiansTalkIndexes.has(index)
      )),
      wildEncounters: (itinerary.wildEncounters ?? []).filter((_, index) => (
         !scheduledWildEncounterIndexes.has(index)
      )),
   };
}
