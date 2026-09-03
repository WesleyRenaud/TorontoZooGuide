export class ScheduleItemKind {
   static ENTRANCE = Object.freeze({
      kind: 'entrance',
   });
   static ANIMAL = Object.freeze({
      kind: 'animal',
      itemType: 'animals',
   });
   static ATTRACTION = Object.freeze({
      kind: 'attraction',
      itemType: 'attractions',
   });
   static TRANSPORTATION = Object.freeze({
      kind: 'transportation',
      itemType: 'transportations',
   });
   static GUARDIANS_TALK = Object.freeze({
      kind: 'guardians_talk',
      itemType: 'guardians_talks',
   });
   static WILD_ENCOUNTER = Object.freeze({
      kind: 'wild_encounter',
      itemType: 'wild_encounters',
   });
   static EVENT = Object.freeze({
      kind: 'event',
   });

   static scheduleItemKindFromItemType(itemType) {
      const normalized = normalizeScheduleItemKindKey(itemType);

      if (!normalized) {
         return null;
      }

      for (const entry of SCHEDULE_ITEM_KIND_ENTRIES) {
         if (entry?.itemType === normalized) {
            return entry;
         }
      }

      for (const entry of SCHEDULE_ITEM_KIND_ENTRIES) {
         if (entry?.kind === normalized) {
            return entry;
         }
      }

      return null;
   }

   static isScheduleItemModuleItemType(itemType) {
      const normalized = normalizeScheduleItemKindKey(itemType);

      return (
         normalized === ScheduleItemKind.ANIMAL.itemType
         || normalized === ScheduleItemKind.ATTRACTION.itemType
         || normalized === ScheduleItemKind.TRANSPORTATION.itemType
         || normalized === ScheduleItemKind.GUARDIANS_TALK.itemType
         || normalized === ScheduleItemKind.WILD_ENCOUNTER.itemType
      );
   }

   static isFixedTimeScheduleItemKind(itemType) {
      const kind = ScheduleItemKind.scheduleItemKindFromItemType(itemType);

      return (
         kind === ScheduleItemKind.GUARDIANS_TALK
         || kind === ScheduleItemKind.WILD_ENCOUNTER
      );
   }

   static usesScheduledTimelineEventCard(scheduleItemKind) {
      const kind = ScheduleItemKind.scheduleItemKindFromItemType(scheduleItemKind);

      return (
         ScheduleItemKind.isFixedTimeScheduleItemKind(scheduleItemKind)
         || kind === ScheduleItemKind.ATTRACTION
         || kind === ScheduleItemKind.TRANSPORTATION
      );
   }

   static scheduleItemModuleItemTypeForKind(kind) {
      return ITEM_TYPE_BY_KIND[normalizeScheduleItemKindKey(kind)] ?? null;
   }
}

function normalizeScheduleItemKindKey(value) {
   return String(value ?? '').trim().toLowerCase();
}

const SCHEDULE_ITEM_KIND_ENTRIES = Object.freeze([
   ScheduleItemKind.ENTRANCE,
   ScheduleItemKind.ANIMAL,
   ScheduleItemKind.ATTRACTION,
   ScheduleItemKind.TRANSPORTATION,
   ScheduleItemKind.GUARDIANS_TALK,
   ScheduleItemKind.WILD_ENCOUNTER,
   ScheduleItemKind.EVENT,
]);

const ITEM_TYPE_BY_KIND = Object.freeze({
   [ScheduleItemKind.ANIMAL.kind]: ScheduleItemKind.ANIMAL.itemType,
   [ScheduleItemKind.ATTRACTION.kind]: ScheduleItemKind.ATTRACTION.itemType,
   [ScheduleItemKind.TRANSPORTATION.kind]: ScheduleItemKind.TRANSPORTATION.itemType,
   [ScheduleItemKind.GUARDIANS_TALK.kind]: ScheduleItemKind.GUARDIANS_TALK.itemType,
   [ScheduleItemKind.WILD_ENCOUNTER.kind]: ScheduleItemKind.WILD_ENCOUNTER.itemType,
});
