import { DayPlannerScheduleController } from '../dayPlannerScheduleController.js';
import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { ItineraryTimeView } from './itineraryTimeView.js';

export class DayPlannerController {
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
      const controls = ItineraryPanelHelper.el('div', 'itinerary-day-module-controls');
      const arrivalBounds = DayPlannerScheduleController.buildArrivalTimeBounds(zooHours);
      const departureBounds = DayPlannerScheduleController.buildDepartureTimeBounds(zooHours);

      if (date) {
         controls.appendChild(ItineraryPanelHelper.el('span', 'itinerary-day-module-date', date));
      }

      controls.appendChild(
         ItineraryTimeView.makeItineraryTimeInput({
            label: strings.arrivalInputLabel,
            value: itinerary.arrivalTime,
            onChange: onArrivalTimeChange,
            clearAriaLabel: strings.clearArrivalTimeAria,
            validateTime: (timeValue) => !DayPlannerScheduleController.resolveArrivalTimeValidationError(
               timeValue,
               arrivalBounds,
               itinerary.departureTime,
               strings
            ),
            resolveInvalidMessage: (timeValue) => DayPlannerScheduleController.resolveArrivalTimeValidationError(
               timeValue,
               arrivalBounds,
               itinerary.departureTime,
               strings
            ),
            invalidMessage: strings.arrivalTimeInvalid,
         })
      );
      controls.appendChild(
         ItineraryTimeView.makeItineraryTimeInput({
            label: strings.departureInputLabel,
            value: itinerary.departureTime,
            onChange: onDepartureTimeChange,
            clearAriaLabel: strings.clearDepartureTimeAria,
            validateTime: (timeValue) => !DayPlannerScheduleController.resolveDepartureTimeValidationError(
               timeValue,
               departureBounds,
               itinerary.arrivalTime,
               strings
            ),
            resolveInvalidMessage: (timeValue) => DayPlannerScheduleController.resolveDepartureTimeValidationError(
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
