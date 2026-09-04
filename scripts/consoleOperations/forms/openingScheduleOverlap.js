export class OpeningScheduleOverlap {
   static OPENING_SCHEDULE_OVERLAP_ERROR_TYPE = 'overlappingSchedule';

   static OPENING_SCHEDULE_OVERLAP_RESOLUTION = Object.freeze({
      REPLACE: 'replace',
      TRIM: 'trim',
   });

   static resultHasOpeningScheduleOverlap(result) {
      return (
         result?.errorType === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE
         || result?.error_type === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE
      );
   }
}
