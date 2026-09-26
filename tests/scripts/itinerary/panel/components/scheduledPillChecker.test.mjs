import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeScheduledItem } from '../../../helpers/scheduledPillTestSetup.mjs';
import { ScheduledPillChecker } from '../../../../../scripts/itinerary/panel/components/scheduledPillChecker.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { ZooClockTimeHelper } from '../../../../../scripts/shared/zooClockTimeHelper.js';
import { Strings } from '../../../../../scripts/strings.js';


test('Test_GetScheduledItemEndMinutes_TestParsedEnd_ExpectEndMinutes', () => {
   const startMinutes = ZooClockTimeHelper.parseMinutes('10:00');
   const endMinutes = ZooClockTimeHelper.parseMinutes('10:15');
   const scheduledItem = {
      startMinutes,
      maximumDuration: 8,
      endMinutes,
   };

   const result = ScheduledPillChecker.getScheduledItemEndMinutes(scheduledItem);

   assert.equal(result, endMinutes);
});


test('Test_GetScheduledItemEndMinutes_TestMissingEnd_ExpectNaN', () => {
   const scheduledItem = {
      startMinutes: ZooClockTimeHelper.parseMinutes('10:00'),
      maximumDuration: 8,
   };

   const result = ScheduledPillChecker.getScheduledItemEndMinutes(scheduledItem);

   assert.ok(Number.isNaN(result));
});


test('Test_GetScheduledItemTimeRange_TestStartAndEnd_ExpectRange', () => {
   const startMinutes = ZooClockTimeHelper.parseMinutes('9:30');
   const endMinutes = ZooClockTimeHelper.parseMinutes('10:00');
   const scheduledItem = { startMinutes, endMinutes };

   const range = ScheduledPillChecker.getScheduledItemTimeRange(scheduledItem);

   assert.deepEqual(range, {
      startMinutes: scheduledItem.startMinutes,
      endMinutes: scheduledItem.endMinutes,
   });
});


test('Test_GetScheduledPillVisualBand_TestShortVisit_ExpectMinDisplaySpan', () => {
   const startMinutes = ZooClockTimeHelper.parseMinutes('9:30');
   const durationMinutes = 2;
   const scheduledItem = makeScheduledItem('Capybara', startMinutes, durationMinutes, startMinutes);

   const band = ScheduledPillChecker.getScheduledPillVisualBand(scheduledItem);

   assert.equal(
      band.endMinutes - band.startMinutes,
      ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   );
});


test('Test_GetScheduledPillVisualBand_TestClusteredSummary_ExpectSpan', () => {
   const firstStart = ZooClockTimeHelper.parseMinutes('9:30');
   const secondStart = ZooClockTimeHelper.parseMinutes('9:35');
   const durationMinutes = 2;

   const band = ScheduledPillChecker.getScheduledPillVisualBand({
      summaryItems: [
         makeScheduledItem('Capybara', firstStart, durationMinutes, firstStart),
         makeScheduledItem('Cheetah', secondStart, durationMinutes, firstStart),
      ],
   });

   assert.ok(band.startMinutes < firstStart);
   assert.ok(band.endMinutes > firstStart + durationMinutes);
});


test('Test_DoScheduledTimeRangesOverlap_TestOverlappingWindows_ExpectTrue', () => {
   const left = {
      startMinutes: ZooClockTimeHelper.parseMinutes('9:30'),
      endMinutes: ZooClockTimeHelper.parseMinutes('10:00'),
   };
   const right = {
      startMinutes: ZooClockTimeHelper.parseMinutes('9:50'),
      endMinutes: ZooClockTimeHelper.parseMinutes('10:20'),
   };

   const overlaps = ScheduledPillChecker.doScheduledTimeRangesOverlap(left, right);

   assert.equal(overlaps, true);
});


test('Test_DoScheduledTimeRangesOverlap_TestTouchingWindows_ExpectFalse', () => {
   const left = {
      startMinutes: ZooClockTimeHelper.parseMinutes('9:30'),
      endMinutes: ZooClockTimeHelper.parseMinutes('10:00'),
   };
   const right = {
      startMinutes: left.endMinutes,
      endMinutes: left.endMinutes + TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
   };

   const overlaps = ScheduledPillChecker.doScheduledTimeRangesOverlap(left, right);

   assert.equal(overlaps, false);
});


test('Test_ScheduledPillsOverlapInDefaultPosition_TestWithinSlot_ExpectTrue', () => {
   const startMinutes = ZooClockTimeHelper.parseMinutes('9:30');
   const laterStart = ZooClockTimeHelper.parseMinutes('9:35');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

   const overlaps = ScheduledPillChecker.scheduledPillsOverlapInDefaultPosition(
      makeScheduledItem('Capybara', startMinutes, durationMinutes),
      makeScheduledItem('Cheetah', laterStart, durationMinutes)
   );

   assert.equal(overlaps, true);
});


test('Test_ScheduledPillsOverlapInDefaultPosition_TestBackToBackSlots_ExpectFalse', () => {
   const firstStart = ZooClockTimeHelper.parseMinutes('9:30');
   const secondStart = ZooClockTimeHelper.parseMinutes('10:00');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

   const overlaps = ScheduledPillChecker.scheduledPillsOverlapInDefaultPosition(
      makeScheduledItem('Capybara', firstStart, durationMinutes, firstStart),
      makeScheduledItem('Greater One-Horned Rhinoceros', secondStart, durationMinutes, secondStart)
   );

   assert.equal(overlaps, false);
});


test('Test_ComputeFirstFreeHorizontalOffsetIndex_TestOpenColumn_ExpectSecond', () => {
   const startMinutes = ZooClockTimeHelper.parseMinutes('9:30');
   const laterStart = ZooClockTimeHelper.parseMinutes('9:35');
   const laterSlot = ZooClockTimeHelper.parseMinutes('10:30');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const placedItems = [
      { ...makeScheduledItem('Capybara', startMinutes, durationMinutes), horizontalOffsetIndex: Position.FIRST },
      { ...makeScheduledItem('Red Panda', laterSlot, durationMinutes), horizontalOffsetIndex: Position.THIRD },
   ];

   const index = ScheduledPillChecker.computeFirstFreeHorizontalOffsetIndex(
      placedItems,
      makeScheduledItem('Cheetah', laterStart, durationMinutes)
   );

   assert.equal(index, Position.SECOND);
});


test('Test_ComputeFirstFreeHorizontalOffsetIndex_TestBlockedColumns_ExpectPastMax', () => {
   const startMinutes = ZooClockTimeHelper.parseMinutes('9:30');
   const laterStart = ZooClockTimeHelper.parseMinutes('9:35');
   const blockedStart = ZooClockTimeHelper.parseMinutes('9:36');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const candidate = makeScheduledItem('Cheetah', laterStart, durationMinutes);
   const placedItems = [
      { ...makeScheduledItem('Capybara', startMinutes, durationMinutes), horizontalOffsetIndex: Position.FIRST },
      { ...makeScheduledItem('Red Panda', blockedStart, durationMinutes), horizontalOffsetIndex: Position.SECOND },
   ];

   const index = ScheduledPillChecker.computeFirstFreeHorizontalOffsetIndex(placedItems, candidate);

   assert.equal(index, ScheduledPillChecker.MAX_TIMELINE_PILL_COLUMNS);
});


test('Test_FormatScheduledPillGroupLabel_TestSingleViewingSpot_ExpectLabel', () => {
   const label = 'Marabou Stork • Savanna Overlook';
   const items = [{ label }];

   const groupLabel = ScheduledPillChecker.formatScheduledPillGroupLabel(items);

   assert.equal(groupLabel, label);
});


test('Test_FormatScheduledPillGroupLabel_TestTwoViewingSpots_ExpectCounted', () => {
   const firstLabel = 'Marabou Stork • Savanna Overlook';
   const items = [
      { label: firstLabel },
      { label: 'Southern Ground Hornbill • Savanna Overlook' },
   ];

   const groupLabel = ScheduledPillChecker.formatScheduledPillGroupLabel(items);

   assert.equal(
      groupLabel,
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(firstLabel, items.length - 1)
   );
});


test('Test_FormatScheduledPillGroupLabel_TestSingleAnimal_ExpectLabel', () => {
   const label = 'African Lion';
   const items = [{ label }];

   const groupLabel = ScheduledPillChecker.formatScheduledPillGroupLabel(items);

   assert.equal(groupLabel, label);
});


test('Test_FormatScheduledPillGroupLabel_TestTwoAnimals_ExpectCounted', () => {
   const firstLabel = 'African Lion';
   const items = [
      { label: firstLabel },
      { label: 'Cheetah' },
   ];

   const groupLabel = ScheduledPillChecker.formatScheduledPillGroupLabel(items);

   assert.equal(
      groupLabel,
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(firstLabel, items.length - 1)
   );
});


test('Test_FormatScheduledPillGroupLabel_TestLongestVisit_ExpectPreferred', () => {
   const giraffe = 'Masai Giraffe';
   const items = [
      { label: 'Lake Malawi Cichlid', maximumDuration: 2 },
      { label: giraffe, maximumDuration: TimelineLayoutConstants.TIMELINE_SLOT_MINUTES },
   ];

   const groupLabel = ScheduledPillChecker.formatScheduledPillGroupLabel(items);

   assert.equal(
      groupLabel,
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(giraffe, items.length - 1)
   );
});


test('Test_GetScheduledItemMaximumDuration_TestEndMinusStart_ExpectDuration', () => {
   const startMinutes = ZooClockTimeHelper.parseMinutes('10:00');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const scheduledItem = {
      startMinutes,
      endMinutes: startMinutes + durationMinutes,
   };

   const duration = ScheduledPillChecker.getScheduledItemMaximumDuration(scheduledItem);

   assert.equal(duration, durationMinutes);
});


test('Test_FormatScheduledPillGroupLabel_TestEmpty_ExpectBlank', () => {
   const items = [];

   const groupLabel = ScheduledPillChecker.formatScheduledPillGroupLabel(items);

   assert.equal(groupLabel, '');
});


test('Test_SortScheduledItemsForGroupDisplay_TestMaxDuration_ExpectOrdered', () => {
   const giraffe = { label: 'Masai Giraffe', maximumDuration: TimelineLayoutConstants.TIMELINE_SLOT_MINUTES };
   const panda = { label: 'Red Panda', maximumDuration: 8 };
   const cichlid = { label: 'Lake Malawi Cichlid', maximumDuration: 2 };
   const items = [cichlid, giraffe, panda];

   const sorted = ScheduledPillChecker.sortScheduledItemsForGroupDisplay(items);

   assert.deepEqual(
      sorted.map((item) => item.label),
      [giraffe.label, panda.label, cichlid.label]
   );
});
