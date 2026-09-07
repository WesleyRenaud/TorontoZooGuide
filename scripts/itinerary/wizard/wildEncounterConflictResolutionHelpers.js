import { ScheduleConflictCompatibility } from './scheduleConflictCompatibility.js';

export class WildEncounterConflictResolutionHelpers {
   static toConflictResolutionDraftItem(item) {
      if (ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)) {
         return {
            name: item.name,
            location: item.location,
         };
      }

      return {
         name: item.name,
         meeting_spot: item.meeting_spot,
      };
   }

   static getDraftItemName(item) {
      if (typeof item === 'string') {
         return item;
      }

      return item?.name ?? '';
   }
}
