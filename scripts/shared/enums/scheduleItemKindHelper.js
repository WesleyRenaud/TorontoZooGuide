export class ScheduleItemKindHelper {
   static normalizeScheduleItemKindKey(value) {
      return String(value ?? '').trim().toLowerCase();
   }
}
