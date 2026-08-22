import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeDayPlannerPreview } from '../../scripts/itinerary/panel/components/dayPlanner.js';
import { buildSectionConfigs } from '../../scripts/itinerary/panel/sectionConfigs.js';
import {
   buildAnimalRows,
   buildAttractionRows,
} from '../../scripts/itinerary/panel/rows.js';
import {
   EMPTY_ITINERARY,
   TEST_ITINERARY_CONFIG,
   allTextFor,
   boundaryMarkerByLabel,
   boundaryMarkerStripByLabel,
   createNode,
   documentListeners,
   imageSrcFor,
   installPanelRowsTestHooks,
   textFor,
   timelinePillTexts,
   timelineScheduledPillTexts,
} from './helpers/panelRowsTestSetup.mjs';


test.describe('itinerary day planner preview unscheduled', () => {
   installPanelRowsTestHooks();

   test('day planner omits guardians talks and wild encounters from unscheduled items', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            guardiansTalks: [
               {
                  name: 'Amur Tiger',
                  location: 'Eurasia Wilds',
                  start_time: '1:30 PM',
                  end_time: '2:00 PM',
                  maximum_duration: 30,
               },
            ],
         }
      );
      const text = allTextFor(planner);
   
      assert.match(text, /Scheduled Items/);
      assert.match(text, /Meet The Guardians \(1\)/);
      assert.match(text, /Unscheduled Items/);
      assert.match(text, /Animals \(0\)/);
      assert.match(text, /Attractions \(0\)/);
      assert.match(text, /Transportation \(0\)/);
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Meet The Guardians/);
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Wild Encounters/);
   });

   test('day planner shows unscheduled transportation without a schedule button', () => {
      const scheduleCalls = [];
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            transportations: [
               {
                  name: 'Zoomobile',
                  added_as_attraction: false,
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onScheduleItineraryItem: (pick) => {
                  scheduleCalls.push(pick);
               },
               onUnscheduleItineraryItem: () => {},
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const text = allTextFor(planner);
      const unscheduledList = [...planner.querySelectorAll('.itinerary-day-items-sections')].find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Unscheduled Items')
      ));
      const zoomobileRow = [...(unscheduledList?.querySelectorAll('.itin-panel-item') ?? [])].find((row) => (
         allTextFor(row).includes('Zoomobile')
      ));
      const zoomobileButtons = [...(zoomobileRow?.querySelectorAll('.itin-panel-item-action-btn') ?? [])];

      assert.match(text, /Unscheduled Items/);
      assert.match(text, /Transportation \(1\)/);
      assert.deepEqual(
         zoomobileButtons.map((button) => button.textContent),
         ['Remove']
      );

      zoomobileButtons[0]?.click();
      assert.equal(scheduleCalls.length, 0);
      assert.deepEqual(removeCalls, [{
         itemType: 'transportations',
         key: 'Zoomobile',
      }]);
   });
});
