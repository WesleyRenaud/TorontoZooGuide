export class OpeningScheduleChecker {
   static OPENING_SCHEDULE_OVERLAP_ERROR_TYPE = 'overlappingSchedule';

   static OPENING_SCHEDULE_OVERLAP_RESOLUTION = Object.freeze({
      REPLACE: 'replace',
      TRIM: 'trim',
   });

   static resultHasOpeningScheduleOverlap(result) {
      return (
         result?.errorType === OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE
         || result?.error_type === OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE
      );
   }
}
