import { OpeningScheduleOverlapFragment } from './openingScheduleOverlapFragment.js';
import { OpeningScheduleOverlapResolution } from '../../shared/enums/openingScheduleOverlapResolution.js';

export class OpeningScheduleOverlapResolver {
   static async resolveOpeningScheduleOverlapConflict({
      payload,
      replaceOverlaps,
      trimOverlaps,
      dismissedResult = null,
      showDialog = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog,
   }) {
      const resolution = await showDialog();

      if (resolution === OpeningScheduleOverlapResolution.REPLACE) {
         return replaceOverlaps(payload);
      }

      if (resolution === OpeningScheduleOverlapResolution.TRIM) {
         return trimOverlaps(payload);
      }

      return dismissedResult;
   }
}
