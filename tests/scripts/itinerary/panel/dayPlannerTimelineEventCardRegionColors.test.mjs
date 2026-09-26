import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerTimelineView } from '../../../../scripts/itinerary/panel/components/dayPlannerTimelineView.js';
import { RegionColors } from '../../../../scripts/shared/regionColors.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

function _makeTimelineGridLine() {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(gridLine);

   return { gridLine };
}

function _makeEventCardRow(className = 'itin-panel-item') {
   return createDomNode('div', className);
}

installDomTestHooks();


test('Test_AppendScheduledItems_TestTalkLocation_ExpectAustralasiaColor', () => {
   const { gridLine } = _makeTimelineGridLine();
   const row = _makeEventCardRow();
   const item = {
      name: 'Komodo Dragon',
      location: 'Australasia Pavilion',
   };

   DayPlannerTimelineView.appendScheduledItems(gridLine, [{
      items: [{
         row,
         maximumDuration: 30,
         offsetFraction: 0,
         scheduleItemKind: ScheduleItemKind.GUARDIANS_TALK.itemType,
         item,
      }],
   }]);

   const card = gridLine.querySelector('.itinerary-day-event-card');
   const slug = RegionColors.resolveRegionColorSlugForScheduledItem(item);

   assert.ok(card);
   assert.ok(card.classList.contains('itinerary-day-scheduled-pill--region-colored'));
   assert.ok(card.classList.contains(`itinerary-day-scheduled-pill--region-${slug}`));
   assert.equal(card.getAttribute('data-region-slug'), slug);
});


test('Test_AppendScheduledItems_TestAttractionRegion_ExpectFrontCourtyardColor', () => {
   const { gridLine } = _makeTimelineGridLine();
   const row = _makeEventCardRow();
   const item = {
      name: 'Zoomobile',
      region: 'Front Courtyard',
   };

   DayPlannerTimelineView.appendScheduledItems(gridLine, [{
      items: [{
         row,
         maximumDuration: 15,
         offsetFraction: 0,
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
         item,
      }],
   }]);

   const card = gridLine.querySelector('.itinerary-day-event-card');
   const slug = RegionColors.resolveRegionColorSlugForScheduledItem(item);

   assert.ok(card);
   assert.ok(card.classList.contains(`itinerary-day-scheduled-pill--region-${slug}`));
   assert.equal(card.getAttribute('data-region-slug'), slug);
});


test('Test_AppendScheduledItems_TestWildEncounterRegion_ExpectAmericasColor', () => {
   const { gridLine } = _makeTimelineGridLine();
   const row = _makeEventCardRow();
   const item = {
      name: 'Capybara',
      meeting_spot: 'Wild Encounter - Mayan Temple Meeting Spot',
      region: 'Americas',
   };

   DayPlannerTimelineView.appendScheduledItems(gridLine, [{
      items: [{
         row,
         maximumDuration: 30,
         offsetFraction: 0,
         scheduleItemKind: ScheduleItemKind.WILD_ENCOUNTER.itemType,
         item,
      }],
   }]);

   const card = gridLine.querySelector('.itinerary-day-event-card');
   const slug = RegionColors.resolveRegionColorSlugForScheduledItem(item);

   assert.ok(card);
   assert.ok(card.classList.contains(`itinerary-day-scheduled-pill--region-${slug}`));
   assert.equal(card.getAttribute('data-region-slug'), slug);
});
