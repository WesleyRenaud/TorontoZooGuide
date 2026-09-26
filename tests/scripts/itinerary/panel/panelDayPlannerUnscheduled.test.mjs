import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerBuilder } from '../../../../scripts/itinerary/panel/components/dayPlannerBuilder.js';
import { TransportationScheduleItemKey } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../scripts/strings.js';
import {
   EMPTY_ITINERARY,
   allTextFor,
   createNode,
   installPanelRowsTestHooks,
} from '../../helpers/panelRowsTestSetup.mjs';

installPanelRowsTestHooks();

const transportationName = 'Zoomobile';
const zooHours = {
   date: '2026-06-20',
   openTime: '09:30',
   lastAdmissionTime: '18:00',
   closeTime: '19:00',
};


test('Test_MakeDayPlannerPreview_TestGuardiansTalksOmittedFromUnscheduled_ExpectScheduledOnly', () => {
   const talkName = 'Amur Tiger';

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
      zooHours,
      {
         ...EMPTY_ITINERARY,
         guardiansTalks: [
            {
               name: talkName,
               location: 'Eurasia Wilds',
               start_time: '1:30 PM',
               end_time: '2:00 PM',
               maximum_duration: 30,
            },
         ],
      }
   );
   const text = allTextFor(planner);

   assert.match(text, new RegExp(Strings.itinerary.dayPlanner.scheduledTitle));
   assert.match(text, new RegExp(`${Strings.site.nav.meetTheGuardians} \\(1\\)`));
   assert.match(text, new RegExp(Strings.itinerary.dayPlanner.unscheduledTitle));
   assert.match(text, new RegExp(`${Strings.site.nav.animals} \\(0\\)`));
   assert.match(text, new RegExp(`${Strings.map.filter.attractions} \\(0\\)`));
   assert.match(text, new RegExp(`${Strings.entityLabels.transportation} \\(0\\)`));
   assert.doesNotMatch(
      text,
      new RegExp(`${Strings.itinerary.dayPlanner.unscheduledTitle}[\\s\\S]*${Strings.site.nav.meetTheGuardians}`)
   );
   assert.doesNotMatch(
      text,
      new RegExp(`${Strings.itinerary.dayPlanner.unscheduledTitle}[\\s\\S]*${Strings.site.nav.wildEncounters}`)
   );
});


test('Test_MakeDayPlannerPreview_TestUnscheduledTransportation_ExpectRemoveOnly', () => {
   const scheduleCalls = [];
   const removeCalls = [];
   const addedAsAttraction = false;
   const transportationKey = new TransportationScheduleItemKey(transportationName, addedAsAttraction).toWire();

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
      zooHours,
      {
         ...EMPTY_ITINERARY,
         transportations: [
            {
               name: transportationName,
               added_as_attraction: addedAsAttraction,
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
      section.querySelector('.itinerary-day-items-title')?.textContent?.includes(
         Strings.itinerary.dayPlanner.unscheduledTitle
      )
   ));
   const zoomobileRow = [...(unscheduledList?.querySelectorAll('.itin-panel-item') ?? [])].find((row) => (
      allTextFor(row).includes(transportationName)
   ));
   const zoomobileButtons = [...(zoomobileRow?.querySelectorAll('.itin-panel-item-action-btn') ?? [])];

   assert.match(text, new RegExp(Strings.itinerary.dayPlanner.unscheduledTitle));
   assert.match(text, new RegExp(`${Strings.entityLabels.transportation} \\(1\\)`));
   assert.deepEqual(
      zoomobileButtons.map((button) => button.textContent),
      [Strings.itinerary.dayPlanner.remove]
   );

   zoomobileButtons.at(Position.FIRST)?.click();

   assert.equal(scheduleCalls.length, 0);
   assert.deepEqual(removeCalls, [{
      itemType: ScheduleItemKind.TRANSPORTATION.itemType,
      key: transportationKey,
   }]);
});


test('Test_MakeDayPlannerPreview_TestBulkEvaluatedTransitWithoutLegs_ExpectScheduledRemove', () => {
   const removeCalls = [];
   const addedAsAttraction = false;
   const transportationKey = new TransportationScheduleItemKey(transportationName, addedAsAttraction).toWire();

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
      zooHours,
      {
         ...EMPTY_ITINERARY,
         transportations: [
            {
               name: transportationName,
               added_as_attraction: addedAsAttraction,
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
      section.querySelector('.itinerary-day-items-title')?.textContent?.includes(
         Strings.itinerary.dayPlanner.scheduledTitle
      )
   ));
   const zoomobileRow = [...(scheduledList?.querySelectorAll('.itin-panel-item') ?? [])].find((row) => (
      allTextFor(row).includes(transportationName)
   ));
   const zoomobileButtons = [...(zoomobileRow?.querySelectorAll('.itin-panel-item-action-btn') ?? [])];
   const zoomobileMeta = allTextFor(
      zoomobileRow?.querySelector('.itin-panel-meta') ?? createNode('div')
   );

   assert.match(text, new RegExp(Strings.itinerary.dayPlanner.scheduledTitle));
   assert.match(text, new RegExp(`${Strings.entityLabels.transportation} \\(1\\)`));
   assert.doesNotMatch(
      text,
      new RegExp(`${Strings.itinerary.dayPlanner.unscheduledTitle}[\\s\\S]*${Strings.entityLabels.transportation} \\(1\\)`)
   );
   assert.doesNotMatch(
      text,
      new RegExp(`${Strings.itinerary.dayPlanner.unscheduledTitle}[\\s\\S]*${transportationName}`)
   );
   assert.equal(zoomobileMeta, '');
   assert.deepEqual(
      zoomobileButtons.map((button) => button.textContent),
      [Strings.itinerary.dayPlanner.remove]
   );

   zoomobileButtons.at(Position.FIRST)?.click();

   assert.deepEqual(removeCalls, [{
      itemType: ScheduleItemKind.TRANSPORTATION.itemType,
      key: transportationKey,
   }]);
});


test('Test_MakeDayPlannerPreview_TestBulkEvaluatedTransitWithLegs_ExpectStationsAndTime', () => {
   const addedAsAttraction = false;
   const firstStation = 'Main Station';
   const lastStation = 'Wildlife Health';
   const startTime = '2:30 PM';
   const endTime = '3:00 PM';

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
      zooHours,
      {
         ...EMPTY_ITINERARY,
         transportations: [
            {
               name: transportationName,
               added_as_attraction: addedAsAttraction,
               bulk_transit_evaluated: true,
               start_time: startTime,
               end_time: endTime,
               legs: [
                  {
                     from_station: firstStation,
                     to_station: 'Canadian Domain',
                     start_time: startTime,
                     end_time: '2:40 PM',
                  },
                  {
                     from_station: 'Canadian Domain',
                     to_station: lastStation,
                     start_time: '2:40 PM',
                     end_time: endTime,
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
      section.querySelector('.itinerary-day-items-title')?.textContent?.includes(
         Strings.itinerary.dayPlanner.scheduledTitle
      )
   ));
   const zoomobileRow = [...(scheduledList?.querySelectorAll('.itin-panel-item') ?? [])].find((row) => (
      allTextFor(row).includes(transportationName)
   ));
   const rowText = allTextFor(zoomobileRow);
   const buttons = [...(zoomobileRow?.querySelectorAll('.itin-panel-item-action-btn') ?? [])]
      .map((button) => button.textContent);

   assert.match(text, new RegExp(`${Strings.itinerary.dayPlanner.scheduledTitle}[\\s\\S]*${Strings.entityLabels.transportation} \\(1\\)`));
   assert.match(rowText, new RegExp(Strings.labels.transportationStations(firstStation, lastStation)));
   assert.match(rowText, new RegExp(`Time: ~${startTime}`));
   assert.deepEqual(buttons, [Strings.itinerary.dayPlanner.remove]);
   assert.doesNotMatch(
      text,
      new RegExp(`${Strings.itinerary.dayPlanner.unscheduledTitle}[\\s\\S]*${transportationName}`)
   );
});


test('Test_MakeDayPlannerPreview_TestScheduledTransportationSequences_ExpectSplitRows', () => {
   const firstSequenceStart = '9:00 AM';
   const firstFrom = 'Main Zoomobile Station';
   const firstTo = 'Africa Zoomobile Station';
   const secondFrom = 'Canadian Domain Zoomobile Station';
   const secondTo = 'Main Zoomobile Station';

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
      zooHours,
      {
         ...EMPTY_ITINERARY,
         transportations: [
            {
               name: transportationName,
               added_as_attraction: false,
               bulk_transit_evaluated: true,
               start_time: firstSequenceStart,
               end_time: '11:19 AM',
               legs: [
                  {
                     from_station: firstFrom,
                     to_station: 'Canadian Domain Zoomobile Station',
                     start_time: firstSequenceStart,
                     end_time: '9:20 AM',
                  },
                  {
                     from_station: 'Canadian Domain Zoomobile Station',
                     to_station: firstTo,
                     start_time: '9:20 AM',
                     end_time: '9:30 AM',
                  },
                  {
                     from_station: secondFrom,
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
                     to_station: secondTo,
                     start_time: '11:04 AM',
                     end_time: '11:19 AM',
                  },
               ],
            },
         ],
      }
   );
   const scheduledList = [...planner.querySelectorAll('.itinerary-day-items-sections')].find((section) => (
      section.querySelector('.itinerary-day-items-title')?.textContent?.includes(
         Strings.itinerary.dayPlanner.scheduledTitle
      )
   ));
   const zoomobileRows = [...(scheduledList?.querySelectorAll('.itin-panel-item') ?? [])].filter((row) => (
      allTextFor(row).includes(transportationName)
   ));
   const firstRowText = allTextFor(zoomobileRows.at(Position.FIRST));
   const secondRowText = allTextFor(zoomobileRows.at(Position.SECOND));

   assert.match(allTextFor(scheduledList), new RegExp(`${Strings.entityLabels.transportation} \\(2\\)`));
   assert.equal(zoomobileRows.length, Position.THIRD);
   assert.match(firstRowText, new RegExp(Strings.labels.transportationStations(firstFrom, firstTo)));
   assert.match(secondRowText, new RegExp(Strings.labels.transportationStations(secondFrom, secondTo)));
   assert.match(firstRowText, new RegExp(`Time: ~${firstSequenceStart}`));
   assert.match(secondRowText, /Time: ~10:25 AM/);
});
