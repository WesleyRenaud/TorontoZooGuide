import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { AttractionOpeningController } from '../../../../../scripts/consoleOperations/attractions/controllers/attractionOpeningController.js';
import { OpeningScheduleChecker } from '../../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { OpeningScheduleOverlapFragment } from '../../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { WeeklyAvailabilityFormController } from '../../../../../scripts/consoleOperations/forms/weeklyAvailabilityFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { Strings } from '../../../../../scripts/strings.js';


function _captureWeeklyForm() {
   const original = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController;
   let captured;
   WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = (options) => {
      captured = options;
      return { created: true };
   };
   return {
      getCaptured: () => captured,
      restore: () => {
         WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = original;
      },
   };
}


test('Test_CreateAttractionOpeningScheduleController_TestWiring_ExpectWeeklyForm', () => {
   const entity = 'Carousel';
   const capture = _captureWeeklyForm();

   try {
      AttractionOpeningController.createAttractionOpeningScheduleController({});

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadAttractions);
      assert.equal(capture.getCaptured().submitSchedule, ConsoleOperationsClient.setAttractionOpeningSchedule);
      assert.equal(capture.getCaptured().entityLabel, Strings.entityLabels.attraction);
      assert.equal(capture.getCaptured().payloadKey, 'attraction');
      assert.equal(capture.getCaptured().resultName({ attraction: entity }), entity);
   } finally {
      capture.restore();
   }
});


test('Test_CreateAttractionOpeningScheduleController_TestResolveOverlapReplace_ExpectReplaced', async () => {
   const payload = { attraction: 'Carousel' };
   const capture = _captureWeeklyForm();
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const originalReplace = ConsoleOperationsClient.replaceAttractionOpeningScheduleOverlaps;
   ConsoleOperationsClient.replaceAttractionOpeningScheduleOverlaps = async (value) => ({ replaced: value });
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
      OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE
   );

   try {
      AttractionOpeningController.createAttractionOpeningScheduleController({});
      const result = await capture.getCaptured().resolveOverlapConflict(payload);

      assert.deepEqual(result, { replaced: payload });
   } finally {
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      ConsoleOperationsClient.replaceAttractionOpeningScheduleOverlaps = originalReplace;
      capture.restore();
   }
});


test('Test_CreateAttractionOpeningScheduleController_TestResolveOverlapTrim_ExpectTrimmed', async () => {
   const payload = { attraction: 'Carousel' };
   const capture = _captureWeeklyForm();
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const originalTrim = ConsoleOperationsClient.trimAttractionOpeningScheduleOverlaps;
   ConsoleOperationsClient.trimAttractionOpeningScheduleOverlaps = async (value) => ({ trimmed: value });
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
      OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM
   );

   try {
      AttractionOpeningController.createAttractionOpeningScheduleController({});
      const result = await capture.getCaptured().resolveOverlapConflict(payload);

      assert.deepEqual(result, { trimmed: payload });
   } finally {
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      ConsoleOperationsClient.trimAttractionOpeningScheduleOverlaps = originalTrim;
      capture.restore();
   }
});


test('Test_CreateAttractionOpeningScheduleController_TestResolveOverlapCancel_ExpectNull', async () => {
   const payload = { attraction: 'Carousel' };
   const capture = _captureWeeklyForm();
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => null;

   try {
      AttractionOpeningController.createAttractionOpeningScheduleController({});
      const result = await capture.getCaptured().resolveOverlapConflict(payload);

      assert.equal(result, null);
   } finally {
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      capture.restore();
   }
});
