import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerScheduleController } from '../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { DateSelectorTimeFields } from '../../../../scripts/itinerary/selectors/dateSelectorTimeFields.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';

const _openTime = '9:30 AM';
const _closeTime = '6:00 PM';
const _lastAdmissionTime = '5:00 PM';
const _zooHours = {
   openTime: _openTime,
   closeTime: _closeTime,
   lastAdmissionTime: _lastAdmissionTime,
};
const _arrivalTime = '10:00 AM';
const _departureTime = '4:00 PM';


test('Test_BuildTimePickerOptions_TestMissingBounds_ExpectEmpty', () => {
   const options = DateSelectorTimeFields.buildTimePickerOptions(null);

   assert.deepEqual(options, {});
});


test('Test_BuildTimePickerOptions_TestBounds_ExpectMinMax', () => {
   const bounds = DayPlannerScheduleController.buildArrivalTimeBounds(_zooHours);

   const options = DateSelectorTimeFields.buildTimePickerOptions(bounds);

   assert.deepEqual(options, {
      minTime: bounds.minClockTime,
      maxTime: bounds.maxClockTime,
   });
});


test('Test_AreVisitTimesValid_TestNullHours_ExpectTrue', () => {
   const isValid = DateSelectorTimeFields.areVisitTimesValid('', '', null);

   assert.equal(isValid, true);
});


test('Test_AreVisitTimesValid_TestOrdered_ExpectTrue', () => {
   const isValid = DateSelectorTimeFields.areVisitTimesValid(
      _arrivalTime,
      _departureTime,
      _zooHours
   );

   assert.equal(isValid, true);
});


test('Test_AreVisitTimesValid_TestReversed_ExpectFalse', () => {
   const isValid = DateSelectorTimeFields.areVisitTimesValid(
      _departureTime,
      _arrivalTime,
      _zooHours
   );

   assert.equal(isValid, false);
});


test('Test_ResolveVisitTimesValidationError_TestReversedArrival_ExpectTimeOrderInvalid', () => {
   const error = DateSelectorTimeFields.resolveVisitTimesValidationError(
      _departureTime,
      _arrivalTime,
      _zooHours
   );

   assert.equal(error, Strings.itinerary.errors.timeOrderInvalid);
});


test('Test_Mount_TestMissingContainer_ExpectNoOp', () => {
   assert.doesNotThrow(() => {
      DateSelectorTimeFields.mount();
   });
});


test('Test_Mount_TestContainer_ExpectTimeInputs', () => {
   const containerEl = createDomNode('div', 'itin-date-time-fields');
   const labels = [];

   DateSelectorTimeFields.mount({
      containerEl,
      arrivalTime: _arrivalTime,
      departureTime: _departureTime,
      zooHours: _zooHours,
      makeTimeInput: ({ label }) => {
         labels.push(label);
         return createDomNode('label', 'itinerary-day-time-control', label);
      },
   });

   assert.deepEqual(labels, [
      Strings.itinerary.dayPlanner.arrivalInputLabel,
      Strings.itinerary.dayPlanner.departureInputLabel,
   ]);
   assert.equal(containerEl.children.length, 2);
});


test('Test_Mount_TestValidationCallbacks_ExpectArrivalAndDepartureChecks', () => {
   const containerEl = createDomNode('div', 'itin-date-time-fields');
   const timeConfigs = [];
   const dayPlannerStrings = Strings.itinerary.dayPlanner;

   DateSelectorTimeFields.mount({
      containerEl,
      arrivalTime: _arrivalTime,
      departureTime: _departureTime,
      zooHours: _zooHours,
      makeTimeInput: (config) => {
         timeConfigs.push(config);
         return createDomNode('label', 'itinerary-day-time-control', config.label);
      },
      getArrivalTime: () => _arrivalTime,
      getDepartureTime: () => _departureTime,
   });

   const arrivalConfig = timeConfigs.at(Position.FIRST);
   const departureConfig = timeConfigs.at(Position.SECOND);

   const isArrivalValid = arrivalConfig.validateTime(_arrivalTime);
   const arrivalInvalidMessage = arrivalConfig.resolveInvalidMessage(_closeTime);
   const isDepartureValid = departureConfig.validateTime(_departureTime);
   const departureInvalidMessage = departureConfig.resolveInvalidMessage(_openTime);

   assert.equal(isArrivalValid, true);
   assert.equal(arrivalInvalidMessage, dayPlannerStrings.arrivalTimeInvalid);
   assert.equal(isDepartureValid, true);
   assert.equal(
      departureInvalidMessage,
      dayPlannerStrings.departureTimeAfterArrivalInvalid
   );
});


test('Test_Mount_TestReversedArrival_ExpectTimeOrderInvalid', () => {
   const containerEl = createDomNode('div', 'itin-date-time-fields');
   const timeConfigs = [];

   DateSelectorTimeFields.mount({
      containerEl,
      arrivalTime: _arrivalTime,
      departureTime: _departureTime,
      zooHours: _zooHours,
      makeTimeInput: (config) => {
         timeConfigs.push(config);
         return createDomNode('label', 'itinerary-day-time-control', config.label);
      },
      getArrivalTime: () => _arrivalTime,
      getDepartureTime: () => _departureTime,
   });

   const arrivalConfig = timeConfigs.at(Position.FIRST);
   const reversedArrivalTime = _departureTime;

   const isArrivalValid = arrivalConfig.validateTime(reversedArrivalTime);
   const arrivalInvalidMessage = arrivalConfig.resolveInvalidMessage(reversedArrivalTime);

   assert.equal(isArrivalValid, false);
   assert.equal(arrivalInvalidMessage, Strings.itinerary.errors.timeOrderInvalid);
});
