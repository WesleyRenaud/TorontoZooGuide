import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledPillChecker } from '../../../../../scripts/itinerary/panel/components/scheduledPillChecker.js';
import { ScheduledPillLayoutHelper } from '../../../../../scripts/itinerary/panel/components/scheduledPillLayoutHelper.js';
import { ScheduledPillRenderPlanBuilder } from '../../../../../scripts/itinerary/panel/components/scheduledPillRenderPlanBuilder.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { ZooClockTimeHelper } from '../../../../../scripts/shared/zooClockTimeHelper.js';


test('Test_AppendRenderGroup_TestAnchor_ExpectGrouped', () => {
   const startMinutes = ZooClockTimeHelper.parseMinutes('10:00');
   const lionGroup = { id: 'african-lion' };
   const tigerGroup = { id: 'amur-tiger' };
   const groupsByAnchor = new Map();

   ScheduledPillRenderPlanBuilder.appendRenderGroup(groupsByAnchor, startMinutes, lionGroup);
   ScheduledPillRenderPlanBuilder.appendRenderGroup(groupsByAnchor, startMinutes, tigerGroup);

   assert.deepEqual(groupsByAnchor.get(startMinutes), [lionGroup, tigerGroup]);
});


test('Test_BuildRenderGroup_TestLayoutUnit_ExpectPlan', () => {
   const startMinutes = ZooClockTimeHelper.parseMinutes('10:00');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES * 2;
   const endMinutes = startMinutes + durationMinutes;
   const slotEndMinutes = startMinutes + TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const horizontalOffsetIndex = Position.SECOND;
   const layoutUnit = {
      startMinutes,
      endMinutes,
      anchorSlotMinutes: startMinutes,
      slotEndMinutes,
   };

   const plan = ScheduledPillRenderPlanBuilder.buildRenderGroup(
      layoutUnit,
      horizontalOffsetIndex
   );
   const slotContext = ScheduledPillLayoutHelper.getLayoutUnitSlotContext(layoutUnit);

   assert.equal(plan.items.length, 1);
   assert.equal(plan.horizontalOffsetIndex, horizontalOffsetIndex);
   assert.equal(plan.durationMinutes, endMinutes - startMinutes);
   assert.ok(
      plan.displayDurationMinutes >= ScheduledPillChecker.getScheduledPillMinDisplayMinutes()
   );
   assert.ok(plan.displayDurationMinutes >= plan.durationMinutes);
   assert.equal(plan.slotSpanMinutes, slotContext.slotSpanMinutes);
});


test('Test_CompareRenderGroupsForDisplay_TestEarlierOffset_ExpectBefore', () => {
   const leftGroup = { offsetFraction: 0.1, horizontalOffsetIndex: Position.FIRST };
   const rightGroup = { offsetFraction: 0.5, horizontalOffsetIndex: Position.FIRST };

   const comparison = ScheduledPillRenderPlanBuilder.compareRenderGroupsForDisplay(
      leftGroup,
      rightGroup
   );

   assert.ok(comparison < 0);
});


test('Test_CompareRenderGroupsForDisplay_TestLaterColumn_ExpectAfter', () => {
   const offsetFraction = 0.2;
   const leftGroup = { offsetFraction, horizontalOffsetIndex: Position.THIRD };
   const rightGroup = { offsetFraction, horizontalOffsetIndex: Position.SECOND };

   const comparison = ScheduledPillRenderPlanBuilder.compareRenderGroupsForDisplay(
      leftGroup,
      rightGroup
   );

   assert.ok(comparison > 0);
});


test('Test_AssignLayoutUnitsByRenderAnchor_TestUnits_ExpectMap', () => {
   const morningStart = ZooClockTimeHelper.parseMinutes('10:00');
   const laterStart = ZooClockTimeHelper.parseMinutes('11:00');
   const slotMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const morningUnit = {
      startMinutes: morningStart,
      endMinutes: morningStart + slotMinutes,
      anchorSlotMinutes: morningStart,
   };
   const laterUnit = {
      startMinutes: laterStart,
      endMinutes: laterStart + slotMinutes,
      anchorSlotMinutes: laterStart,
   };
   const unanchoredUnit = {
      startMinutes: morningStart + 10,
      endMinutes: morningStart + 20,
   };

   const byAnchor = ScheduledPillRenderPlanBuilder.assignLayoutUnitsByRenderAnchor([
      morningUnit,
      laterUnit,
      unanchoredUnit,
   ]);

   assert.deepEqual(byAnchor.get(morningStart), [morningUnit]);
   assert.deepEqual(byAnchor.get(laterStart), [laterUnit]);
});
