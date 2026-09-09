import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionOpeningController } from '../../../../../scripts/consoleOperations/attractions/controllers/attractionOpeningController.js';
import { WeeklyAvailabilityFormController } from '../../../../../scripts/consoleOperations/forms/weeklyAvailabilityFormController.js';
import { OpeningScheduleOverlapFragment } from '../../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { OpeningScheduleChecker } from '../../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateAttractionOpeningScheduleController_TestWiring_ExpectWeeklyForm', async () => {
   const original = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController;
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const originalReplace = ConsoleOperationsClient.replaceAttractionOpeningScheduleOverlaps;
   const originalTrim = ConsoleOperationsClient.trimAttractionOpeningScheduleOverlaps;
   let captured;

   WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = (options) => {
      captured = options;
      return { created: true };
   };
   ConsoleOperationsClient.replaceAttractionOpeningScheduleOverlaps = async (p) => ({ replaced: p });
   ConsoleOperationsClient.trimAttractionOpeningScheduleOverlaps = async (p) => ({ trimmed: p });

   try {
      AttractionOpeningController.createAttractionOpeningScheduleController({ attractionEl: {} });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadAttractions);
      assert.equal(captured.submitSchedule, ConsoleOperationsClient.setAttractionOpeningSchedule);
      assert.equal(captured.entityLabel, Strings.entityLabels.attraction);
      assert.equal(captured.payloadKey, 'attraction');
      assert.equal(captured.resultName({ attraction: 'Carousel' }), 'Carousel');

      const payload = { attraction: 'Carousel' };

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE
      );
      assert.deepEqual(await captured.resolveOverlapConflict(payload), { replaced: payload });

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM
      );
      assert.deepEqual(await captured.resolveOverlapConflict(payload), { trimmed: payload });

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => null;
      assert.equal(await captured.resolveOverlapConflict(payload), null);
   } finally {
      WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = original;
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      ConsoleOperationsClient.replaceAttractionOpeningScheduleOverlaps = originalReplace;
      ConsoleOperationsClient.trimAttractionOpeningScheduleOverlaps = originalTrim;
   }
});
