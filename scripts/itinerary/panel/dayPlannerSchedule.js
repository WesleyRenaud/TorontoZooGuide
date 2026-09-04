import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { Format } from './format.js';
import { ItineraryShape } from '../itineraryShape.js';
import { TIMELINE_SLOT_MINUTES } from '../../shared/constants.js';

function isTimeWithinBounds(timeValue, bounds) {
   if (!bounds) {
      return true;
   }

   const normalizedTimeValue = ValueNormalizer.asTrimmedString(timeValue);

   if (!normalizedTimeValue) {
      return true;
   }

   const timeMinutes = DayPlannerSchedule.parseClockTimeMinutes(normalizedTimeValue);

   if (!Number.isFinite(timeMinutes)) {
      return false;
   }

   return (
      timeMinutes >= bounds.minMinutes
      && timeMinutes <= bounds.maxMinutes
   );
}

export class DayPlannerSchedule {
   static parseClockTimeMinutes(timeValue) {
      const normalizedTimeValue = ValueNormalizer.asTrimmedString(timeValue);
      const timeParts = normalizedTimeValue.match(/^(\d{1,2}):(\d{2})(?::(\d{2}))?$/);

      if (timeParts) {
         const hours = Number(timeParts[1]);
         const minutes = Number(timeParts[2]);
         const seconds = timeParts[3] == null ? 0 : Number(timeParts[3]);

         if (
            hours < 0
            || hours > 23
            || minutes < 0
            || minutes > 59
            || seconds < 0
            || seconds > 59
         ) {
            return null;
         }

         return (hours * 60) + minutes + (seconds / 60);
      }

      const displayTimeParts = normalizedTimeValue.match(
         /^(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(AM|PM)$/i
      );

      if (!displayTimeParts) {
         return null;
      }

      const displayHours = Number(displayTimeParts[1]);
      const displayMinutes = Number(displayTimeParts[2]);
      const displaySeconds = displayTimeParts[3] == null
         ? 0
         : Number(displayTimeParts[3]);
      const period = displayTimeParts[4].toUpperCase();

      if (
         displayHours < 1
         || displayHours > 12
         || displayMinutes < 0
         || displayMinutes > 59
         || displaySeconds < 0
         || displaySeconds > 59
      ) {
         return null;
      }

      const hours = (displayHours % 12) + (period === 'PM' ? 12 : 0);

      return (hours * 60) + displayMinutes + (displaySeconds / 60);
   }

   static formatMinutesAsScheduleTimeKey(totalMinutes) {
      const hours = Math.floor(totalMinutes / 60);
      const minutes = totalMinutes % 60;

      return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
   }

   static formatMinutesAsClockTime(totalMinutes) {
      return Format.formatClockTime(
         DayPlannerSchedule.formatMinutesAsScheduleTimeKey(totalMinutes)
      );
   }

   static collectFixedZooScheduleStartMinutes(itinerary = {}) {
      return [
         ...ItineraryShape.normalizeItineraryItems(itinerary.guardiansTalks),
         ...ItineraryShape.normalizeItineraryItems(itinerary.wildEncounters),
      ]
         .filter((item) => item && item.is_deleted !== true)
         .map((item) => DayPlannerSchedule.parseClockTimeMinutes(item.start_time))
         .filter((startMinutes) => Number.isFinite(startMinutes));
   }

   static earliestFixedZooScheduleStartMinutes(itinerary = {}) {
      const startMinutes = DayPlannerSchedule.collectFixedZooScheduleStartMinutes(itinerary);

      return startMinutes.length > 0
         ? Math.min(...startMinutes)
         : null;
   }

   static resolveDayPlannerTimelineStartMinutes(zooHours = {}, itinerary = {}) {
      const earlyAdmissionMinutes = DayPlannerSchedule.parseClockTimeMinutes(
         zooHours.earlyAdmissionTime
      );
      const openMinutes = DayPlannerSchedule.parseClockTimeMinutes(zooHours.openTime);
      const arrivalMinutes = DayPlannerSchedule.parseClockTimeMinutes(itinerary.arrivalTime);
      const zooFloorMinutes = Number.isFinite(earlyAdmissionMinutes)
         ? earlyAdmissionMinutes
         : openMinutes;
      const fixedZooStartMinutes = DayPlannerSchedule.earliestFixedZooScheduleStartMinutes(
         itinerary
      );
      const candidates = [
         zooFloorMinutes,
         arrivalMinutes,
         fixedZooStartMinutes,
      ].filter((value) => Number.isFinite(value));

      return candidates.length > 0
         ? Math.min(...candidates)
         : null;
   }

   static buildArrivalTimeBounds(zooHours = {}) {
      const earlyAdmissionMinutes = DayPlannerSchedule.parseClockTimeMinutes(
         zooHours.earlyAdmissionTime
      );
      const openMinutes = DayPlannerSchedule.parseClockTimeMinutes(zooHours.openTime);
      const lastAdmissionMinutes = DayPlannerSchedule.parseClockTimeMinutes(
         zooHours.lastAdmissionTime
      );
      const minMinutes = Number.isFinite(earlyAdmissionMinutes)
         ? earlyAdmissionMinutes
         : openMinutes;

      if (
         !Number.isFinite(minMinutes)
         || !Number.isFinite(lastAdmissionMinutes)
         || lastAdmissionMinutes < minMinutes
      ) {
         return null;
      }

      return {
         minMinutes,
         maxMinutes: lastAdmissionMinutes,
         minScheduleTime: DayPlannerSchedule.formatMinutesAsScheduleTimeKey(minMinutes),
         maxScheduleTime: DayPlannerSchedule.formatMinutesAsScheduleTimeKey(
            lastAdmissionMinutes
         ),
         minClockTime: DayPlannerSchedule.formatMinutesAsClockTime(minMinutes),
         maxClockTime: DayPlannerSchedule.formatMinutesAsClockTime(lastAdmissionMinutes),
      };
   }

   static isArrivalTimeWithinBounds(timeValue, bounds) {
      return isTimeWithinBounds(timeValue, bounds);
   }

   static buildDepartureTimeBounds(zooHours = {}) {
      const openMinutes = DayPlannerSchedule.parseClockTimeMinutes(zooHours.openTime);
      const closeMinutes = DayPlannerSchedule.parseClockTimeMinutes(zooHours.closeTime);

      if (
         !Number.isFinite(openMinutes)
         || !Number.isFinite(closeMinutes)
         || closeMinutes < openMinutes
      ) {
         return null;
      }

      return {
         minMinutes: openMinutes,
         maxMinutes: closeMinutes,
         minScheduleTime: DayPlannerSchedule.formatMinutesAsScheduleTimeKey(openMinutes),
         maxScheduleTime: DayPlannerSchedule.formatMinutesAsScheduleTimeKey(closeMinutes),
         minClockTime: DayPlannerSchedule.formatMinutesAsClockTime(openMinutes),
         maxClockTime: DayPlannerSchedule.formatMinutesAsClockTime(closeMinutes),
      };
   }

   static isDepartureTimeWithinBounds(timeValue, bounds) {
      return isTimeWithinBounds(timeValue, bounds);
   }

   static areItineraryScheduleTimesOrdered(arrivalTime, departureTime) {
      const arrivalMinutes = DayPlannerSchedule.parseClockTimeMinutes(arrivalTime);
      const departureMinutes = DayPlannerSchedule.parseClockTimeMinutes(departureTime);

      if (!Number.isFinite(arrivalMinutes) || !Number.isFinite(departureMinutes)) {
         return true;
      }

      return departureMinutes > arrivalMinutes;
   }

   static resolveArrivalTimeValidationError(
      timeValue,
      bounds,
      departureTime,
      strings = {}
   ) {
      if (!DayPlannerSchedule.isArrivalTimeWithinBounds(timeValue, bounds)) {
         return strings.arrivalTimeInvalid;
      }

      if (!DayPlannerSchedule.areItineraryScheduleTimesOrdered(timeValue, departureTime)) {
         return strings.timeOrderInvalid;
      }

      return null;
   }

   static resolveDepartureTimeValidationError(
      timeValue,
      bounds,
      arrivalTime,
      strings = {}
   ) {
      if (!DayPlannerSchedule.isDepartureTimeWithinBounds(timeValue, bounds)) {
         return strings.departureTimeInvalid;
      }

      if (!DayPlannerSchedule.areItineraryScheduleTimesOrdered(arrivalTime, timeValue)) {
         return strings.departureTimeAfterArrivalInvalid;
      }

      return null;
   }

   static buildHalfHourSlotStarts(openMinutes, closeMinutes) {
      if (
         !Number.isFinite(openMinutes)
         || !Number.isFinite(closeMinutes)
         || closeMinutes <= openMinutes
      ) {
         return [];
      }

      const slotStarts = [];
      const firstHalfHour = Math.ceil(openMinutes / TIMELINE_SLOT_MINUTES)
         * TIMELINE_SLOT_MINUTES;

      slotStarts.push(openMinutes);

      for (
         let slotStart = firstHalfHour;
         slotStart < closeMinutes;
         slotStart += TIMELINE_SLOT_MINUTES
      ) {
         if (slotStart === openMinutes) {
            continue;
         }

         slotStarts.push(slotStart);
      }

      return slotStarts;
   }
}
