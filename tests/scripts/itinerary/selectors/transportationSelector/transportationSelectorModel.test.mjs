import assert from 'node:assert/strict';
import { test } from 'node:test';

import { TransportationSelectorModel } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { TransportationStationNameResolver } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationStationNameResolver.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../../scripts/strings.js';


test('Test_IsTransitTransportationHandledForDayPlanner_TestBulkEvaluated_ExpectTrue', () => {
   const row = {
      name: 'Zoomobile',
      added_as_attraction: false,
      bulk_transit_evaluated: true,
      legs: [],
   };

   const handled = TransportationSelectorModel.isTransitTransportationHandledForDayPlanner(row);

   assert.equal(handled, true);
});


test('Test_IsTransitTransportationHandledForDayPlanner_TestNotEvaluated_ExpectFalse', () => {
   const row = {
      name: 'Zoomobile',
      added_as_attraction: false,
      bulk_transit_evaluated: false,
      legs: [],
   };

   const handled = TransportationSelectorModel.isTransitTransportationHandledForDayPlanner(row);

   assert.equal(handled, false);
});


test('Test_BuildTransportationStationsLine_TestPureTransport_ExpectEmpty', () => {
   const row = {
      name: 'Zoomobile',
      added_as_attraction: false,
      main_station: 'Main Zoomobile Station',
      legs: [],
   };

   const line = TransportationSelectorModel.buildTransportationStationsLine(row);

   assert.equal(line, '');
});


test('Test_BuildTransportationStationsLine_TestAttraction_ExpectRoundTrip', () => {
   const station = 'Main Zoomobile Station';
   const row = {
      name: 'Zoomobile',
      added_as_attraction: true,
      main_station: station,
      legs: [],
   };

   const line = TransportationSelectorModel.buildTransportationStationsLine(row);

   assert.equal(line, Strings.labels.transportationRoundTrip(station));
});


test('Test_IsScheduleItemTransportationRow_TestTransportationKind_ExpectTrue', () => {
   const row = {
      scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType,
   };

   const isTransportation = TransportationSelectorModel.isScheduleItemTransportationRow(row);

   assert.equal(isTransportation, true);
});


test('Test_IsScheduleItemTransportationRow_TestAlsoTransportationAttraction_ExpectFalse', () => {
   const row = {
      is_also_transportation: true,
      scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
   };

   const isTransportation = TransportationSelectorModel.isScheduleItemTransportationRow(row);

   assert.equal(isTransportation, false);
});


test('Test_IsScheduleItemTransportationRow_TestAddedAsAttraction_ExpectTrue', () => {
   const row = {
      added_as_attraction: true,
      scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
   };

   const isTransportation = TransportationSelectorModel.isScheduleItemTransportationRow(row);

   assert.equal(isTransportation, true);
});


test('Test_IsScheduleItemTransportationRow_TestAttractionKind_ExpectFalse', () => {
   const row = {
      scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
   };

   const isTransportation = TransportationSelectorModel.isScheduleItemTransportationRow(row);

   assert.equal(isTransportation, false);
});


test('Test_MakeTransportationSelection_TestScheduledLegs_ExpectStationsSubtitle', () => {
   const name = 'Zoomobile';
   const infoLink = 'https://example.com/zoomobile';
   const fromStation = 'Main Zoomobile Station';
   const toStation = 'Canadian Domain Zoomobile Station';
   const row = {
      name,
      info_link: infoLink,
      free_with_admission: false,
      open_time: '10:00 AM',
      close_time: '4:00 PM',
      legs: [
         {
            from_station: fromStation,
            to_station: toStation,
         },
      ],
   };

   const selection = TransportationSelectorModel.makeTransportationSelection(row);

   assert.equal(selection.id, name);
   assert.equal(selection.name, name);
   assert.equal(selection.subtitle, Strings.labels.transportationStations(fromStation, toStation));
   assert.equal(selection.infoLink, infoLink);
   assert.equal(selection.imageSrc, TransportationSelectorModel.buildTransportationImageSrc(row));
   assert.equal(selection.addedAsAttraction, false);
});


test('Test_MakeTransportationSelection_TestNoLegs_ExpectCostAndHoursSubtitle', () => {
   const name = 'Zoomobile';
   const openTime = '10:00 AM';
   const closeTime = '4:00 PM';
   const row = {
      name,
      free_with_admission: false,
      open_time: openTime,
      close_time: closeTime,
   };

   const selection = TransportationSelectorModel.makeTransportationSelection(row);

   assert.equal(selection.id, name);
   assert.equal(selection.name, name);
   assert.match(selection.subtitle, new RegExp(Strings.search.extraCharge));
   assert.match(selection.subtitle, new RegExp(openTime));
   assert.match(selection.subtitle, new RegExp(closeTime));
   assert.equal(selection.imageSrc, TransportationSelectorModel.buildTransportationImageSrc(row));
});


test('Test_ShouldConfirmAddAsTransportation_TestAddingAlsoAttraction_ExpectTrue', () => {
   const zoomobileRow = { is_also_attraction: true };

   const shouldConfirm = TransportationSelectorModel.shouldConfirmAddAsTransportation({
      row: zoomobileRow,
      isSelected: false,
   });

   assert.equal(shouldConfirm, true);
});


test('Test_ShouldConfirmAddAsTransportation_TestAlreadySelected_ExpectFalse', () => {
   const zoomobileRow = { is_also_attraction: true };

   const shouldConfirm = TransportationSelectorModel.shouldConfirmAddAsTransportation({
      row: zoomobileRow,
      isSelected: true,
   });

   assert.equal(shouldConfirm, false);
});


test('Test_ShouldConfirmAddAsTransportation_TestPureTransportation_ExpectFalse', () => {
   const pureTransportationRow = { is_also_attraction: false };

   const shouldConfirm = TransportationSelectorModel.shouldConfirmAddAsTransportation({
      row: pureTransportationRow,
      isSelected: false,
   });

   assert.equal(shouldConfirm, false);
});


test('Test_BuildAddAsTransportationMessage_TestZoomobile_ExpectBulkSchedulingCopy', () => {
   const name = 'Zoomobile';
   const row = { name };

   const message = TransportationSelectorModel.buildAddAsTransportationMessage(row);

   assert.equal(message, Strings.itinerary.confirmation.addAsTransportationMessage(name));
});


test('Test_MigrateStoredTransportations_TestStringAndObject_ExpectNormalized', () => {
   const name = 'Zoomobile';
   const subtitle = 'Main Zoomobile Station';
   const items = [
      name,
      {
         id: name,
         name,
         subtitle,
         addedAsAttraction: false,
      },
      { name: '' },
   ];

   const migrated = TransportationSelectorModel.migrateStoredTransportations(items);

   assert.deepEqual(
      migrated.at(Position.FIRST),
      TransportationStationNameResolver.createStoredTransportationFromString(name)
   );
   assert.deepEqual(
      migrated.at(Position.SECOND),
      TransportationStationNameResolver.createStoredTransportationFromObject({
         id: name,
         name,
         subtitle,
         addedAsAttraction: false,
      })
   );
});


test('Test_GetTransportationScheduleItemKey_TestBlankName_ExpectEmpty', () => {
   const row = { name: '' };

   const key = TransportationSelectorModel.getTransportationScheduleItemKey(row);

   assert.equal(key, '');
});


test('Test_IsTransportationScheduled_TestLegs_ExpectTrue', () => {
   const row = {
      name: 'Zoomobile',
      legs: [{ from_station: 'A', to_station: 'B' }],
   };

   const scheduled = TransportationSelectorModel.isTransportationScheduled(row);

   assert.equal(scheduled, true);
});


test('Test_IsTransitTransportationHandledForDayPlanner_TestAttractionWindow_ExpectTrue', () => {
   const row = {
      name: 'Zoomobile',
      added_as_attraction: true,
      start_time: '10:00 AM',
      end_time: '10:30 AM',
   };

   const handled = TransportationSelectorModel.isTransitTransportationHandledForDayPlanner(row);

   assert.equal(handled, true);
});


test('Test_BuildTransportationStationsLine_TestSingleStation_ExpectStation', () => {
   const station = 'Main Station';
   const row = {
      name: 'Zoomobile',
      added_as_attraction: false,
      legs: [{ from_station: station, to_station: '' }],
   };

   const line = TransportationSelectorModel.buildTransportationStationsLine(row);

   assert.equal(line, station);
});


test('Test_IsScheduleItemTransportationRow_TestNull_ExpectFalse', () => {
   const row = null;

   const isTransportation = TransportationSelectorModel.isScheduleItemTransportationRow(row);

   assert.equal(isTransportation, false);
});


test('Test_IsScheduleItemTransportationRow_TestString_ExpectFalse', () => {
   const row = 'row';

   const isTransportation = TransportationSelectorModel.isScheduleItemTransportationRow(row);

   assert.equal(isTransportation, false);
});


test('Test_GetTransportationTitle_TestBlankName_ExpectFallback', () => {
   const row = { name: '' };

   const title = TransportationSelectorModel.getTransportationTitle(row);

   assert.equal(title, Strings.entityLabels.transportation);
});
