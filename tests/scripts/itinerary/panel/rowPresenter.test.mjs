import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerScheduleController } from '../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { RowPresenter } from '../../../../scripts/itinerary/panel/rowPresenter.js';
import { RowPresentationHelper } from '../../../../scripts/itinerary/panel/rowPresentationHelper.js';
import { ScheduledOccurrenceTimeModel } from '../../../../scripts/itinerary/scheduledOccurrenceTimeModel.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_BuildImageSrc_TestParts_ExpectPathOrNull', () => {
   assert.equal(
      RowPresenter.buildImageSrc('animals', 'African Savanna', 'African Lion'),
      'images/details/animals/african-savanna/african-lion.png'
   );
   assert.equal(RowPresenter.buildImageSrc('animals', '', 'African Lion'), null);
});

test('Test_BuildFieldLine_TestValue_ExpectLabeledOrEmpty', () => {
   assert.equal(RowPresenter.buildFieldLine('Exhibit', 'African Rainforest'), 'Exhibit: African Rainforest');
   assert.equal(RowPresenter.buildFieldLine('Exhibit', ''), '');
});

test('Test_BuildScheduledTimeFieldLine_TestItem_ExpectTimeLine', () => {
   const original = ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange;
   ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange = () => '11:00 AM - 12:00 PM';

   try {
      assert.equal(
         RowPresenter.buildScheduledTimeFieldLine({ start_time: '11:00 AM' }),
         RowPresentationHelper.buildTimeFieldLine('11:00 AM - 12:00 PM')
      );
   } finally {
      ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange = original;
   }
});

test('Test_BuildApproximateStartTimeFieldLine_TestStartTime_ExpectRounded', () => {
   const originalParse = DayPlannerScheduleController.parseClockTimeMinutes;
   const originalFormat = DayPlannerScheduleController.formatMinutesAsClockTime;
   DayPlannerScheduleController.parseClockTimeMinutes = (value) => (
      value ? 602 : Number.NaN
   );
   DayPlannerScheduleController.formatMinutesAsClockTime = (minutes) => `m${minutes}`;

   try {
      assert.equal(
         RowPresenter.buildApproximateStartTimeFieldLine({ start_time: '10:02 AM' }),
         RowPresentationHelper.buildTimeFieldLine('~m600')
      );
      assert.equal(RowPresenter.buildApproximateStartTimeFieldLine({}), '');
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
      DayPlannerScheduleController.formatMinutesAsClockTime = originalFormat;
   }
});

test('Test_BuildMetaLines_TestValues_ExpectFiltered', () => {
   assert.deepEqual(RowPresenter.buildMetaLines(['a', '', 'b', null]), ['a', 'b']);
});

test('Test_BuildLinkRowProps_TestLink_ExpectHandlers', () => {
   assert.deepEqual(RowPresenter.buildLinkRowProps(null), {});

   const opens = [];
   const originalOpen = window.open;
   window.open = (...args) => { opens.push(args); };

   try {
      const props = RowPresenter.buildLinkRowProps('https://example.com');
      assert.equal(props.linkText, Strings.common.moreInfo);
      props.onLinkClick();
      assert.deepEqual(opens, [['https://example.com', '_blank']]);

      const titleProps = RowPresenter.buildTitleLinkRowProps('https://zoo.example');
      titleProps.onNameClick();
      assert.deepEqual(opens[1], ['https://zoo.example', '_blank']);
   } finally {
      window.open = originalOpen;
   }
});
