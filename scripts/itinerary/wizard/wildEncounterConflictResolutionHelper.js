import { ScheduleConflictChecker } from './scheduleConflictChecker.js';

export class WildEncounterConflictResolutionHelper {
   static toConflictResolutionDraftItem(item) {
      if (ScheduleConflictChecker.isGuardiansTalkConflictItem(item)) {
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
