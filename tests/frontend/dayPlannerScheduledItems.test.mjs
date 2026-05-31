import assert from 'node:assert/strict';
import { test } from 'node:test';

import { buildScheduledItemRowsContext } from '../../scripts/itinerary/panel/dayPlannerScheduledItems.js';
import { resolveScheduledPillOptions } from '../../scripts/itinerary/panel/components/dayPlannerTimelinePills.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';

test('buildScheduledItemRowsContext places generic events on the timeline', () => {
   const context = buildScheduledItemRowsContext(
      {
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         events: [
            {
               event_type: 'lunch',
               start_time: '12:00 PM',
               end_time: '12:40 PM',
            },
         ],
      },
      [720, 750],
      1140
   );
   const lunchItems = [...context.itemsByStart.values()].flat();

   assert.equal(lunchItems.length, 1);
   assert.equal(lunchItems[0].label, 'Lunch');
   assert.equal(lunchItems[0].scheduleItemKind, ScheduleItemKind.EVENT.kind);
   assert.equal(lunchItems[0].scheduleItemEventType, 'lunch');
   assert.equal(lunchItems[0].maximumDuration, 40);
});

test('resolveScheduledPillOptions unschedules generic events by event type', () => {
   const requests = [];

   const options = resolveScheduledPillOptions(
      {
         scheduleItemKind: ScheduleItemKind.EVENT.kind,
         scheduleItemEventType: 'lunch',
         scheduleItemKey: '',
      },
      {
         onUnscheduleItineraryItem: (request) => {
            requests.push(request);
         },
      },
      { scheduledItemMenuAria: 'Menu', unschedule: 'Unschedule' }
   );

   options.onUnschedule?.();

   assert.deepEqual(requests, [{
      itemType: 'lunch',
      key: '',
   }]);
});
