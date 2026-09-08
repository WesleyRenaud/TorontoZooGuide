import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerTimelineRenderer } from '../../../../scripts/itinerary/panel/dayPlannerTimelineRenderer.js';

test('Test_BuildItineraryTimeMarkers_TestArrivalDeparture_ExpectMarkers', () => {
   const markers = DayPlannerTimelineRenderer.buildItineraryTimeMarkers(
      {
         arrivalTime: '10:00',
         departureTime: '16:00',
         itineraryConfig: {
            visitBoundaryEventTypes: {
               arrival: 'arrival',
               departure: 'departure',
            },
         },
      },
      {
         arrivalLabel: 'Arrive',
         departureLabel: 'Depart',
      }
   );

   assert.deepEqual(markers, [
      { startMinutes: 600, label: 'Arrive', kind: 'arrival' },
      { startMinutes: 960, label: 'Depart', kind: 'departure' },
   ]);
});

test('Test_BuildItineraryTimeMarkers_TestMissingParts_ExpectFiltered', () => {
   assert.deepEqual(
      DayPlannerTimelineRenderer.buildItineraryTimeMarkers(
         { arrivalTime: 'bad', departureTime: '16:00' },
         { arrivalLabel: 'Arrive', departureLabel: 'Depart' }
      ),
      []
   );
});

test('Test_FindTimelineAnchorSlot_TestSlots_ExpectNearestNotAfter', () => {
   assert.equal(DayPlannerTimelineRenderer.findTimelineAnchorSlot(75, [0, 30, 60, 90]), 60);
   assert.equal(DayPlannerTimelineRenderer.findTimelineAnchorSlot(10, []), null);
   assert.equal(DayPlannerTimelineRenderer.findTimelineAnchorSlot(NaN, [0, 30]), null);
});

test('Test_FindTimelineSlotEndMinutes_TestAnchor_ExpectNextOrFallback', () => {
   assert.equal(
      DayPlannerTimelineRenderer.findTimelineSlotEndMinutes(30, [0, 30, 60], 99),
      60
   );
   assert.equal(
      DayPlannerTimelineRenderer.findTimelineSlotEndMinutes(60, [0, 30, 60], 99),
      99
   );
});

test('Test_ComputeMarkerOffsetFraction_TestSpan_ExpectFraction', () => {
   assert.equal(DayPlannerTimelineRenderer.computeMarkerOffsetFraction(30, 30, 60), 0);
   assert.equal(DayPlannerTimelineRenderer.computeMarkerOffsetFraction(45, 30, 60), 0.5);
   assert.equal(DayPlannerTimelineRenderer.computeMarkerOffsetFraction(45, 30, 30), 0);
});

test('Test_BuildMarkersByAnchorSlot_TestMarkers_ExpectGroupedOffsets', () => {
   const markersMap = DayPlannerTimelineRenderer.buildMarkersByAnchorSlot(
      [
         { startMinutes: 45, label: 'Arrive', kind: 'arrival' },
         { startMinutes: 90, label: 'Depart', kind: 'departure' },
      ],
      [0, 30, 60],
      120
   );

   assert.deepEqual(markersMap.get(30), [
      { label: 'Arrive', offsetFraction: 0.5, kind: 'arrival' },
   ]);
   assert.deepEqual(markersMap.get(60), [
      { label: 'Depart', offsetFraction: 0.5, kind: 'departure' },
   ]);
});

test('Test_ResolveTimelinePillLabel_TestBoundarySlots_ExpectLabels', () => {
   const hours = {
      earlyAdmissionMinutes: 480,
      openMinutes: 540,
      lastAdmissionMinutes: 960,
      closeMinutes: 1020,
   };
   const strings = {
      earlyAdmissionLabel: 'Early',
      openLabel: 'Open',
      lastAdmissionLabel: 'Last',
      closeLabel: 'Close',
   };

   assert.equal(DayPlannerTimelineRenderer.resolveTimelinePillLabel(480, hours, strings), 'Early');
   assert.equal(DayPlannerTimelineRenderer.resolveTimelinePillLabel(540, hours, strings), 'Open');
   assert.equal(DayPlannerTimelineRenderer.resolveTimelinePillLabel(960, hours, strings), 'Last');
   assert.equal(DayPlannerTimelineRenderer.resolveTimelinePillLabel(1020, hours, strings), 'Close');
   assert.equal(DayPlannerTimelineRenderer.resolveTimelinePillLabel(600, hours, strings), null);
});
