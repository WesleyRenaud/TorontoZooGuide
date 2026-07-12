import { getAnimalViewingWalkNodeId } from './components/scheduledPillViewingWalkNode.js';
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
import { formatItineraryEventTypeLabel } from './scheduleItemEventLabels.js';
import {
   getAnimalId,
   getAnimalTitleLine,
} from '../selectors/animalSelector/model.js';
import { getAttractionId } from '../selectors/attractionSelector/model.js';
import { getGuardiansTalkId } from '../selectors/guardiansTalkSelector/model.js';
import { getWildEncounterId } from '../selectors/wildEncounterSelector/model.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import {
   buildAnimalViewingSpotKey,
   buildUniqueSpeciesExhibitEntries,
} from '../speciesExhibitKey.js';

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

function isActiveScheduledOccurrence(item) {
   return item?.is_deleted !== true;
}

function getScheduledItemLabel(item) {
   if (item?.species) {
      return getAnimalTitleLine(item);
   }

   return String(item?.name || '').trim();
}

function getItineraryEventType(item) {
   return String(item?.event_type ?? '').trim();
}

function buildGenericEventScheduledRows(events = []) {
   return events.map((event, index) => {
      const eventType = getItineraryEventType(event);
      const startMinutes = parseClockTimeMinutes(event.start_time);
      const endMinutes = parseClockTimeMinutes(event.end_time);
      const maximumDuration = getDurationMinutesFromScheduleTimes(event);
      const label = formatItineraryEventTypeLabel(eventType);

      return {
         index,
         item: event,
         row: null,
         label,
         startMinutes,
         endMinutes,
         maximumDuration,
         scheduleItemKind: ScheduleItemKind.EVENT.kind,
         scheduleItemEventType: eventType,
         scheduleItemKey: '',
      };
   }).filter((scheduledItem) => (
      scheduledItem.label
      && scheduledItem.scheduleItemEventType
      && Number.isFinite(scheduledItem.startMinutes)
      && Number.isFinite(scheduledItem.endMinutes)
      && Number.isFinite(scheduledItem.maximumDuration)
   ));
}

function buildScheduledItemRows(items, buildRows, getDurationMinutes) {
   return items.map((item, index) => {
      const [row] = buildRows([item]);
      const startMinutes = parseClockTimeMinutes(item.start_time);
      const endMinutes = parseClockTimeMinutes(item.end_time);
      const maximumDuration = getDurationMinutes(item);
      const label = getScheduledItemLabel(item);

      return {
         index,
         item,
         row,
         label,
         startMinutes,
         endMinutes,
         maximumDuration,
      };
   }).filter((scheduledItem) => (
      scheduledItem.row
      && scheduledItem.label
      && Number.isFinite(scheduledItem.startMinutes)
      && Number.isFinite(scheduledItem.endMinutes)
      && Number.isFinite(scheduledItem.maximumDuration)
   ));
}

function buildScheduledAnimalRows(animals = []) {
   return buildUniqueSpeciesExhibitEntries(animals, {
      includeAnimal: hasItineraryScheduleTimes,
      buildKey: buildAnimalViewingSpotKey,
      requireExhibit: false,
   }).map(({ item, index }) => {
      const [row] = buildAnimalRows([item]);
      const startMinutes = parseClockTimeMinutes(item.start_time);
      const endMinutes = parseClockTimeMinutes(item.end_time);
      const maximumDuration = getDurationMinutesFromScheduleTimes(item);
      const label = getScheduledItemLabel(item);
      const viewingWalkNodeId = getAnimalViewingWalkNodeId(item);

      return {
         index,
         item,
         row,
         label,
         startMinutes,
         endMinutes,
         maximumDuration,
         viewingWalkNodeId,
      };
   }).filter((scheduledItem) => (
      scheduledItem.row
      && scheduledItem.label
      && Number.isFinite(scheduledItem.startMinutes)
      && Number.isFinite(scheduledItem.endMinutes)
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
         anchorSlotMinutes: anchorSlot,
         slotEndMinutes,
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
      events = [],
   } = {},
   slotStarts = [],
   closeMinutes = null
) {
   const guardiansTalkRows = buildScheduledItemRows(
      guardiansTalks.filter(isActiveScheduledOccurrence),
      buildGuardiansRows,
      getScheduledMaximumDuration
   ).map((scheduledItem) => ({
      ...scheduledItem,
      scheduleItemKind: 'guardians_talks',
      scheduleItemKey: getGuardiansTalkId(scheduledItem.item),
   }));
   const wildEncounterRows = buildScheduledItemRows(
      wildEncounters.filter(isActiveScheduledOccurrence),
      buildWildRows,
      getScheduledMaximumDuration
   ).map((scheduledItem) => ({
      ...scheduledItem,
      scheduleItemKind: 'wild_encounters',
      scheduleItemKey: getWildEncounterId(scheduledItem.item),
   }));
   const animalRows = buildScheduledAnimalRows(animals).map((scheduledItem) => ({
      ...scheduledItem,
      scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
      scheduleItemKey: getAnimalId(scheduledItem.item),
   }));
   const attractionRows = buildScheduledItemRows(
      attractions,
      buildAttractionRows,
      getDurationMinutesFromScheduleTimes
   ).map((scheduledItem) => ({
      ...scheduledItem,
      scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      scheduleItemKey: getAttractionId(scheduledItem.item),
   }));
   const genericEventRows = buildGenericEventScheduledRows(events);
   const scheduledItems = [
      ...guardiansTalkRows,
      ...wildEncounterRows,
      ...animalRows,
      ...attractionRows,
      ...genericEventRows,
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
      animals: (itinerary.animals ?? []).filter((_, index) => (
         scheduledAnimalIndexes.has(index)
      )),
      attractions: (itinerary.attractions ?? []).filter((_, index) => (
         scheduledAttractionIndexes.has(index)
      )),
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
