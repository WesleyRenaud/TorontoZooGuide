import { DayPlannerSchedule } from '../dayPlannerSchedule.js';
import { Dom } from '../dom.js';
import { ItineraryTimeInput } from './itineraryTimeInput.js';

export class DayPlannerControls {
   static makeDayPlannerControls(
      date,
      itinerary = {},
      {
         onArrivalTimeChange = null,
         onDepartureTimeChange = null,
      } = {},
      strings = {},
      zooHours = {}
   ) {
      const controls = Dom.el('div', 'itinerary-day-module-controls');
      const arrivalBounds = DayPlannerSchedule.buildArrivalTimeBounds(zooHours);
      const departureBounds = DayPlannerSchedule.buildDepartureTimeBounds(zooHours);

      controls.appendChild(Dom.el('span', 'itinerary-day-module-date', date));
      controls.appendChild(
         ItineraryTimeInput.makeItineraryTimeInput({
            label: strings.arrivalInputLabel,
            value: itinerary.arrivalTime,
            onChange: onArrivalTimeChange,
            clearAriaLabel: strings.clearArrivalTimeAria,
            validateTime: (timeValue) => !DayPlannerSchedule.resolveArrivalTimeValidationError(
               timeValue,
               arrivalBounds,
               itinerary.departureTime,
               strings
            ),
            resolveInvalidMessage: (timeValue) => DayPlannerSchedule.resolveArrivalTimeValidationError(
               timeValue,
               arrivalBounds,
               itinerary.departureTime,
               strings
            ),
            invalidMessage: strings.arrivalTimeInvalid,
         })
      );
      controls.appendChild(
         ItineraryTimeInput.makeItineraryTimeInput({
            label: strings.departureInputLabel,
            value: itinerary.departureTime,
            onChange: onDepartureTimeChange,
            clearAriaLabel: strings.clearDepartureTimeAria,
            validateTime: (timeValue) => !DayPlannerSchedule.resolveDepartureTimeValidationError(
               timeValue,
               departureBounds,
               itinerary.arrivalTime,
               strings
            ),
            resolveInvalidMessage: (timeValue) => DayPlannerSchedule.resolveDepartureTimeValidationError(
               timeValue,
               departureBounds,
               itinerary.arrivalTime,
               strings
            ),
            invalidMessage: strings.departureTimeInvalid,
         })
      );

      return controls;
   }
}
