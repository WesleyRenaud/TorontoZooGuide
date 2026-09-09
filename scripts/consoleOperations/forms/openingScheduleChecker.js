import { OpeningScheduleOverlapErrorType } from '../../shared/enums/openingScheduleOverlapErrorType.js';
import { OpeningScheduleOverlapResolution } from '../../shared/enums/openingScheduleOverlapResolution.js';

export class OpeningScheduleChecker {
   static OPENING_SCHEDULE_OVERLAP_ERROR_TYPE = OpeningScheduleOverlapErrorType.OVERLAPPING_SCHEDULE;

   static OPENING_SCHEDULE_OVERLAP_RESOLUTION = OpeningScheduleOverlapResolution;

   static resultHasOpeningScheduleOverlap(result) {
      return (
         result?.errorType === OpeningScheduleOverlapErrorType.OVERLAPPING_SCHEDULE
         || result?.error_type === OpeningScheduleOverlapErrorType.OVERLAPPING_SCHEDULE
      );
   }
}
