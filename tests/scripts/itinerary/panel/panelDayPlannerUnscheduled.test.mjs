import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlanner } from '../../../../scripts/itinerary/panel/components/dayPlanner.js';
import { SectionConfigs } from '../../../../scripts/itinerary/panel/sectionConfigs.js';
import { Rows } from '../../../../scripts/itinerary/panel/rows.js';
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
} from '../../helpers/panelRowsTestSetup.mjs';


test.describe('itinerary day planner preview unscheduled', () => {
   installPanelRowsTestHooks();

   test('Test_Day_TestDayPlannerOmitsGuardiansTalksAndWildEncounters_ExpectOk', () => {
      const planner = DayPlanner.makeDayPlannerPreview(
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

   test('Test_Day_TestDayPlannerShowsUnscheduledTransportationWithoutASchedule_ExpectOk', () => {
      const scheduleCalls = [];
      const removeCalls = [];
      const planner = DayPlanner.makeDayPlannerPreview(
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
         key: 'Zoomobile||0',
      }]);
   });

   test('Test_Day_TestDayPlannerRendersBulkEvaluatedTransitTransportationIn_ExpectOk', () => {
      const removeCalls = [];
      const planner = DayPlanner.makeDayPlannerPreview(
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
                  bulk_transit_evaluated: true,
                  legs: [],
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: () => {},
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const text = allTextFor(planner);
      const scheduledList = [...planner.querySelectorAll('.itinerary-day-items-sections')].find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Scheduled Items')
      ));
      const zoomobileRow = [...(scheduledList?.querySelectorAll('.itin-panel-item') ?? [])].find((row) => (
         allTextFor(row).includes('Zoomobile')
      ));
      const zoomobileButtons = [...(zoomobileRow?.querySelectorAll('.itin-panel-item-action-btn') ?? [])];
      const zoomobileMeta = allTextFor(
         zoomobileRow?.querySelector('.itin-panel-meta') ?? createNode('div')
      );

      assert.match(text, /Scheduled Items/);
      assert.match(text, /Transportation \(1\)/);
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Transportation \(1\)/);
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Zoomobile/);
      assert.equal(zoomobileMeta, '');
      assert.deepEqual(
         zoomobileButtons.map((button) => button.textContent),
         ['Remove']
      );

      zoomobileButtons[0]?.click();

      assert.deepEqual(removeCalls, [{
         itemType: 'transportations',
         key: 'Zoomobile||0',
      }]);
   });

   test('Test_Day_TestDayPlannerRendersBulkEvaluatedTransitTransportationWith_ExpectOk', () => {
      const planner = DayPlanner.makeDayPlannerPreview(
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
                  bulk_transit_evaluated: true,
                  start_time: '2:30 PM',
                  end_time: '3:00 PM',
                  legs: [
                     {
                        from_station: 'Main Station',
                        to_station: 'Canadian Domain',
                        start_time: '2:30 PM',
                        end_time: '2:40 PM',
                     },
                     {
                        from_station: 'Canadian Domain',
                        to_station: 'Wildlife Health',
                        start_time: '2:40 PM',
                        end_time: '3:00 PM',
                     },
                  ],
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: () => {
                  throw new Error('pure transportations should not expose unschedule');
               },
               onRemoveItineraryItem: () => {},
            },
         }
      );
      const text = allTextFor(planner);
      const scheduledList = [...planner.querySelectorAll('.itinerary-day-items-sections')].find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Scheduled Items')
      ));
      const zoomobileRow = [...(scheduledList?.querySelectorAll('.itin-panel-item') ?? [])].find((row) => (
         allTextFor(row).includes('Zoomobile')
      ));

      assert.match(text, /Scheduled Items[\s\S]*Transportation \(1\)/);
      assert.match(allTextFor(zoomobileRow), /Main Station → Wildlife Health/);
      assert.match(allTextFor(zoomobileRow), /Time: ~2:30 PM/);
      assert.deepEqual(
         [...(zoomobileRow?.querySelectorAll('.itin-panel-item-action-btn') ?? [])]
            .map((button) => button.textContent),
         ['Remove']
      );
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Zoomobile/);
   });

   test('Test_Day_TestDayPlannerRendersEachScheduledTransportationSequenceIn_ExpectOk', () => {
      const planner = DayPlanner.makeDayPlannerPreview(
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
                  bulk_transit_evaluated: true,
                  start_time: '9:00 AM',
                  end_time: '11:19 AM',
                  legs: [
                     {
                        from_station: 'Main Zoomobile Station',
                        to_station: 'Canadian Domain Zoomobile Station',
                        start_time: '9:00 AM',
                        end_time: '9:20 AM',
                     },
                     {
                        from_station: 'Canadian Domain Zoomobile Station',
                        to_station: 'Africa Zoomobile Station',
                        start_time: '9:20 AM',
                        end_time: '9:30 AM',
                     },
                     {
                        from_station: 'Canadian Domain Zoomobile Station',
                        to_station: 'Africa Zoomobile Station',
                        start_time: '10:24 AM',
                        end_time: '10:34 AM',
                     },
                     {
                        from_station: 'Africa Zoomobile Station',
                        to_station: 'Tundra Zoomobile Station',
                        start_time: '10:34 AM',
                        end_time: '10:49 AM',
                     },
                     {
                        from_station: 'Tundra Zoomobile Station',
                        to_station: 'Eurasia Zoomobile Station',
                        start_time: '10:49 AM',
                        end_time: '11:04 AM',
                     },
                     {
                        from_station: 'Eurasia Zoomobile Station',
                        to_station: 'Main Zoomobile Station',
                        start_time: '11:04 AM',
                        end_time: '11:19 AM',
                     },
                  ],
               },
            ],
         }
      );
      const scheduledList = [...planner.querySelectorAll('.itinerary-day-items-sections')].find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Scheduled Items')
      ));
      const zoomobileRows = [...(scheduledList?.querySelectorAll('.itin-panel-item') ?? [])].filter((row) => (
         allTextFor(row).includes('Zoomobile')
      ));

      assert.match(allTextFor(scheduledList), /Transportation \(2\)/);
      assert.equal(zoomobileRows.length, 2);
      assert.match(
         allTextFor(zoomobileRows[0]),
         /Main Zoomobile Station → Africa Zoomobile Station/
      );
      assert.match(
         allTextFor(zoomobileRows[1]),
         /Canadian Domain Zoomobile Station → Main Zoomobile Station/
      );
      assert.match(allTextFor(zoomobileRows[0]), /Time: ~9:00 AM/);
      assert.match(allTextFor(zoomobileRows[1]), /Time: ~10:25 AM/);
   });
});
