import assert from 'node:assert/strict';
import { test } from 'node:test';

import { isScheduleItemTransportationRow } from '../../scripts/itinerary/selectors/transportationSelector/model.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';

test('isScheduleItemTransportationRow recognizes transportations and added-as-attraction rows', () => {
   assert.equal(
      isScheduleItemTransportationRow({
         scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType,
      }),
      true
   );
   assert.equal(
      isScheduleItemTransportationRow({
         is_also_transportation: true,
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      }),
      false
   );
   assert.equal(
      isScheduleItemTransportationRow({
         added_as_attraction: true,
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      }),
      true
   );
   assert.equal(
      isScheduleItemTransportationRow({
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      }),
      false
   );
});
