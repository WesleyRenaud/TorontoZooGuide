import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ScheduledPillViewingWalkNode } from './components/scheduledPillViewingWalkNode.js';
import { DayPlannerSchedule } from './dayPlannerSchedule.js';
import { DayPlannerTimelineMarkers } from './dayPlannerTimelineMarkers.js';
import { ItineraryPanelRowsBuilder } from './itineraryPanelRowsBuilder.js';
import { RowActionProps } from './rowActionProps.js';
import { ScheduleItemEventLabels } from './scheduleItemEventLabels.js';
import { AnimalSelectorModel } from '../selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../selectors/attractionSelector/attractionSelectorModel.js';
import { GuardiansTalkSelectorModel } from '../selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { TransportationSelectorModel } from '../selectors/transportationSelector/transportationSelectorModel.js';
import { TransportationSequenceItems } from '../selectors/transportationSelector/transportationSequenceItems.js';
import { WildEncounterSelectorModel } from '../selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { SpeciesExhibitKey } from '../speciesExhibitKey.js';

export class DayPlannerScheduledItems {
   static getScheduledMaximumDuration(item) {
      const maximumDuration = Number(item?.maximum_duration);
      return Number.isFinite(maximumDuration) && maximumDuration > 0 ? maximumDuration : null;
   }

   static getDurationMinutesFromScheduleTimes(item) {
      return (
         DayPlannerSchedule.parseClockTimeMinutes(item.end_time) - DayPlannerSchedule.parseClockTimeMinutes(item.start_time)
      );
   }

   static isCoveredByTalk(item) {
      return item?.covered_by_talk === true;
   }

   static isActiveScheduledOccurrence(item) {
      return item?.is_deleted !== true;
   }

   static getScheduledItemLabel(item) {
      if (item?.species) {
         return AnimalSelectorModel.getAnimalTitleLine(item);
      }

      return ValueNormalizer.asTrimmedString(item?.name);
   }

   static getItineraryEventType(item) {
      return ValueNormalizer.asTrimmedString(item?.event_type);
   }

   static buildGenericEventScheduledRows(events = []) {
      return events.map((event, index) => {
         const eventType = DayPlannerScheduledItems.getItineraryEventType(event);
         const startMinutes = DayPlannerSchedule.parseClockTimeMinutes(event.start_time);
         const endMinutes = DayPlannerSchedule.parseClockTimeMinutes(event.end_time);
         const maximumDuration = DayPlannerScheduledItems.getDurationMinutesFromScheduleTimes(event);
         const label = ScheduleItemEventLabels.formatItineraryEventTypeLabel(eventType);

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

   static buildScheduledItemRows(items, buildRows, getDurationMinutes) {
      return items.map((item, index) => {
         const [row] = buildRows([item]);
         const startMinutes = DayPlannerSchedule.parseClockTimeMinutes(item.start_time);
         const endMinutes = DayPlannerSchedule.parseClockTimeMinutes(item.end_time);
         const maximumDuration = getDurationMinutes(item);
         const label = DayPlannerScheduledItems.getScheduledItemLabel(item);

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

   static buildScheduledAnimalRows(animals = []) {
      return SpeciesExhibitKey.buildUniqueSpeciesExhibitEntries(animals, {
         includeAnimal: (item) => (
            RowActionProps.hasItineraryScheduleTimes(item) && !DayPlannerScheduledItems.isCoveredByTalk(item)
         ),
         buildKey: SpeciesExhibitKey.buildAnimalViewingSpotKey,
         requireExhibit: false,
      }).map(({ item, index }) => {
         const [row] = ItineraryPanelRowsBuilder.buildAnimalRows([item]);
         const startMinutes = DayPlannerSchedule.parseClockTimeMinutes(item.start_time);
         const endMinutes = DayPlannerSchedule.parseClockTimeMinutes(item.end_time);
         const maximumDuration = DayPlannerScheduledItems.getDurationMinutesFromScheduleTimes(item);
         const label = DayPlannerScheduledItems.getScheduledItemLabel(item);
         const viewingWalkNodeId = ScheduledPillViewingWalkNode.getAnimalViewingWalkNodeId(item);

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

   static buildScheduledTransportationRows(transportations = []) {
      return transportations.flatMap((transportation, index) => (
         TransportationSequenceItems.buildTransportationSequenceItems(transportation).map((item) => {
            const [row] = ItineraryPanelRowsBuilder.buildTransportationRows([item]);
            const startMinutes = DayPlannerSchedule.parseClockTimeMinutes(item.start_time);
            const endMinutes = DayPlannerSchedule.parseClockTimeMinutes(item.end_time);
            const maximumDuration = DayPlannerScheduledItems.getDurationMinutesFromScheduleTimes(item);
            const label = DayPlannerScheduledItems.getScheduledItemLabel(item);

            return {
               index,
               item,
               row,
               label,
               startMinutes,
               endMinutes,
               maximumDuration,
            };
         })
      )).filter((scheduledItem) => (
         scheduledItem.row
         && scheduledItem.label
         && Number.isFinite(scheduledItem.startMinutes)
         && Number.isFinite(scheduledItem.endMinutes)
         && Number.isFinite(scheduledItem.maximumDuration)
      ));
   }

   static buildItineraryScheduledTransportationIndexes(items = []) {
      const indexes = new Set();

      items.forEach((item, index) => {
         if (!TransportationSelectorModel.isTransitTransportationHandledForDayPlanner(item)) {
            return;
         }

         indexes.add(index);
      });

      return indexes;
   }

   static buildItineraryScheduledItemIndexes(items = []) {
      const indexes = new Set();

      items.forEach((item, index) => {
         if (!RowActionProps.hasItineraryScheduleTimes(item)) {
            return;
         }

         indexes.add(index);
      });

      return indexes;
   }

   static mergeScheduledItemsByAnchorSlot(
      scheduledItems = [],
      slotStarts = [],
      closeMinutes = null
   ) {
      const sortedSlotStarts = [...slotStarts].sort((left, right) => left - right);

      return scheduledItems.reduce((itemsByAnchorMap, scheduledItem) => {
         const anchorSlot = DayPlannerTimelineMarkers.findTimelineAnchorSlot(
            scheduledItem.startMinutes,
            sortedSlotStarts
         );

         if (!Number.isFinite(anchorSlot)) {
            return itemsByAnchorMap;
         }

         const slotEndMinutes = DayPlannerTimelineMarkers.findTimelineSlotEndMinutes(
            anchorSlot,
            sortedSlotStarts,
            closeMinutes
         );
         const offsetFraction = DayPlannerTimelineMarkers.computeMarkerOffsetFraction(
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

   static buildScheduledItemRowsContext(
      {
      animals = [],
      attractions = [],
      guardiansTalks = [],
      wildEncounters = [],
      transportations = [],
      events = [],
      } = {},
      slotStarts = [],
      closeMinutes = null
   ) {
      const guardiansTalkRows = DayPlannerScheduledItems.buildScheduledItemRows(
         guardiansTalks.filter(DayPlannerScheduledItems.isActiveScheduledOccurrence),
         ItineraryPanelRowsBuilder.buildGuardiansRows,
         DayPlannerScheduledItems.getScheduledMaximumDuration
      ).map((scheduledItem) => ({
         ...scheduledItem,
         scheduleItemKind: 'guardians_talks',
         scheduleItemKey: GuardiansTalkSelectorModel.getGuardiansTalkId(scheduledItem.item),
      }));
      const wildEncounterRows = DayPlannerScheduledItems.buildScheduledItemRows(
         wildEncounters.filter(DayPlannerScheduledItems.isActiveScheduledOccurrence),
         ItineraryPanelRowsBuilder.buildWildRows,
         DayPlannerScheduledItems.getScheduledMaximumDuration
      ).map((scheduledItem) => ({
         ...scheduledItem,
         scheduleItemKind: 'wild_encounters',
         scheduleItemKey: WildEncounterSelectorModel.getWildEncounterId(scheduledItem.item),
      }));
      const animalRows = DayPlannerScheduledItems.buildScheduledAnimalRows(animals).map((scheduledItem) => ({
         ...scheduledItem,
         scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
         scheduleItemKey: AnimalSelectorModel.getAnimalId(scheduledItem.item),
      }));
      const attractionRows = DayPlannerScheduledItems.buildScheduledItemRows(
         attractions,
         ItineraryPanelRowsBuilder.buildAttractionRows,
         DayPlannerScheduledItems.getDurationMinutesFromScheduleTimes
      ).map((scheduledItem) => ({
         ...scheduledItem,
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
         scheduleItemKey: AttractionSelectorModel.getAttractionId(scheduledItem.item),
      }));
      const transportationRows = DayPlannerScheduledItems.buildScheduledTransportationRows(
         transportations
      ).map((scheduledItem) => ({
         ...scheduledItem,
         scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType,
         scheduleItemKey: TransportationSelectorModel.getTransportationScheduleItemKey(scheduledItem.item),
      }));
      const genericEventRows = DayPlannerScheduledItems.buildGenericEventScheduledRows(events);
      const scheduledItems = [
         ...guardiansTalkRows,
         ...wildEncounterRows,
         ...animalRows,
         ...attractionRows,
         ...transportationRows,
         ...genericEventRows,
      ];

      return {
         itemsByStart: DayPlannerScheduledItems.mergeScheduledItemsByAnchorSlot(
            scheduledItems,
            slotStarts,
            closeMinutes
         ),
         scheduledAnimalIndexes: DayPlannerScheduledItems.buildItineraryScheduledItemIndexes(animals),
         scheduledAttractionIndexes: DayPlannerScheduledItems.buildItineraryScheduledItemIndexes(attractions),
         scheduledTransportationIndexes: DayPlannerScheduledItems.buildItineraryScheduledTransportationIndexes(
            transportations
         ),
         scheduledGuardiansTalkIndexes: new Set(
            guardiansTalkRows.map((scheduledItem) => scheduledItem.index)
         ),
         scheduledWildEncounterIndexes: new Set(
            wildEncounterRows.map((scheduledItem) => scheduledItem.index)
         ),
      };

   }

   static buildScheduledItinerary(
      itinerary = {},
      {
      scheduledAnimalIndexes = new Set(),
      scheduledAttractionIndexes = new Set(),
      scheduledTransportationIndexes = new Set(),
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
         transportations: (itinerary.transportations ?? []).filter((_, index) => (
            scheduledTransportationIndexes.has(index)
         )),
         guardiansTalks: (itinerary.guardiansTalks ?? []).filter((_, index) => (
            scheduledGuardiansTalkIndexes.has(index)
         )),
         wildEncounters: (itinerary.wildEncounters ?? []).filter((_, index) => (
            scheduledWildEncounterIndexes.has(index)
         )),
      };

   }

   static buildUnscheduledItinerary(
      itinerary = {},
      {
      scheduledAnimalIndexes = new Set(),
      scheduledAttractionIndexes = new Set(),
      scheduledTransportationIndexes = new Set(),
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
         transportations: (itinerary.transportations ?? []).filter((_, index) => (
            !scheduledTransportationIndexes.has(index)
         )),
         guardiansTalks: (itinerary.guardiansTalks ?? []).filter((_, index) => (
            !scheduledGuardiansTalkIndexes.has(index)
         )),
         wildEncounters: (itinerary.wildEncounters ?? []).filter((_, index) => (
            !scheduledWildEncounterIndexes.has(index)
         )),
      };
   }
}
