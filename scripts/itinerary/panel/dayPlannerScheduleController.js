import { DayPlannerScheduleHelper } from './dayPlannerScheduleHelper.js';
import { ItineraryShape } from '../itineraryShape.js';
import { TimelineLayoutConstants } from '../../shared/timelineLayoutConstants.js';
import { ZooClockTimeHelper } from '../../shared/zooClockTimeHelper.js';

export class DayPlannerScheduleController {
   static parseClockTimeMinutes(timeValue) {
      return ZooClockTimeHelper.parseMinutes(timeValue);
   }

   static formatMinutesAsScheduleTimeKey(totalMinutes) {
      const hours = Math.floor(totalMinutes / 60);
      const minutes = totalMinutes % 60;

      return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
   }

   static formatMinutesAsClockTime(totalMinutes) {
      return ZooClockTimeHelper.formatClockTime(
         DayPlannerScheduleController.formatMinutesAsScheduleTimeKey(totalMinutes)
      );
   }

   static collectFixedZooScheduleStartMinutes(itinerary = {}) {
      return [
         ...ItineraryShape.normalizeItineraryItems(itinerary.guardiansTalks),
         ...ItineraryShape.normalizeItineraryItems(itinerary.wildEncounters),
      ]
         .filter((item) => item && item.is_deleted !== true)
         .map((item) => DayPlannerScheduleController.parseClockTimeMinutes(item.start_time))
         .filter((startMinutes) => Number.isFinite(startMinutes));
   }

   static earliestFixedZooScheduleStartMinutes(itinerary = {}) {
      const startMinutes = DayPlannerScheduleController.collectFixedZooScheduleStartMinutes(itinerary);

      return startMinutes.length > 0
         ? Math.min(...startMinutes)
         : null;
   }

   static resolveDayPlannerTimelineStartMinutes(zooHours = {}, itinerary = {}) {
      const earlyAdmissionMinutes = DayPlannerScheduleController.parseClockTimeMinutes(
         zooHours.earlyAdmissionTime
      );
      const openMinutes = DayPlannerScheduleController.parseClockTimeMinutes(zooHours.openTime);
      const arrivalMinutes = DayPlannerScheduleController.parseClockTimeMinutes(itinerary.arrivalTime);
      const zooFloorMinutes = Number.isFinite(earlyAdmissionMinutes)
         ? earlyAdmissionMinutes
         : openMinutes;
      const fixedZooStartMinutes = DayPlannerScheduleController.earliestFixedZooScheduleStartMinutes(
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
      const earlyAdmissionMinutes = DayPlannerScheduleController.parseClockTimeMinutes(
         zooHours.earlyAdmissionTime
      );
      const openMinutes = DayPlannerScheduleController.parseClockTimeMinutes(zooHours.openTime);
      const lastAdmissionMinutes = DayPlannerScheduleController.parseClockTimeMinutes(
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
         minScheduleTime: DayPlannerScheduleController.formatMinutesAsScheduleTimeKey(minMinutes),
         maxScheduleTime: DayPlannerScheduleController.formatMinutesAsScheduleTimeKey(
            lastAdmissionMinutes
         ),
         minClockTime: DayPlannerScheduleController.formatMinutesAsClockTime(minMinutes),
         maxClockTime: DayPlannerScheduleController.formatMinutesAsClockTime(lastAdmissionMinutes),
      };
   }

   static isArrivalTimeWithinBounds(timeValue, bounds) {
      return DayPlannerScheduleHelper.isTimeWithinBounds(timeValue, bounds);
   }

   static buildDepartureTimeBounds(zooHours = {}) {
      const openMinutes = DayPlannerScheduleController.parseClockTimeMinutes(zooHours.openTime);
      const closeMinutes = DayPlannerScheduleController.parseClockTimeMinutes(zooHours.closeTime);

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
         minScheduleTime: DayPlannerScheduleController.formatMinutesAsScheduleTimeKey(openMinutes),
         maxScheduleTime: DayPlannerScheduleController.formatMinutesAsScheduleTimeKey(closeMinutes),
         minClockTime: DayPlannerScheduleController.formatMinutesAsClockTime(openMinutes),
         maxClockTime: DayPlannerScheduleController.formatMinutesAsClockTime(closeMinutes),
      };
   }

   static isDepartureTimeWithinBounds(timeValue, bounds) {
      return DayPlannerScheduleHelper.isTimeWithinBounds(timeValue, bounds);
   }

   static areItineraryScheduleTimesOrdered(arrivalTime, departureTime) {
      const arrivalMinutes = DayPlannerScheduleController.parseClockTimeMinutes(arrivalTime);
      const departureMinutes = DayPlannerScheduleController.parseClockTimeMinutes(departureTime);

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
      if (!DayPlannerScheduleController.isArrivalTimeWithinBounds(timeValue, bounds)) {
         return strings.arrivalTimeInvalid;
      }

      if (!DayPlannerScheduleController.areItineraryScheduleTimesOrdered(timeValue, departureTime)) {
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
      if (!DayPlannerScheduleController.isDepartureTimeWithinBounds(timeValue, bounds)) {
         return strings.departureTimeInvalid;
      }

      if (!DayPlannerScheduleController.areItineraryScheduleTimesOrdered(arrivalTime, timeValue)) {
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
      const firstHalfHour = Math.ceil(openMinutes / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES)
         * TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

      slotStarts.push(openMinutes);

      for (
         let slotStart = firstHalfHour;
         slotStart < closeMinutes;
         slotStart += TimelineLayoutConstants.TIMELINE_SLOT_MINUTES
      ) {
         if (slotStart === openMinutes) {
            continue;
         }

         slotStarts.push(slotStart);
      }

      return slotStarts;
   }
}
