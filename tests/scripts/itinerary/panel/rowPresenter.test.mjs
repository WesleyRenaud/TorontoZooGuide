import assert from 'node:assert/strict';
import test from 'node:test';

import { AssetKeyNormalizer } from '../../../../scripts/assets/assetKeyNormalizer.js';
import { DayPlannerScheduleController } from '../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { RowPresentationHelper } from '../../../../scripts/itinerary/panel/rowPresentationHelper.js';
import { RowPresenter } from '../../../../scripts/itinerary/panel/rowPresenter.js';
import { ScheduledOccurrenceTimeModel } from '../../../../scripts/itinerary/scheduledOccurrenceTimeModel.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_BuildImageSrc_TestParts_ExpectPath', () => {
   const directory = 'animals';
   const exhibit = 'African Savanna';
   const species = 'African Lion';

   const src = RowPresenter.buildImageSrc(directory, exhibit, species);

   assert.equal(
      src,
      `images/details/${[directory, exhibit, species].map((part) => AssetKeyNormalizer.normalize(part)).join('/')}.png`
   );
});


test('Test_BuildImageSrc_TestBlankPart_ExpectNull', () => {
   const directory = 'animals';
   const exhibit = '';
   const species = 'African Lion';

   const src = RowPresenter.buildImageSrc(directory, exhibit, species);

   assert.equal(src, null);
});


test('Test_BuildFieldLine_TestValue_ExpectLabeled', () => {
   const label = 'Exhibit';
   const value = 'African Rainforest';

   const line = RowPresenter.buildFieldLine(label, value);

   assert.equal(line, Strings.format.labeledValue(label, value));
});


test('Test_BuildFieldLine_TestBlank_ExpectEmpty', () => {
   const label = 'Exhibit';
   const value = '';

   const line = RowPresenter.buildFieldLine(label, value);

   assert.equal(line, value);
});


test('Test_BuildScheduledTimeFieldLine_TestItem_ExpectTimeLine', () => {
   const original = ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange;
   const timeRange = '11:00 AM - 12:00 PM';
   ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange = () => timeRange;

   try {
      const line = RowPresenter.buildScheduledTimeFieldLine({ start_time: '11:00 AM' });

      assert.equal(line, RowPresentationHelper.buildTimeFieldLine(timeRange));
   } finally {
      ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange = original;
   }
});


test('Test_BuildApproximateStartTimeFieldLine_TestStartTime_ExpectRounded', () => {
   const originalParse = DayPlannerScheduleController.parseClockTimeMinutes;
   const originalFormat = DayPlannerScheduleController.formatMinutesAsClockTime;
   const startMinutes = 602;
   const roundedMinutes = Math.round(startMinutes / 5) * 5;
   DayPlannerScheduleController.parseClockTimeMinutes = (value) => (
      value ? startMinutes : Number.NaN
   );
   DayPlannerScheduleController.formatMinutesAsClockTime = (minutes) => `m${minutes}`;

   try {
      const line = RowPresenter.buildApproximateStartTimeFieldLine({ start_time: '10:02 AM' });

      assert.equal(
         line,
         RowPresentationHelper.buildTimeFieldLine(
            Strings.format.approximate(`m${roundedMinutes}`)
         )
      );
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
      DayPlannerScheduleController.formatMinutesAsClockTime = originalFormat;
   }
});


test('Test_BuildApproximateStartTimeFieldLine_TestMissingStart_ExpectEmpty', () => {
   const originalParse = DayPlannerScheduleController.parseClockTimeMinutes;
   const originalFormat = DayPlannerScheduleController.formatMinutesAsClockTime;
   DayPlannerScheduleController.parseClockTimeMinutes = () => Number.NaN;
   DayPlannerScheduleController.formatMinutesAsClockTime = (minutes) => `m${minutes}`;

   try {
      const line = RowPresenter.buildApproximateStartTimeFieldLine({});

      assert.equal(line, '');
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
      DayPlannerScheduleController.formatMinutesAsClockTime = originalFormat;
   }
});


test('Test_BuildMetaLines_TestValues_ExpectFiltered', () => {
   const first = 'African Lion';
   const second = 'Snow Leopard';
   const lines = [first, '', second, null];

   const metaLines = RowPresenter.buildMetaLines(lines);

   assert.deepEqual(metaLines, [first, second]);
});


test('Test_BuildLinkRowProps_TestNull_ExpectEmpty', () => {
   const link = null;

   const props = RowPresenter.buildLinkRowProps(link);

   assert.deepEqual(props, {});
});


test('Test_BuildLinkRowProps_TestLink_ExpectOpens', () => {
   const link = 'https://example.com';
   const opens = [];
   const originalOpen = window.open;
   window.open = (...args) => { opens.push(args); };

   try {
      const props = RowPresenter.buildLinkRowProps(link);
      props.onLinkClick();

      assert.equal(props.linkText, Strings.common.moreInfo);
      assert.deepEqual(opens.at(Position.FIRST), [link, '_blank']);
   } finally {
      window.open = originalOpen;
   }
});


test('Test_BuildTitleLinkRowProps_TestLink_ExpectOpens', () => {
   const link = 'https://zoo.example';
   const opens = [];
   const originalOpen = window.open;
   window.open = (...args) => { opens.push(args); };

   try {
      const props = RowPresenter.buildTitleLinkRowProps(link);
      props.onNameClick();

      assert.deepEqual(opens.at(Position.FIRST), [link, '_blank']);
   } finally {
      window.open = originalOpen;
   }
});
