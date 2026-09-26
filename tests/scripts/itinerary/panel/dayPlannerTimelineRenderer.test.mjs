import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerScheduleController } from '../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { DayPlannerTimelineRenderer } from '../../../../scripts/itinerary/panel/dayPlannerTimelineRenderer.js';
import { ItineraryEventTypes } from '../../../../scripts/itinerary/itineraryEventTypes.js';
import { Position } from '../../../../scripts/shared/enums/position.js';


test('Test_BuildItineraryTimeMarkers_TestArrivalDeparture_ExpectMarkers', () => {
   const arrivalTime = '10:00';
   const departureTime = '16:00';
   const arrivalLabel = 'Arrive';
   const departureLabel = 'Depart';
   const visitBoundaryEventTypes = {
      arrival: 'arrival',
      departure: 'departure',
   };

   const markers = DayPlannerTimelineRenderer.buildItineraryTimeMarkers(
      {
         arrivalTime,
         departureTime,
         itineraryConfig: { visitBoundaryEventTypes },
      },
      { arrivalLabel, departureLabel }
   );

   const normalizedKinds = ItineraryEventTypes.normalizeVisitBoundaryEventTypes(visitBoundaryEventTypes);
   assert.deepEqual(markers, [
      {
         startMinutes: DayPlannerScheduleController.parseClockTimeMinutes(arrivalTime),
         label: arrivalLabel,
         kind: normalizedKinds.arrival,
      },
      {
         startMinutes: DayPlannerScheduleController.parseClockTimeMinutes(departureTime),
         label: departureLabel,
         kind: normalizedKinds.departure,
      },
   ]);
});


test('Test_BuildItineraryTimeMarkers_TestMissingParts_ExpectFiltered', () => {
   const arrivalTime = 'bad';
   const departureTime = '16:00';

   const markers = DayPlannerTimelineRenderer.buildItineraryTimeMarkers(
      { arrivalTime, departureTime },
      { arrivalLabel: 'Arrive', departureLabel: 'Depart' }
   );

   assert.deepEqual(markers, []);
});


test('Test_FindTimelineAnchorSlot_TestMidSlot_ExpectPreceding', () => {
   const startMinutes = 75;
   const slotStarts = [0, 30, 60, 90];

   const anchor = DayPlannerTimelineRenderer.findTimelineAnchorSlot(startMinutes, slotStarts);

   assert.equal(anchor, slotStarts.at(Position.THIRD));
});


test('Test_FindTimelineAnchorSlot_TestEmptySlots_ExpectNull', () => {
   const startMinutes = 10;
   const slotStarts = [];

   const anchor = DayPlannerTimelineRenderer.findTimelineAnchorSlot(startMinutes, slotStarts);

   assert.equal(anchor, null);
});


test('Test_FindTimelineAnchorSlot_TestNaN_ExpectNull', () => {
   const startMinutes = Number.NaN;
   const slotStarts = [0, 30];

   const anchor = DayPlannerTimelineRenderer.findTimelineAnchorSlot(startMinutes, slotStarts);

   assert.equal(anchor, null);
});


test('Test_FindTimelineSlotEndMinutes_TestAnchor_ExpectNext', () => {
   const anchorSlot = 30;
   const slotStarts = [0, 30, 60];
   const fallbackEndMinutes = 99;

   const endMinutes = DayPlannerTimelineRenderer.findTimelineSlotEndMinutes(
      anchorSlot,
      slotStarts,
      fallbackEndMinutes
   );

   assert.equal(endMinutes, slotStarts.at(Position.THIRD));
});


test('Test_FindTimelineSlotEndMinutes_TestLastSlot_ExpectFallback', () => {
   const slotStarts = [0, 30, 60];
   const anchorSlot = slotStarts.at(Position.LAST);
   const fallbackEndMinutes = 99;

   const endMinutes = DayPlannerTimelineRenderer.findTimelineSlotEndMinutes(
      anchorSlot,
      slotStarts,
      fallbackEndMinutes
   );

   assert.equal(endMinutes, fallbackEndMinutes);
});


test('Test_ComputeMarkerOffsetFraction_TestAtAnchor_ExpectZero', () => {
   const startMinutes = 30;
   const anchorSlot = 30;
   const slotEndMinutes = 60;

   const fraction = DayPlannerTimelineRenderer.computeMarkerOffsetFraction(
      startMinutes,
      anchorSlot,
      slotEndMinutes
   );

   assert.equal(fraction, 0);
});


test('Test_ComputeMarkerOffsetFraction_TestMidSpan_ExpectHalf', () => {
   const startMinutes = 45;
   const anchorSlot = 30;
   const slotEndMinutes = 60;

   const fraction = DayPlannerTimelineRenderer.computeMarkerOffsetFraction(
      startMinutes,
      anchorSlot,
      slotEndMinutes
   );

   assert.equal(fraction, (startMinutes - anchorSlot) / (slotEndMinutes - anchorSlot));
});


test('Test_ComputeMarkerOffsetFraction_TestZeroSpan_ExpectZero', () => {
   const startMinutes = 45;
   const anchorSlot = 30;
   const slotEndMinutes = 30;

   const fraction = DayPlannerTimelineRenderer.computeMarkerOffsetFraction(
      startMinutes,
      anchorSlot,
      slotEndMinutes
   );

   assert.equal(fraction, 0);
});


test('Test_BuildMarkersByAnchorSlot_TestMarkers_ExpectGroupedOffsets', () => {
   const arriveMinutes = 45;
   const departMinutes = 90;
   const slotStarts = [0, 30, 60];
   const closeMinutes = 120;
   const arriveLabel = 'Arrive';
   const departLabel = 'Depart';
   const arrivalKind = 'arrival';
   const departureKind = 'departure';

   const markersMap = DayPlannerTimelineRenderer.buildMarkersByAnchorSlot(
      [
         { startMinutes: arriveMinutes, label: arriveLabel, kind: arrivalKind },
         { startMinutes: departMinutes, label: departLabel, kind: departureKind },
      ],
      slotStarts,
      closeMinutes
   );

   const arriveAnchor = DayPlannerTimelineRenderer.findTimelineAnchorSlot(arriveMinutes, slotStarts);
   const departAnchor = DayPlannerTimelineRenderer.findTimelineAnchorSlot(departMinutes, slotStarts);
   assert.deepEqual(markersMap.get(arriveAnchor), [
      {
         label: arriveLabel,
         offsetFraction: DayPlannerTimelineRenderer.computeMarkerOffsetFraction(
            arriveMinutes,
            arriveAnchor,
            DayPlannerTimelineRenderer.findTimelineSlotEndMinutes(arriveAnchor, slotStarts, closeMinutes)
         ),
         kind: arrivalKind,
      },
   ]);
   assert.deepEqual(markersMap.get(departAnchor), [
      {
         label: departLabel,
         offsetFraction: DayPlannerTimelineRenderer.computeMarkerOffsetFraction(
            departMinutes,
            departAnchor,
            DayPlannerTimelineRenderer.findTimelineSlotEndMinutes(departAnchor, slotStarts, closeMinutes)
         ),
         kind: departureKind,
      },
   ]);
});


test('Test_BuildMarkersByAnchorSlot_TestNoAnchorSlot_ExpectUnchangedMap', () => {
   const markersMap = DayPlannerTimelineRenderer.buildMarkersByAnchorSlot(
      [{ startMinutes: 45, label: 'Arrive', kind: 'arrival' }],
      [],
      120
   );

   assert.equal(markersMap.size, 0);
});


test('Test_ResolveTimelinePillLabel_TestEarlyAdmission_ExpectEarly', () => {
   const hours = {
      earlyAdmissionMinutes: 8 * 60,
      openMinutes: 9 * 60,
      lastAdmissionMinutes: 16 * 60,
      closeMinutes: 17 * 60,
   };
   const strings = {
      earlyAdmissionLabel: 'Early',
      openLabel: 'Open',
      lastAdmissionLabel: 'Last',
      closeLabel: 'Close',
   };

   const label = DayPlannerTimelineRenderer.resolveTimelinePillLabel(
      hours.earlyAdmissionMinutes,
      hours,
      strings
   );

   assert.equal(label, strings.earlyAdmissionLabel);
});


test('Test_ResolveTimelinePillLabel_TestOpen_ExpectOpen', () => {
   const hours = {
      earlyAdmissionMinutes: 8 * 60,
      openMinutes: 9 * 60,
      lastAdmissionMinutes: 16 * 60,
      closeMinutes: 17 * 60,
   };
   const strings = {
      earlyAdmissionLabel: 'Early',
      openLabel: 'Open',
      lastAdmissionLabel: 'Last',
      closeLabel: 'Close',
   };

   const label = DayPlannerTimelineRenderer.resolveTimelinePillLabel(hours.openMinutes, hours, strings);

   assert.equal(label, strings.openLabel);
});


test('Test_ResolveTimelinePillLabel_TestLastAdmission_ExpectLast', () => {
   const hours = {
      earlyAdmissionMinutes: 8 * 60,
      openMinutes: 9 * 60,
      lastAdmissionMinutes: 16 * 60,
      closeMinutes: 17 * 60,
   };
   const strings = {
      earlyAdmissionLabel: 'Early',
      openLabel: 'Open',
      lastAdmissionLabel: 'Last',
      closeLabel: 'Close',
   };

   const label = DayPlannerTimelineRenderer.resolveTimelinePillLabel(
      hours.lastAdmissionMinutes,
      hours,
      strings
   );

   assert.equal(label, strings.lastAdmissionLabel);
});


test('Test_ResolveTimelinePillLabel_TestClose_ExpectClose', () => {
   const hours = {
      earlyAdmissionMinutes: 8 * 60,
      openMinutes: 9 * 60,
      lastAdmissionMinutes: 16 * 60,
      closeMinutes: 17 * 60,
   };
   const strings = {
      earlyAdmissionLabel: 'Early',
      openLabel: 'Open',
      lastAdmissionLabel: 'Last',
      closeLabel: 'Close',
   };

   const label = DayPlannerTimelineRenderer.resolveTimelinePillLabel(hours.closeMinutes, hours, strings);

   assert.equal(label, strings.closeLabel);
});


test('Test_ResolveTimelinePillLabel_TestInterior_ExpectNull', () => {
   const hours = {
      earlyAdmissionMinutes: 8 * 60,
      openMinutes: 9 * 60,
      lastAdmissionMinutes: 16 * 60,
      closeMinutes: 17 * 60,
   };
   const strings = {
      earlyAdmissionLabel: 'Early',
      openLabel: 'Open',
      lastAdmissionLabel: 'Last',
      closeLabel: 'Close',
   };

   const label = DayPlannerTimelineRenderer.resolveTimelinePillLabel(10 * 60, hours, strings);

   assert.equal(label, null);
});
