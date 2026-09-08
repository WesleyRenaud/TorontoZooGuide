import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledPillRenderPlanBuilder } from '../../../../../scripts/itinerary/panel/components/scheduledPillRenderPlanBuilder.js';

test('Test_AppendRenderGroup_TestAnchor_ExpectGrouped', () => {
   const groupsByAnchor = new Map();
   ScheduledPillRenderPlanBuilder.appendRenderGroup(groupsByAnchor, 600, { id: 'a' });
   ScheduledPillRenderPlanBuilder.appendRenderGroup(groupsByAnchor, 600, { id: 'b' });

   assert.equal(groupsByAnchor.get(600).length, 2);
});

test('Test_BuildRenderGroup_TestLayoutUnit_ExpectPlan', () => {
   const plan = ScheduledPillRenderPlanBuilder.buildRenderGroup({
      startMinutes: 600,
      endMinutes: 660,
      anchorSlotMinutes: 600,
      slotEndMinutes: 630,
   }, 1);

   assert.equal(plan.items.length, 1);
   assert.equal(plan.horizontalOffsetIndex, 1);
   assert.equal(plan.durationMinutes, 60);
   assert.ok(plan.displayDurationMinutes >= 60);
   assert.equal(plan.slotSpanMinutes, 30);
});

test('Test_CompareRenderGroupsForDisplay_TestOffsets_ExpectOrder', () => {
   assert.ok(ScheduledPillRenderPlanBuilder.compareRenderGroupsForDisplay(
      { offsetFraction: 0.1, horizontalOffsetIndex: 0 },
      { offsetFraction: 0.5, horizontalOffsetIndex: 0 }
   ) < 0);
   assert.ok(ScheduledPillRenderPlanBuilder.compareRenderGroupsForDisplay(
      { offsetFraction: 0.2, horizontalOffsetIndex: 2 },
      { offsetFraction: 0.2, horizontalOffsetIndex: 1 }
   ) > 0);
});

test('Test_AssignLayoutUnitsByRenderAnchor_TestUnits_ExpectMap', () => {
   const byAnchor = ScheduledPillRenderPlanBuilder.assignLayoutUnitsByRenderAnchor([
      { startMinutes: 600, endMinutes: 630, anchorSlotMinutes: 600 },
      { startMinutes: 660, endMinutes: 690, anchorSlotMinutes: 660 },
      { startMinutes: 610, endMinutes: 620 },
   ]);

   assert.equal(byAnchor.get(600).length, 1);
   assert.equal(byAnchor.get(660).length, 1);
});
