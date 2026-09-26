import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerTimelinePillAppendHelper } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillAppendHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ApplyPointPillStripPlacement_TestEmptyPlacement_ExpectNoAttribute', () => {
   const strip = document.createElement('div');

   DayPlannerTimelinePillAppendHelper.applyPointPillStripPlacement(strip, '');

   assert.equal(strip.getAttribute('data-visit-boundary-placement'), null);
});


test('Test_ApplyPointPillStripPlacement_TestPlacement_ExpectAttribute', () => {
   const strip = document.createElement('div');
   const placement = 'ends-at-anchor';

   DayPlannerTimelinePillAppendHelper.applyPointPillStripPlacement(strip, placement);

   assert.equal(strip.getAttribute('data-visit-boundary-placement'), placement);
});


test('Test_InsertPointPillInStrip_TestPill_ExpectAppended', () => {
   const strip = document.createElement('div');
   const pill = document.createElement('div');

   DayPlannerTimelinePillAppendHelper.insertPointPillInStrip(strip, pill);

   assert.equal(strip.children.length, 1);
});


test('Test_ResolveTimePillOptions_TestArrival_ExpectEndsAtAnchor', () => {
   const arrivalKind = 'arrival';
   const arrivalTimeMenuAria = 'Arrival menu';
   const cleared = [];

   const options = DayPlannerTimelinePillAppendHelper.resolveTimePillOptions(
      { kind: arrivalKind },
      { onArrivalTimeChange: (value) => { cleared.push(value); } },
      {
         arrivalTimeMenuAria,
         remove: 'Remove',
      },
      { arrival: arrivalKind, departure: 'departure' }
   );
   options.onRemove();

   assert.equal(options.menuAriaLabel, arrivalTimeMenuAria);
   assert.equal(options.visitBoundaryPlacement, 'ends-at-anchor');
   assert.deepEqual(cleared, ['']);
});


test('Test_ResolveTimePillOptions_TestDeparture_ExpectStartsAtAnchor', () => {
   const departureKind = 'departure';
   const departureTimeMenuAria = 'Departure menu';
   const cleared = [];

   const options = DayPlannerTimelinePillAppendHelper.resolveTimePillOptions(
      { kind: departureKind },
      { onDepartureTimeChange: (value) => { cleared.push(value); } },
      {
         departureTimeMenuAria,
         remove: 'Remove',
      },
      { arrival: 'arrival', departure: departureKind }
   );
   options.onRemove();

   assert.equal(options.menuAriaLabel, departureTimeMenuAria);
   assert.equal(options.visitBoundaryPlacement, 'starts-at-anchor');
   assert.deepEqual(cleared, ['']);
});


test('Test_ResolveTimePillOptions_TestOtherKind_ExpectEmpty', () => {
   const marker = { kind: 'animal' };
   const visitBoundaryEventTypes = { arrival: 'arrival', departure: 'departure' };

   const options = DayPlannerTimelinePillAppendHelper.resolveTimePillOptions(
      marker,
      {},
      {},
      visitBoundaryEventTypes
   );

   assert.deepEqual(options, {});
});
