export const OPENING_SCHEDULE_OVERLAP_ERROR_TYPE = 'overlappingSchedule';

export const OPENING_SCHEDULE_OVERLAP_RESOLUTION = Object.freeze({
   REPLACE: 'replace',
   TRIM: 'trim',
});

export function resultHasOpeningScheduleOverlap(result) {
   return (
      result?.errorType === OPENING_SCHEDULE_OVERLAP_ERROR_TYPE
      || result?.error_type === OPENING_SCHEDULE_OVERLAP_ERROR_TYPE
   );
}
