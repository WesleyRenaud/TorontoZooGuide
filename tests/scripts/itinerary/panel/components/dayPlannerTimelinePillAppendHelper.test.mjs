import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerTimelinePillAppendHelper } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillAppendHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ApplyPointPillStripPlacement_TestPlacement_ExpectAttribute', () => {
   const strip = document.createElement('div');
   DayPlannerTimelinePillAppendHelper.applyPointPillStripPlacement(strip, '');
   assert.equal(strip.getAttribute('data-visit-boundary-placement'), null);

   DayPlannerTimelinePillAppendHelper.applyPointPillStripPlacement(strip, 'ends-at-anchor');
   assert.equal(strip.getAttribute('data-visit-boundary-placement'), 'ends-at-anchor');
});

test('Test_InsertPointPillInStrip_TestPill_ExpectAppended', () => {
   const strip = document.createElement('div');
   const pill = document.createElement('div');
   DayPlannerTimelinePillAppendHelper.insertPointPillInStrip(strip, pill);
   assert.equal(strip.children.length, 1);
});

test('Test_ResolveTimePillOptions_TestArrival_ExpectEndsAtAnchor', () => {
   const cleared = [];
   const options = DayPlannerTimelinePillAppendHelper.resolveTimePillOptions(
      { kind: 'arrival' },
      { onArrivalTimeChange: (value) => { cleared.push(value); } },
      {
         arrivalTimeMenuAria: 'Arrival menu',
         remove: 'Remove',
      },
      { arrival: 'arrival', departure: 'departure' }
   );

   assert.equal(options.menuAriaLabel, 'Arrival menu');
   assert.equal(options.visitBoundaryPlacement, 'ends-at-anchor');
   options.onRemove();
   assert.deepEqual(cleared, ['']);
});

test('Test_ResolveTimePillOptions_TestDeparture_ExpectStartsAtAnchor', () => {
   const cleared = [];
   const options = DayPlannerTimelinePillAppendHelper.resolveTimePillOptions(
      { kind: 'departure' },
      { onDepartureTimeChange: (value) => { cleared.push(value); } },
      {
         departureTimeMenuAria: 'Departure menu',
         remove: 'Remove',
      },
      { arrival: 'arrival', departure: 'departure' }
   );

   assert.equal(options.menuAriaLabel, 'Departure menu');
   assert.equal(options.visitBoundaryPlacement, 'starts-at-anchor');
   options.onRemove();
   assert.deepEqual(cleared, ['']);
});

test('Test_ResolveTimePillOptions_TestOtherKind_ExpectEmpty', () => {
   assert.deepEqual(DayPlannerTimelinePillAppendHelper.resolveTimePillOptions(
      { kind: 'animal' },
      {},
      {},
      { arrival: 'arrival', departure: 'departure' }
   ), {});
});
