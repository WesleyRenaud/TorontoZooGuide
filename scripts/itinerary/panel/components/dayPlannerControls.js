import {
   buildArrivalTimeBounds,
   buildDepartureTimeBounds,
   resolveArrivalTimeValidationError,
   resolveDepartureTimeValidationError,
} from '../dayPlannerSchedule.js';
import { el } from '../dom.js';
import { makeItineraryTimeInput } from './itineraryTimeInput.js';

export function makeDayPlannerControls(
   date,
   itinerary = {},
   {
      onArrivalTimeChange = null,
      onDepartureTimeChange = null,
   } = {},
   strings = {},
   zooHours = {}
) {
   const controls = el('div', 'itinerary-day-module-controls');
   const arrivalBounds = buildArrivalTimeBounds(zooHours);
   const departureBounds = buildDepartureTimeBounds(zooHours);

   controls.appendChild(el('span', 'itinerary-day-module-date', date));
   controls.appendChild(
      makeItineraryTimeInput({
         label: strings.arrivalInputLabel,
         value: itinerary.arrivalTime,
         onChange: onArrivalTimeChange,
         validateTime: (timeValue) => !resolveArrivalTimeValidationError(
            timeValue,
            arrivalBounds,
            itinerary.departureTime,
            strings
         ),
         resolveInvalidMessage: (timeValue) => resolveArrivalTimeValidationError(
            timeValue,
            arrivalBounds,
            itinerary.departureTime,
            strings
         ),
         invalidMessage: strings.arrivalTimeInvalid,
      })
   );
   controls.appendChild(
      makeItineraryTimeInput({
         label: strings.departureInputLabel,
         value: itinerary.departureTime,
         onChange: onDepartureTimeChange,
         validateTime: (timeValue) => !resolveDepartureTimeValidationError(
            timeValue,
            departureBounds,
            itinerary.arrivalTime,
            strings
         ),
         resolveInvalidMessage: (timeValue) => resolveDepartureTimeValidationError(
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
