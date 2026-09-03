import assert from 'node:assert/strict';
import { test } from 'node:test';

import { appendScheduledItems } from '../../scripts/itinerary/panel/components/dayPlannerTimeline.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

function makeTimelineGridLine() {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(gridLine);

   return { gridLine };
}

function makeEventCardRow(className = 'itin-panel-item') {
   return createDomNode('div', className);
}

test.describe('dayPlannerTimeline event card region colours', () => {
   installDomTestHooks();

   test('colors talk event cards from location exhibit', () => {
      const { gridLine } = makeTimelineGridLine();
      const row = makeEventCardRow();

      appendScheduledItems(gridLine, [{
         items: [{
            row,
            maximumDuration: 30,
            offsetFraction: 0,
            scheduleItemKind: ScheduleItemKind.GUARDIANS_TALK.itemType,
            item: {
               name: 'Komodo Dragon',
               location: 'Australasia Pavilion',
            },
         }],
      }]);

      const card = gridLine.querySelector('.itinerary-day-event-card');

      assert.ok(card);
      assert.ok(card.classList.contains('itinerary-day-scheduled-pill--region-colored'));
      assert.ok(card.classList.contains('itinerary-day-scheduled-pill--region-australasia'));
      assert.equal(card.getAttribute('data-region-slug'), 'australasia');
   });

   test('colors attraction event cards from region', () => {
      const { gridLine } = makeTimelineGridLine();
      const row = makeEventCardRow();

      appendScheduledItems(gridLine, [{
         items: [{
            row,
            maximumDuration: 15,
            offsetFraction: 0,
            scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
            item: {
               name: 'Zoomobile',
               region: 'Front Courtyard',
            },
         }],
      }]);

      const card = gridLine.querySelector('.itinerary-day-event-card');

      assert.ok(card);
      assert.ok(card.classList.contains('itinerary-day-scheduled-pill--region-front-courtyard'));
      assert.equal(card.getAttribute('data-region-slug'), 'front-courtyard');
   });

   test('colors wild encounter event cards from region', () => {
      const { gridLine } = makeTimelineGridLine();
      const row = makeEventCardRow();

      appendScheduledItems(gridLine, [{
         items: [{
            row,
            maximumDuration: 30,
            offsetFraction: 0,
            scheduleItemKind: ScheduleItemKind.WILD_ENCOUNTER.itemType,
            item: {
               name: 'Capybara',
               meeting_spot: 'Wild Encounter - Mayan Temple Meeting Spot',
               region: 'Americas',
            },
         }],
      }]);

      const card = gridLine.querySelector('.itinerary-day-event-card');

      assert.ok(card);
      assert.ok(card.classList.contains('itinerary-day-scheduled-pill--region-americas'));
      assert.equal(card.getAttribute('data-region-slug'), 'americas');
   });
});
