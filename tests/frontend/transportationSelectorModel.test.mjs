import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   buildAddAsTransportationMessage,
   isScheduleItemTransportationRow,
   makeTransportationSelection,
   migrateStoredTransportations,
   shouldConfirmAddAsTransportation,
} from '../../scripts/itinerary/selectors/transportationSelector/model.js';
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

test('makeTransportationSelection stores pure transportation selections', () => {
   assert.deepEqual(
      makeTransportationSelection({
         name: 'Zoomobile',
         info_link: 'https://example.com/zoomobile',
         free_with_admission: false,
         open_time: '10:00 AM',
         close_time: '4:00 PM',
         legs: [
            {
               from_station: 'Main Zoomobile Station',
               to_station: 'Canadian Domain Zoomobile Station',
            },
         ],
      }),
      {
         id: 'Zoomobile',
         name: 'Zoomobile',
         subtitle: 'Main Zoomobile Station - Canadian Domain Zoomobile Station',
         infoLink: 'https://example.com/zoomobile',
         imageSrc: '../images/details/transportations/zoomobile.png',
         addedAsAttraction: false,
      }
   );
});

test('makeTransportationSelection falls back to cost and hours subtitle', () => {
   assert.deepEqual(
      makeTransportationSelection({
         name: 'Zoomobile',
         free_with_admission: false,
         open_time: '10:00 AM',
         close_time: '4:00 PM',
      }),
      {
         id: 'Zoomobile',
         name: 'Zoomobile',
         subtitle: 'Extra Charge  •  10:00 AM - 4:00 PM',
         infoLink: null,
         imageSrc: '../images/details/transportations/zoomobile.png',
         addedAsAttraction: false,
      }
   );
});

test('shouldConfirmAddAsTransportation only prompts when adding also-attraction rows', () => {
   const zoomobileRow = { is_also_attraction: true };
   const pureTransportationRow = { is_also_attraction: false };

   assert.equal(
      shouldConfirmAddAsTransportation({
         row: zoomobileRow,
         isSelected: false,
      }),
      true
   );
   assert.equal(
      shouldConfirmAddAsTransportation({
         row: zoomobileRow,
         isSelected: true,
      }),
      false
   );
   assert.equal(
      shouldConfirmAddAsTransportation({
         row: pureTransportationRow,
         isSelected: false,
      }),
      false
   );
});

test('buildAddAsTransportationMessage explains bulk scheduling use', () => {
   assert.equal(
      buildAddAsTransportationMessage({ name: 'Zoomobile' }),
      'The Zoomobile will be used to reduce walking distance when bulk scheduling. This action will add the Zoomobile as a transportation method.'
   );
});

test('migrateStoredTransportations normalizes string and object selections', () => {
   assert.deepEqual(
      migrateStoredTransportations([
         'Zoomobile',
         {
            id: 'Zoomobile',
            name: 'Zoomobile',
            subtitle: 'Main Zoomobile Station',
            added_as_attraction: false,
         },
         { name: '' },
      ]),
      [
         {
            id: 'Zoomobile',
            name: 'Zoomobile',
            subtitle: '',
            infoLink: null,
            imageSrc: null,
            addedAsAttraction: false,
         },
         {
            id: 'Zoomobile',
            name: 'Zoomobile',
            subtitle: 'Main Zoomobile Station',
            infoLink: null,
            imageSrc: null,
            addedAsAttraction: false,
         },
      ]
   );
});
