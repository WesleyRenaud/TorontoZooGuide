import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeScheduledItem } from '../../../helpers/scheduledPillTestSetup.mjs';
import { ScheduledPillChecker } from '../../../../../scripts/itinerary/panel/components/scheduledPillChecker.js';
import { ScheduledPillRenderBuilder } from '../../../../../scripts/itinerary/panel/components/scheduledPillRenderBuilder.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { ZooClockTimeHelper } from '../../../../../scripts/shared/zooClockTimeHelper.js';
import { Strings } from '../../../../../scripts/strings.js';

function _minutes(clockTime) {
   return ZooClockTimeHelper.parseMinutes(clockTime);
}

function _groupLabel(group) {
   return group.label ?? group.items.at(Position.FIRST).label;
}


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestSequentialVisits_ExpectFirstColumn', () => {
   const firstStart = _minutes('9:30');
   const secondStart = _minutes('10:00');
   const thirdStart = _minutes('10:30');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Capybara', firstStart, durationMinutes, firstStart),
      makeScheduledItem('Greater One-Horned Rhinoceros', secondStart, durationMinutes, secondStart),
      makeScheduledItem('Indian Peafowl', thirdStart, durationMinutes, thirdStart),
   ]);

   assert.deepEqual(
      groupsByAnchor.get(firstStart)?.map((group) => group.horizontalOffsetIndex),
      [Position.FIRST]
   );
   assert.deepEqual(
      groupsByAnchor.get(secondStart)?.map((group) => group.horizontalOffsetIndex),
      [Position.FIRST]
   );
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestShortVisits_ExpectClustered', () => {
   const startMinutes = _minutes('9:30');
   const capybara = 'Capybara';
   const extraCount = 1;

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem(capybara, startMinutes, 2, startMinutes),
      makeScheduledItem('Cheetah', startMinutes + 2, 2, startMinutes),
   ]);

   assert.equal(groupsByAnchor.get(startMinutes)?.length, 1);
   assert.equal(
      _groupLabel(groupsByAnchor.get(startMinutes).at(Position.FIRST)),
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(capybara, extraCount)
   );
   assert.deepEqual(
      groupsByAnchor.get(startMinutes)?.map((group) => group.horizontalOffsetIndex),
      [Position.FIRST]
   );
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestSameViewingStop_ExpectGrouped', () => {
   const firstStart = _minutes('10:00');
   const secondStart = _minutes('10:30');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const viewingWalkNodeId = 'v-0652';
   const penguin = 'African Penguin';

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem(penguin, firstStart, durationMinutes, firstStart, viewingWalkNodeId),
      makeScheduledItem('White-Breasted Cormorant', secondStart, durationMinutes, firstStart, viewingWalkNodeId),
   ]);

   assert.equal(groupsByAnchor.get(firstStart)?.length, 1);
   assert.equal(
      _groupLabel(groupsByAnchor.get(firstStart).at(Position.FIRST)),
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(penguin, 1)
   );
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestSameStopAcrossSlots_ExpectGrouped', () => {
   const firstStart = _minutes('10:00');
   const nextSlot = _minutes('10:30');
   const viewingWalkNodeId = 'v-0255';
   const meerkat = 'Slender-Tailed Meerkat';

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem(meerkat, firstStart, 3, firstStart, viewingWalkNodeId),
      makeScheduledItem('South African Crested Porcupine', firstStart + 3, 2, firstStart, viewingWalkNodeId),
      makeScheduledItem('Speckled Mousebird', firstStart + 5, 3, firstStart, viewingWalkNodeId),
      makeScheduledItem('Naked Mole Rat', firstStart + 8, 3, nextSlot, viewingWalkNodeId),
   ]);
   const group = groupsByAnchor.get(firstStart).at(Position.FIRST);

   assert.equal(groupsByAnchor.get(firstStart).length, 1);
   assert.equal(group.items.length, 4);
   assert.equal(
      group.label,
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(
         group.items.at(Position.FIRST).label,
         group.items.length - 1
      )
   );
   assert.equal(groupsByAnchor.get(nextSlot), undefined);
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestDifferentStops_ExpectSeparate', () => {
   const firstStart = _minutes('10:00');
   const secondStart = _minutes('10:30');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const gorilla = 'Western Lowland Gorilla';

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem(gorilla, firstStart, durationMinutes, firstStart, 'v-0247'),
      makeScheduledItem(gorilla, secondStart, durationMinutes, secondStart, 'v-0229'),
   ]);

   assert.equal(groupsByAnchor.get(firstStart)?.length, 1);
   assert.equal(groupsByAnchor.get(secondStart)?.length, 1);
   assert.equal(_groupLabel(groupsByAnchor.get(firstStart).at(Position.FIRST)), gorilla);
   assert.equal(_groupLabel(groupsByAnchor.get(secondStart).at(Position.FIRST)), gorilla);
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestConsecutiveBuckets_ExpectVisible', () => {
   const startMinutes = _minutes('16:30');
   const owl = 'Eurasian Eagle Owl';
   const stork = 'Marabou Stork';
   const flamingo = 'American Flamingo';
   const monkey = 'Black-Handed Spider Monkey';
   const capybara = 'Capybara';
   const seriema = 'Red-Legged Seriema';

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem(owl, startMinutes, 2, startMinutes),
      makeScheduledItem('Great Horned Owl', startMinutes + 2, 2, startMinutes),
      makeScheduledItem('Guinea Pig', startMinutes + 4, 1, startMinutes),
      makeScheduledItem('Harris Hawk', startMinutes + 5, 1, startMinutes),
      makeScheduledItem(stork, startMinutes + 6, 2, startMinutes),
      makeScheduledItem('Rabbit', startMinutes + 8, 2, startMinutes),
      makeScheduledItem(flamingo, startMinutes + 10, 5, startMinutes),
      makeScheduledItem(monkey, startMinutes + 15, 5, startMinutes),
      makeScheduledItem(capybara, startMinutes + 20, 5, startMinutes),
      makeScheduledItem(seriema, startMinutes + 25, 2, startMinutes),
      makeScheduledItem('Turkey Vulture', startMinutes + 27, 1, startMinutes),
   ]);
   const groupLabels = (groupsByAnchor.get(startMinutes) ?? []).map(_groupLabel);

   assert.deepEqual(groupLabels, [
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(owl, 1),
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(stork, 2),
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(flamingo, 1),
      monkey,
      capybara,
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(seriema, 1),
   ]);
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestNoGap_ExpectConsecutive', () => {
   const firstStart = _minutes('9:30');
   const secondStart = _minutes('10:00');
   const slotSpanMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

   const groups = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Clouded Leopard', firstStart, slotSpanMinutes, firstStart),
      makeScheduledItem('Bighead Carp', secondStart, 4, secondStart),
      makeScheduledItem('Crocodile Lizard', secondStart + 4, 4, secondStart),
      makeScheduledItem('Luzon Bleeding-Heart Dove', secondStart + 8, 4, secondStart),
      makeScheduledItem('Sumatran Orangutan', secondStart + 12, slotSpanMinutes, secondStart),
      makeScheduledItem('Tentacled Snake', secondStart + 42, 4, secondStart),
      makeScheduledItem('White-Handed Gibbon', secondStart + 46, 4, secondStart),
   ]).get(secondStart) ?? [];

   for (let index = 1; index < groups.length; index += 1) {
      const previousGroup = groups[index - 1];
      const previousEndOffset = (previousGroup.offsetFraction ?? 0)
         + ((previousGroup.durationMinutes ?? 0) / slotSpanMinutes);

      assert.ok(
         Math.abs((groups[index]?.offsetFraction ?? 0) - previousEndOffset) < 0.0001,
         `expected group ${index} to start where group ${index - 1} ends`
      );
   }
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestGappedUnderMin_ExpectMerged', () => {
   const startMinutes = _minutes('10:00');
   const partridge = 'Crested Wood Partridge';
   const firstDuration = 1;
   const lastDuration = 2;
   const lastStart = startMinutes + 4;

   const groups = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Bighead Carp', startMinutes, firstDuration, startMinutes),
      makeScheduledItem('Black-Breasted Leaf Turtle', startMinutes + 1, firstDuration, startMinutes),
      makeScheduledItem('Burmese Star Tortoise', startMinutes + 3, firstDuration, startMinutes),
      makeScheduledItem(partridge, lastStart, lastDuration, startMinutes),
   ]).get(startMinutes) ?? [];
   const group = groups.at(Position.FIRST);
   const durationMinutes = (lastStart + lastDuration) - startMinutes;

   assert.equal(groups.length, 1);
   assert.equal(_groupLabel(group), Strings.itinerary.dayPlanner.scheduledPillGroupLabel(partridge, 3));
   assert.equal(group?.durationMinutes, durationMinutes);
   assert.equal(group?.displayDurationMinutes, durationMinutes);
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestRealGaps_ExpectKept', () => {
   const startMinutes = _minutes('10:00');
   const peafowl = 'Indian Peafowl';
   const dove = 'Luzon Bleeding-Heart Dove';
   const firstDuration = 1;
   const secondDuration = 2;

   const groups = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem(peafowl, startMinutes, firstDuration, startMinutes),
      makeScheduledItem(dove, startMinutes + 25, secondDuration, startMinutes),
   ]).get(startMinutes) ?? [];

   assert.equal(groups.length, 2);
   assert.deepEqual(groups.map(_groupLabel), [peafowl, dove]);
   assert.equal(groups.at(Position.FIRST)?.durationMinutes, firstDuration);
   assert.equal(
      groups.at(Position.FIRST)?.displayDurationMinutes,
      ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   );
   assert.equal(groups.at(Position.SECOND)?.durationMinutes, secondDuration);
   assert.equal(
      groups.at(Position.SECOND)?.displayDurationMinutes,
      ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   );
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestStartTimes_ExpectOffsets', () => {
   const startMinutes = _minutes('9:30');
   const slotMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const sloth = 'Two-Toed Sloth';

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem(sloth, startMinutes, slotMinutes, startMinutes),
      ...Array.from({ length: 9 }, (_, index) => (
         makeScheduledItem(
            `Fish ${index + 1}`,
            startMinutes + 1 + index,
            2,
            startMinutes
         )
      )),
   ]);
   const groups = groupsByAnchor.get(startMinutes);

   assert.equal(_groupLabel(groups.at(Position.FIRST)), sloth);
   assert.equal(groups.at(Position.FIRST).offsetFraction, 0);
   groups.slice(1).forEach((group) => {
      const firstItem = group.items.at(Position.FIRST);
      const expectedOffset = (firstItem.startMinutes - startMinutes) / slotMinutes;

      assert.ok(
         Math.abs(group.offsetFraction - expectedOffset) < 0.0001,
         `expected ${_groupLabel(group)} at offset ${expectedOffset}`
      );
   });
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestNextSlot_ExpectNaturalOffset', () => {
   const firstStart = _minutes('9:30');
   const nextStart = _minutes('10:00');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Capybara', firstStart, durationMinutes, firstStart),
      makeScheduledItem('Cheetah', firstStart + 1, durationMinutes, firstStart),
      makeScheduledItem('Red Panda', nextStart, 2, nextStart),
   ]);
   const nextSlotGroups = groupsByAnchor.get(nextStart);

   assert.equal(nextSlotGroups.length, 1);
   assert.equal(nextSlotGroups.at(Position.FIRST).offsetFraction, 0);
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestOverlappingFullVisits_ExpectSeparate', () => {
   const startMinutes = _minutes('9:30');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const capybara = 'Capybara';
   const cheetah = 'Cheetah';

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem(capybara, startMinutes, durationMinutes, startMinutes),
      makeScheduledItem(cheetah, startMinutes + 6, durationMinutes, startMinutes),
   ]);

   assert.equal(groupsByAnchor.get(startMinutes)?.length, 2);
   assert.deepEqual(
      groupsByAnchor.get(startMinutes)?.map(_groupLabel),
      [capybara, cheetah]
   );
   assert.deepEqual(
      groupsByAnchor.get(startMinutes)?.map((group) => group.horizontalOffsetIndex),
      [Position.FIRST, Position.FIRST]
   );
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestTailOrphan_ExpectMerged', () => {
   const anchorMinutes = _minutes('16:30');
   const firstStart = _minutes('16:45');
   const firstDuration = 10;
   const secondStart = _minutes('16:55');
   const secondDuration = 2;
   const slotEndMinutes = _minutes('17:00');
   const monkey = 'Black-Handed Spider Monkey';
   const withSlotEnd = (item, endMinutes) => ({ ...item, slotEndMinutes: endMinutes });

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      withSlotEnd(makeScheduledItem(monkey, firstStart, firstDuration, anchorMinutes), slotEndMinutes),
      withSlotEnd(makeScheduledItem('Red-Legged Seriema', secondStart, secondDuration, anchorMinutes), slotEndMinutes),
   ]);
   const groups = groupsByAnchor.get(anchorMinutes) ?? [];
   const group = groups.at(Position.FIRST);
   const durationMinutes = (secondStart + secondDuration) - firstStart;

   assert.equal(groups.length, 1);
   assert.equal(_groupLabel(group), Strings.itinerary.dayPlanner.scheduledPillGroupLabel(monkey, 1));
   assert.equal(group?.durationMinutes, durationMinutes);
   assert.equal(group?.displayDurationMinutes, durationMinutes);
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestIsolatedShortVisit_ExpectMinHeight', () => {
   const beforeStart = _minutes('15:30');
   const startMinutes = _minutes('16:00');
   const afterStart = _minutes('16:30');
   const durationMinutes = 2;
   const slotMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const bird = 'Black-Throated Laughingthrush';

   const groups = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Greater One-Horned Rhinoceros', beforeStart, slotMinutes, beforeStart),
      makeScheduledItem(bird, startMinutes, durationMinutes, startMinutes),
      makeScheduledItem('Red Panda', afterStart, slotMinutes, afterStart),
   ]).get(startMinutes) ?? [];
   const group = groups.at(Position.FIRST);

   assert.equal(groups.length, 1);
   assert.equal(_groupLabel(group), bird);
   assert.equal(group?.durationMinutes, durationMinutes);
   assert.equal(
      group?.displayDurationMinutes,
      ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   );
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestFullWidth_ExpectFirstColumn', () => {
   const anchorMinutes = _minutes('16:30');
   const startMinutes = _minutes('16:55');

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor(
      [
         makeScheduledItem('Red-Legged Seriema', startMinutes, 2, anchorMinutes),
      ],
      [
         { startMinutes: _minutes('17:00') },
      ]
   );

   assert.deepEqual(
      groupsByAnchor.get(anchorMinutes)?.map((group) => group.horizontalOffsetIndex),
      [Position.FIRST]
   );
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestOverlappingCarousel_ExpectGroups', () => {
   const startMinutes = _minutes('16:00');
   const snowLeopard = 'Snow Leopard';
   const eagle = 'Steller Sea Eagle';
   const tur = 'West Caucasian Tur';
   const goat = 'Domestic Goat';

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem(snowLeopard, startMinutes + 11, 8, startMinutes),
      makeScheduledItem(eagle, startMinutes + 19, 3, startMinutes),
      makeScheduledItem(tur, startMinutes + 22, 3, startMinutes),
      makeScheduledItem(goat, startMinutes + 25, 3, startMinutes),
      makeScheduledItem('African Spurred Tortoise', startMinutes + 28, 1, startMinutes),
      makeScheduledItem('Common Raven', startMinutes + 29, 1, startMinutes),
   ]);
   const groups = groupsByAnchor.get(startMinutes) ?? [];

   assert.equal(groups.length, 4);
   assert.deepEqual(groups.map(_groupLabel), [
      snowLeopard,
      eagle,
      tur,
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(goat, 2),
   ]);
   assert.equal(groups.at(Position.FIRST)?.items.length, 1);
   assert.equal(groups.at(Position.FOURTH)?.items.length, 3);
});


test('Test_PlanScheduledPillRenderGroupsByAnchor_TestFullLengthVisits_ExpectOwnPills', () => {
   const startMinutes = _minutes('9:30');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const labels = [
      'Capybara',
      'Cheetah',
      'Red Panda',
      'Masai Giraffe',
      'Ostrich',
      'African Lion',
   ];
   const scheduledItems = labels.map((label, labelIndex) => (
      makeScheduledItem(label, startMinutes + labelIndex, durationMinutes, startMinutes)
   ));

   const groupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor(scheduledItems);
   const groups = groupsByAnchor.get(startMinutes) ?? [];

   assert.equal(groups.length, labels.length);
   assert.deepEqual(groups.map(_groupLabel), labels);
   assert.equal(
      ScheduledPillChecker.MAX_TIMELINE_PILL_COLUMNS,
      TimelineLayoutConstants.MAX_TIMELINE_PILL_COLUMNS
   );
   assert.equal(
      ScheduledPillChecker.MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS,
      TimelineLayoutConstants.MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS
   );
});
