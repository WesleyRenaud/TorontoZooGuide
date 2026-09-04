import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerTimelinePillAppend } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillAppend.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function makeTimelineGridLine() {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(gridLine);

   return { gridLine };
}

test.describe('Test_DayPlannerTimelinePillAppend', () => {
   installDomTestHooks();

   test('Test_AppendTimelinePill_TestOpenPill_ExpectPointStrip', () => {
      const { gridLine } = makeTimelineGridLine();

      DayPlannerTimelinePillAppend.appendTimelinePill(gridLine, 'Lunch', 0);

      const strip = gridLine.querySelector('.itinerary-day-pill-strip');
      const pill = strip?.querySelector('.itinerary-day-open-pill');

      assert.ok(strip);
      assert.equal(
         pill?.querySelector('.itinerary-day-open-pill-label')?.textContent,
         'Lunch'
      );
      assert.equal(strip?.getAttribute('data-scheduled-column'), null);
   });

   test('Test_AppendTimelinePill_TestBoundaryPlacement_ExpectMarker', () => {
      const { gridLine } = makeTimelineGridLine();

      DayPlannerTimelinePillAppend.appendTimelinePill(gridLine, 'Arrival', 0, {
         visitBoundaryPlacement: 'ends-at-anchor',
         onRemove: () => {},
         menuAriaLabel: 'Arrival options',
         removeLabel: 'Clear arrival',
      });

      const marker = gridLine.querySelector('.itinerary-day-boundary-marker');

      assert.ok(marker);
      assert.equal(marker?.getAttribute('data-boundary-marker-kind'), 'arrival');
      assert.equal(
         gridLine.querySelector('.itinerary-day-pill-strip')?.getAttribute('data-visit-boundary-placement'),
         'ends-at-anchor'
      );
   });

   test('Test_AppendScheduledDurationPill_TestDuration_ExpectStripAndPill', () => {
      const { gridLine } = makeTimelineGridLine();

      DayPlannerTimelinePillAppend.appendScheduledDurationPill(gridLine, {
         label: 'African Lion',
         durationMinutes: 30,
         startTime: '12:00 PM',
         endTime: '12:30 PM',
      });

      const strip = gridLine.querySelector('.itinerary-day-pill-strip');
      const pill = strip?.querySelector('.itinerary-day-scheduled-pill');

      assert.equal(strip?.getAttribute('data-scheduled-column'), 'true');
      assert.ok(pill);
   });

   test('Test_AppendItineraryTimeMarkers_TestArrivalSlot_ExpectAppended', () => {
      const { gridLine } = makeTimelineGridLine();
      const markersByAnchorSlot = new Map([
         [720, [{
            label: 'Arrival',
            kind: 'arrival',
            offsetFraction: 0,
         }]],
      ]);

      DayPlannerTimelinePillAppend.appendItineraryTimeMarkers(
         gridLine,
         markersByAnchorSlot,
         720,
         {},
         { remove: 'Remove' },
         {
            arrival: 'arrival',
            departure: 'departure',
         }
      );

      const marker = gridLine.querySelector('.itinerary-day-boundary-marker');

      assert.equal(marker?.getAttribute('aria-label'), 'Arrival');
      assert.equal(marker?.getAttribute('data-boundary-marker-kind'), 'arrival');
   });
});
