import { ValueNormalizer } from '../../api/valueNormalizer.js';
import scheduleItemKindValues from '../../../shared/enums/scheduleItemKind.json' with { type: 'json' };

export class ScheduleItemKind {
   static {
      Object.entries(scheduleItemKindValues).forEach(([memberName, definition]) => {
         Object.assign(ScheduleItemKind, { [memberName]: Object.freeze({ ...definition }) });
      });

      ScheduleItemKind.SCHEDULE_ITEM_KIND_ENTRIES = Object.freeze(
         Object.keys(scheduleItemKindValues).map(memberName => ScheduleItemKind[memberName])
      );

      ScheduleItemKind.ITEM_TYPE_BY_KIND = Object.freeze(
         Object.fromEntries(
            ScheduleItemKind.SCHEDULE_ITEM_KIND_ENTRIES
               .filter(entry => Boolean(entry.itemType))
               .map(entry => [entry.kind, entry.itemType])
         )
      );
   }

   static scheduleItemKindFromItemType(itemType) {
      const normalized = ValueNormalizer.asTrimmedString(itemType).toLowerCase();

      if (!normalized) {
         return null;
      }

      for (const entry of ScheduleItemKind.SCHEDULE_ITEM_KIND_ENTRIES) {
         if (entry?.itemType === normalized) {
            return entry;
         }
      }

      for (const entry of ScheduleItemKind.SCHEDULE_ITEM_KIND_ENTRIES) {
         if (entry?.kind === normalized) {
            return entry;
         }
      }

      return null;
   }

   static isScheduleItemModuleItemType(itemType) {
      const normalized = ValueNormalizer.asTrimmedString(itemType).toLowerCase();

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
      return ScheduleItemKind.ITEM_TYPE_BY_KIND[ValueNormalizer.asTrimmedString(kind).toLowerCase()] ?? null;
   }
}
