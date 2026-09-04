import assert from 'node:assert/strict';
import { test } from 'node:test';

import { TransportationSelectorModel } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';

test('Test_IsTransitTransportationHandledForDayPlanner_TestBulkEvaluation_ExpectHandled', () => {
   assert.equal(
      TransportationSelectorModel.isTransitTransportationHandledForDayPlanner({
         name: 'Zoomobile',
         added_as_attraction: false,
         bulk_transit_evaluated: true,
         legs: [],
      }),
      true
   );
   assert.equal(
      TransportationSelectorModel.isTransitTransportationHandledForDayPlanner({
         name: 'Zoomobile',
         added_as_attraction: false,
         bulk_transit_evaluated: false,
         legs: [],
      }),
      false
   );
});

test('Test_BuildTransportationStationsLine_TestPureTransport_ExpectOmitMainStationRoundTrip', () => {
   assert.equal(
      TransportationSelectorModel.buildTransportationStationsLine({
         name: 'Zoomobile',
         added_as_attraction: false,
         main_station: 'Main Zoomobile Station',
         legs: [],
      }),
      ''
   );
   assert.equal(
      TransportationSelectorModel.buildTransportationStationsLine({
         name: 'Zoomobile',
         added_as_attraction: true,
         main_station: 'Main Zoomobile Station',
         legs: [],
      }),
      'Main Zoomobile Station (round trip)'
   );
});

test('Test_IsScheduleItemTransportationRow_TestKinds_ExpectRecognized', () => {
   assert.equal(
      TransportationSelectorModel.isScheduleItemTransportationRow({
         scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType,
      }),
      true
   );
   assert.equal(
      TransportationSelectorModel.isScheduleItemTransportationRow({
         is_also_transportation: true,
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      }),
      false
   );
   assert.equal(
      TransportationSelectorModel.isScheduleItemTransportationRow({
         added_as_attraction: true,
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      }),
      true
   );
   assert.equal(
      TransportationSelectorModel.isScheduleItemTransportationRow({
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      }),
      false
   );
});

test('Test_MakeTransportationSelection_TestScheduledLegs_ExpectStationsSubtitle', () => {
   assert.deepEqual(
      TransportationSelectorModel.makeTransportationSelection({
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
         subtitle: 'Main Zoomobile Station → Canadian Domain Zoomobile Station',
         infoLink: 'https://example.com/zoomobile',
         imageSrc: '../images/details/transportations/zoomobile.png',
         addedAsAttraction: false,
      }
   );
});

test('Test_MakeTransportationSelection_TestNoLegs_ExpectCostAndHoursSubtitle', () => {
   assert.deepEqual(
      TransportationSelectorModel.makeTransportationSelection({
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

test('Test_ShouldConfirmAddAsTransportation_TestAlsoAttraction_ExpectPromptOnlyWhenAdding', () => {
   const zoomobileRow = { is_also_attraction: true };
   const pureTransportationRow = { is_also_attraction: false };

   assert.equal(
      TransportationSelectorModel.shouldConfirmAddAsTransportation({
         row: zoomobileRow,
         isSelected: false,
      }),
      true
   );
   assert.equal(
      TransportationSelectorModel.shouldConfirmAddAsTransportation({
         row: zoomobileRow,
         isSelected: true,
      }),
      false
   );
   assert.equal(
      TransportationSelectorModel.shouldConfirmAddAsTransportation({
         row: pureTransportationRow,
         isSelected: false,
      }),
      false
   );
});

test('Test_BuildAddAsTransportationMessage_TestZoomobile_ExpectBulkSchedulingCopy', () => {
   assert.equal(
      TransportationSelectorModel.buildAddAsTransportationMessage({ name: 'Zoomobile' }),
      'The Zoomobile will be used to reduce walking distance when bulk scheduling. This action will add the Zoomobile as a transportation method.'
   );
});

test('Test_MigrateStoredTransportations_TestStringAndObject_ExpectNormalized', () => {
   assert.deepEqual(
      TransportationSelectorModel.migrateStoredTransportations([
         'Zoomobile',
         {
            id: 'Zoomobile',
            name: 'Zoomobile',
            subtitle: 'Main Zoomobile Station',
            addedAsAttraction: false,
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
