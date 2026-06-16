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
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Meet The Guardians/);
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Wild Encounters/);
   });
});
