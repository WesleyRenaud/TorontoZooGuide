export const ScheduleItemKind = Object.freeze({
   ENTRANCE: Object.freeze({
      kind: 'entrance',
   }),
   ANIMAL: Object.freeze({
      kind: 'animal',
      itemType: 'animals',
   }),
   ATTRACTION: Object.freeze({
      kind: 'attraction',
      itemType: 'attractions',
   }),
   GUARDIANS_TALK: Object.freeze({
      kind: 'guardians_talk',
      itemType: 'guardians_talks',
   }),
   WILD_ENCOUNTER: Object.freeze({
      kind: 'wild_encounter',
      itemType: 'wild_encounters',
   }),
   EVENT: Object.freeze({
      kind: 'event',
   }),
});

const ITEM_TYPE_BY_KIND = Object.freeze({
   [ScheduleItemKind.ANIMAL.kind]: ScheduleItemKind.ANIMAL.itemType,
   [ScheduleItemKind.ATTRACTION.kind]: ScheduleItemKind.ATTRACTION.itemType,
   [ScheduleItemKind.GUARDIANS_TALK.kind]: ScheduleItemKind.GUARDIANS_TALK.itemType,
   [ScheduleItemKind.WILD_ENCOUNTER.kind]: ScheduleItemKind.WILD_ENCOUNTER.itemType,
});

export function scheduleItemKindFromItemType(itemType) {
   const normalized = String(itemType ?? '').trim().toLowerCase();

   if (!normalized) {
      return null;
   }

   for (const entry of Object.values(ScheduleItemKind)) {
      if (entry.itemType === normalized) {
         return entry;
      }
   }

   for (const entry of Object.values(ScheduleItemKind)) {
      if (entry.kind === normalized) {
         return entry;
      }
   }

   return null;
}

export function isScheduleItemModuleItemType(itemType) {
   const normalized = String(itemType ?? '').trim().toLowerCase();

   return (
      normalized === ScheduleItemKind.ANIMAL.itemType
      || normalized === ScheduleItemKind.ATTRACTION.itemType
      || normalized === ScheduleItemKind.GUARDIANS_TALK.itemType
      || normalized === ScheduleItemKind.WILD_ENCOUNTER.itemType
   );
}

export function scheduleItemModuleItemTypeForKind(kind) {
   return ITEM_TYPE_BY_KIND[String(kind ?? '').trim().toLowerCase()] ?? null;
}
