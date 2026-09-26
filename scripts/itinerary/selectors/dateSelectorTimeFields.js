import { ItineraryTimeView } from '../panel/components/itineraryTimeView.js';
import { DayPlannerScheduleController } from '../panel/dayPlannerScheduleController.js';
import { Strings } from '../../strings.js';

export class DateSelectorTimeFields {
   static buildTimePickerOptions(bounds) {
      if (!bounds?.minClockTime || !bounds?.maxClockTime) {
         return {};
      }

      return {
         minTime: bounds.minClockTime,
         maxTime: bounds.maxClockTime,
      };
   }

   static resolveVisitTimesValidationError(
      arrivalTime,
      departureTime,
      zooHours,
      strings = Strings.itinerary.dayPlanner
   ) {
      if (!zooHours) {
         return null;
      }

      const arrivalBounds = DayPlannerScheduleController.buildArrivalTimeBounds(zooHours);
      const departureBounds = DayPlannerScheduleController.buildDepartureTimeBounds(zooHours);

      return DayPlannerScheduleController.resolveArrivalTimeValidationError(
         arrivalTime,
         arrivalBounds,
         departureTime,
         strings
      ) || DayPlannerScheduleController.resolveDepartureTimeValidationError(
         departureTime,
         departureBounds,
         arrivalTime,
         strings
      );
   }

   static areVisitTimesValid(
      arrivalTime,
      departureTime,
      zooHours,
      strings = Strings.itinerary.dayPlanner
   ) {
      return !DateSelectorTimeFields.resolveVisitTimesValidationError(
         arrivalTime,
         departureTime,
         zooHours,
         strings
      );
   }

   static mount({
      containerEl,
      arrivalTime = null,
      departureTime = null,
      zooHours = null,
      strings = Strings,
      makeTimeInput = ItineraryTimeView.makeItineraryTimeInput,
      onArrivalTimeChange = null,
      onDepartureTimeChange = null,
      getArrivalTime = () => arrivalTime,
      getDepartureTime = () => departureTime,
   } = {}) {
      if (!containerEl) {
         return;
      }

      const dayPlannerStrings = strings.itinerary.dayPlanner;
      const arrivalBounds = zooHours
         ? DayPlannerScheduleController.buildArrivalTimeBounds(zooHours)
         : null;
      const departureBounds = zooHours
         ? DayPlannerScheduleController.buildDepartureTimeBounds(zooHours)
         : null;

      containerEl.replaceChildren(
         makeTimeInput({
            label: dayPlannerStrings.arrivalInputLabel,
            value: arrivalTime,
            onChange: onArrivalTimeChange,
            clearAriaLabel: dayPlannerStrings.clearArrivalTimeAria,
            timePickerOptions: DateSelectorTimeFields.buildTimePickerOptions(arrivalBounds),
            validateTime: (timeValue) => !DayPlannerScheduleController.resolveArrivalTimeValidationError(
               timeValue,
               arrivalBounds,
               getDepartureTime(),
               dayPlannerStrings
            ),
            resolveInvalidMessage: (timeValue) => (
               DayPlannerScheduleController.resolveArrivalTimeValidationError(
                  timeValue,
                  arrivalBounds,
                  getDepartureTime(),
                  dayPlannerStrings
               )
            ),
            invalidMessage: dayPlannerStrings.arrivalTimeInvalid,
         }),
         makeTimeInput({
            label: dayPlannerStrings.departureInputLabel,
            value: departureTime,
            onChange: onDepartureTimeChange,
            clearAriaLabel: dayPlannerStrings.clearDepartureTimeAria,
            timePickerOptions: DateSelectorTimeFields.buildTimePickerOptions(departureBounds),
            validateTime: (timeValue) => !DayPlannerScheduleController.resolveDepartureTimeValidationError(
               timeValue,
               departureBounds,
               getArrivalTime(),
               dayPlannerStrings
            ),
            resolveInvalidMessage: (timeValue) => (
               DayPlannerScheduleController.resolveDepartureTimeValidationError(
                  timeValue,
                  departureBounds,
                  getArrivalTime(),
                  dayPlannerStrings
               )
            ),
            invalidMessage: dayPlannerStrings.departureTimeInvalid,
         })
      );
   }
}
