import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerTimelinePillAppender } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillAppender.js';
import { OpenTimelineView } from '../../../../../scripts/itinerary/panel/components/openTimelineView.js';
import { ScheduledTimelineView } from '../../../../../scripts/itinerary/panel/components/scheduledTimelineView.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { ZooClockTimeHelper } from '../../../../../scripts/shared/zooClockTimeHelper.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _makeTimelineGridLine() {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(gridLine);

   return { gridLine };
}

installDomTestHooks();


test('Test_AppendTimelinePill_TestOpenPill_ExpectPointStrip', () => {
   const { gridLine } = _makeTimelineGridLine();
   const label = 'Tundra Grill';

   DayPlannerTimelinePillAppender.appendTimelinePill(gridLine, label, 0);
   const strip = gridLine.querySelector('.itinerary-day-pill-strip');
   const pill = strip?.querySelector('.itinerary-day-open-pill');

   assert.ok(strip);
   assert.equal(pill?.querySelector('.itinerary-day-open-pill-label')?.textContent, label);
   assert.equal(strip?.getAttribute('data-scheduled-column'), null);
});


test('Test_AppendTimelinePill_TestBoundaryPlacement_ExpectMarker', () => {
   const { gridLine } = _makeTimelineGridLine();
   const label = 'Arrival';
   const visitBoundaryPlacement = 'ends-at-anchor';

   DayPlannerTimelinePillAppender.appendTimelinePill(gridLine, label, 0, {
      visitBoundaryPlacement,
      onRemove: () => {},
      menuAriaLabel: 'Arrival options',
      removeLabel: 'Clear arrival',
   });
   const marker = gridLine.querySelector('.itinerary-day-boundary-marker');

   assert.ok(marker);
   assert.equal(marker?.getAttribute('data-boundary-marker-kind'), 'arrival');
   assert.equal(
      gridLine.querySelector('.itinerary-day-pill-strip')?.getAttribute('data-visit-boundary-placement'),
      visitBoundaryPlacement
   );
});


test('Test_AppendScheduledDurationPill_TestDuration_ExpectStripAndPill', () => {
   const { gridLine } = _makeTimelineGridLine();
   const startTime = '12:00';
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const endMinutes = ZooClockTimeHelper.parseMinutes(startTime) + durationMinutes;
   const hours = Math.floor(endMinutes / 60);
   const minutes = endMinutes % 60;
   const endTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;

   DayPlannerTimelinePillAppender.appendScheduledDurationPill(gridLine, {
      label: 'African Lion',
      durationMinutes,
      startTime,
      endTime,
   });
   const strip = gridLine.querySelector('.itinerary-day-pill-strip');
   const pill = strip?.querySelector('.itinerary-day-scheduled-pill');

   assert.equal(strip?.getAttribute('data-scheduled-column'), 'true');
   assert.ok(pill);
});


test('Test_AppendItineraryTimeMarkers_TestArrivalSlot_ExpectAppended', () => {
   const { gridLine } = _makeTimelineGridLine();
   const label = 'Arrival';
   const kind = 'arrival';
   const anchorSlotMinutes = ZooClockTimeHelper.parseMinutes('12:00');
   const markersByAnchorSlot = new Map([
      [anchorSlotMinutes, [{
         label,
         kind,
         offsetFraction: 0,
      }]],
   ]);

   DayPlannerTimelinePillAppender.appendItineraryTimeMarkers(
      gridLine,
      markersByAnchorSlot,
      anchorSlotMinutes,
      {},
      { remove: 'Remove' },
      {
         arrival: kind,
         departure: 'departure',
      }
   );
   const marker = gridLine.querySelector('.itinerary-day-boundary-marker');

   assert.equal(marker?.getAttribute('aria-label'), label);
   assert.equal(marker?.getAttribute('data-boundary-marker-kind'), kind);
});


test('Test_AppendTimelinePill_TestMissingLabel_ExpectNoOp', () => {
   const { gridLine } = _makeTimelineGridLine();

   DayPlannerTimelinePillAppender.appendTimelinePill(gridLine, '', 0);

   assert.equal(gridLine.querySelector('.itinerary-day-pill-strip'), null);
});


test('Test_AppendTimelinePill_TestMissingOpenPill_ExpectNoOp', () => {
   const { gridLine } = _makeTimelineGridLine();
   const originalOpenPill = OpenTimelineView.makeOpenPill;

   OpenTimelineView.makeOpenPill = () => null;

   try {
      DayPlannerTimelinePillAppender.appendTimelinePill(gridLine, 'Tundra Grill', 0);

      assert.equal(gridLine.querySelector('.itinerary-day-pill-strip'), null);
   } finally {
      OpenTimelineView.makeOpenPill = originalOpenPill;
   }
});


test('Test_AppendScheduledDurationPill_TestMissingPill_ExpectNoOp', () => {
   const { gridLine } = _makeTimelineGridLine();
   const originalScheduledPill = ScheduledTimelineView.makeScheduledPill;
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

   ScheduledTimelineView.makeScheduledPill = () => null;

   try {
      DayPlannerTimelinePillAppender.appendScheduledDurationPill(gridLine, {
         label: 'African Lion',
         durationMinutes,
      });

      assert.equal(gridLine.querySelector('.itinerary-day-pill-strip'), null);
   } finally {
      ScheduledTimelineView.makeScheduledPill = originalScheduledPill;
   }
});
