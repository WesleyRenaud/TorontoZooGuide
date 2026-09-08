export class ScheduleItemKindHelpers {
   static normalizeScheduleItemKindKey(value) {
      return String(value ?? '').trim().toLowerCase();
   }
}
