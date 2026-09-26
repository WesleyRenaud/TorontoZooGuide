import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerController } from '../../../../../scripts/itinerary/panel/components/dayPlannerController.js';
import { DayPlannerScheduleController } from '../../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { ItineraryPanelHelper } from '../../../../../scripts/itinerary/panel/itineraryPanelHelper.js';
import { ItineraryTimeView } from '../../../../../scripts/itinerary/panel/components/itineraryTimeView.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _createElement(tag, className, text) {
   const el = document.createElement(tag);
   if (className) el.className = className;
   if (text != null) el.textContent = text;
   return el;
}

installDomTestHooks();


test('Test_MakeDayPlannerControls_TestArrivalAndDeparture_ExpectWiredInputs', () => {
   const originalEl = ItineraryPanelHelper.el;
   const originalArrivalBounds = DayPlannerScheduleController.buildArrivalTimeBounds;
   const originalDepartureBounds = DayPlannerScheduleController.buildDepartureTimeBounds;
   const originalArrivalError = DayPlannerScheduleController.resolveArrivalTimeValidationError;
   const originalDepartureError = DayPlannerScheduleController.resolveDepartureTimeValidationError;
   const originalTimeInput = ItineraryTimeView.makeItineraryTimeInput;
   const visitDate = '2026-06-01';
   const arrivalTime = '10:00';
   const departureTime = '16:00';
   const arrivalLabel = 'Arrival';
   const departureLabel = 'Departure';
   const arrivalError = 'arrival bad';
   const timeConfigs = [];

   ItineraryPanelHelper.el = _createElement;
   DayPlannerScheduleController.buildArrivalTimeBounds = () => ({ min: '09:00' });
   DayPlannerScheduleController.buildDepartureTimeBounds = () => ({ max: '18:00' });
   DayPlannerScheduleController.resolveArrivalTimeValidationError = () => arrivalError;
   DayPlannerScheduleController.resolveDepartureTimeValidationError = () => null;
   ItineraryTimeView.makeItineraryTimeInput = (config) => {
      timeConfigs.push(config);
      return _createElement('div', 'time-input');
   };

   try {
      const controls = DayPlannerController.makeDayPlannerControls(
         visitDate,
         { arrivalTime, departureTime },
         {
            onArrivalTimeChange: () => {},
            onDepartureTimeChange: () => {},
         },
         {
            arrivalInputLabel: arrivalLabel,
            departureInputLabel: departureLabel,
            clearArrivalTimeAria: 'Clear arrival',
            clearDepartureTimeAria: 'Clear departure',
            arrivalTimeInvalid: 'Arrival invalid',
            departureTimeInvalid: 'Departure invalid',
         },
         { open: '09:00', close: '18:00' }
      );
      const arrivalConfig = timeConfigs.at(Position.FIRST);
      const departureConfig = timeConfigs.at(Position.SECOND);

      assert.equal(controls.className, 'itinerary-day-module-controls');
      assert.equal(controls.children.at(Position.FIRST).textContent, visitDate);
      assert.equal(timeConfigs.length, 2);
      assert.equal(arrivalConfig.label, arrivalLabel);
      assert.equal(arrivalConfig.value, arrivalTime);
      assert.equal(arrivalConfig.validateTime(arrivalTime), false);
      assert.equal(arrivalConfig.resolveInvalidMessage(arrivalTime), arrivalError);
      assert.equal(departureConfig.label, departureLabel);
      assert.equal(departureConfig.validateTime(departureTime), true);
   } finally {
      ItineraryPanelHelper.el = originalEl;
      DayPlannerScheduleController.buildArrivalTimeBounds = originalArrivalBounds;
      DayPlannerScheduleController.buildDepartureTimeBounds = originalDepartureBounds;
      DayPlannerScheduleController.resolveArrivalTimeValidationError = originalArrivalError;
      DayPlannerScheduleController.resolveDepartureTimeValidationError = originalDepartureError;
      ItineraryTimeView.makeItineraryTimeInput = originalTimeInput;
   }
});


test('Test_MakeDayPlannerControls_TestEmptyDate_ExpectOmitsDateLabel', () => {
   const originalEl = ItineraryPanelHelper.el;
   const originalArrivalBounds = DayPlannerScheduleController.buildArrivalTimeBounds;
   const originalDepartureBounds = DayPlannerScheduleController.buildDepartureTimeBounds;
   const originalTimeInput = ItineraryTimeView.makeItineraryTimeInput;

   ItineraryPanelHelper.el = _createElement;
   DayPlannerScheduleController.buildArrivalTimeBounds = () => null;
   DayPlannerScheduleController.buildDepartureTimeBounds = () => null;
   ItineraryTimeView.makeItineraryTimeInput = () => _createElement('div', 'time-input');

   try {
      const controls = DayPlannerController.makeDayPlannerControls(
         '',
         {},
         {},
         {
            arrivalInputLabel: 'Arrival',
            departureInputLabel: 'Departure',
            clearArrivalTimeAria: 'Clear arrival',
            clearDepartureTimeAria: 'Clear departure',
         },
         {}
      );

      assert.equal(controls.querySelector('.itinerary-day-module-date'), null);
      assert.equal(controls.querySelectorAll('.time-input').length, 2);
   } finally {
      ItineraryPanelHelper.el = originalEl;
      DayPlannerScheduleController.buildArrivalTimeBounds = originalArrivalBounds;
      DayPlannerScheduleController.buildDepartureTimeBounds = originalDepartureBounds;
      ItineraryTimeView.makeItineraryTimeInput = originalTimeInput;
   }
});
