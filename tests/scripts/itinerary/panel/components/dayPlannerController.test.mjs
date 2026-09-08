import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerController } from '../../../../../scripts/itinerary/panel/components/dayPlannerController.js';
import { DayPlannerScheduleController } from '../../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { ItineraryPanelHelper } from '../../../../../scripts/itinerary/panel/itineraryPanelHelper.js';
import { ItineraryTimeView } from '../../../../../scripts/itinerary/panel/components/itineraryTimeView.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_MakeDayPlannerControls_TestArrivalAndDeparture_ExpectWiredInputs', () => {
   const originalEl = ItineraryPanelHelper.el;
   const originalArrivalBounds = DayPlannerScheduleController.buildArrivalTimeBounds;
   const originalDepartureBounds = DayPlannerScheduleController.buildDepartureTimeBounds;
   const originalArrivalError = DayPlannerScheduleController.resolveArrivalTimeValidationError;
   const originalDepartureError = DayPlannerScheduleController.resolveDepartureTimeValidationError;
   const originalTimeInput = ItineraryTimeView.makeItineraryTimeInput;
   const timeConfigs = [];

   ItineraryPanelHelper.el = (tag, className, text) => {
      const el = document.createElement(tag);
      if (className) el.className = className;
      if (text != null) el.textContent = text;
      return el;
   };
   DayPlannerScheduleController.buildArrivalTimeBounds = () => ({ min: '09:00' });
   DayPlannerScheduleController.buildDepartureTimeBounds = () => ({ max: '18:00' });
   DayPlannerScheduleController.resolveArrivalTimeValidationError = () => 'arrival bad';
   DayPlannerScheduleController.resolveDepartureTimeValidationError = () => null;
   ItineraryTimeView.makeItineraryTimeInput = (config) => {
      timeConfigs.push(config);
      const el = document.createElement('div');
      el.className = 'time-input';
      return el;
   };

   try {
      const controls = DayPlannerController.makeDayPlannerControls(
         '2026-06-01',
         { arrivalTime: '10:00', departureTime: '16:00' },
         {
            onArrivalTimeChange: () => {},
            onDepartureTimeChange: () => {},
         },
         {
            arrivalInputLabel: 'Arrival',
            departureInputLabel: 'Departure',
            clearArrivalTimeAria: 'Clear arrival',
            clearDepartureTimeAria: 'Clear departure',
            arrivalTimeInvalid: 'Arrival invalid',
            departureTimeInvalid: 'Departure invalid',
         },
         { open: '09:00', close: '18:00' }
      );

      assert.equal(controls.className, 'itinerary-day-module-controls');
      assert.equal(controls.children[0].textContent, '2026-06-01');
      assert.equal(timeConfigs.length, 2);
      assert.equal(timeConfigs[0].label, 'Arrival');
      assert.equal(timeConfigs[0].value, '10:00');
      assert.equal(timeConfigs[0].validateTime('10:00'), false);
      assert.equal(timeConfigs[0].resolveInvalidMessage('10:00'), 'arrival bad');
      assert.equal(timeConfigs[1].label, 'Departure');
      assert.equal(timeConfigs[1].validateTime('16:00'), true);
   } finally {
      ItineraryPanelHelper.el = originalEl;
      DayPlannerScheduleController.buildArrivalTimeBounds = originalArrivalBounds;
      DayPlannerScheduleController.buildDepartureTimeBounds = originalDepartureBounds;
      DayPlannerScheduleController.resolveArrivalTimeValidationError = originalArrivalError;
      DayPlannerScheduleController.resolveDepartureTimeValidationError = originalDepartureError;
      ItineraryTimeView.makeItineraryTimeInput = originalTimeInput;
   }
});
