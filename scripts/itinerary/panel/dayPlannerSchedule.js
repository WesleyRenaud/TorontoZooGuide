import { formatClockTime } from './format.js';
import { TIMELINE_SLOT_MINUTES } from '../../shared/constants.js';

export function parseClockTimeMinutes(timeValue) {
   if (typeof timeValue !== 'string') {
      return null;
   }

   const normalizedTimeValue = timeValue.trim();
   const timeParts = normalizedTimeValue.match(/^(\d{1,2}):(\d{2})$/);

   if (timeParts) {
      const hours = Number(timeParts[1]);
      const minutes = Number(timeParts[2]);

      if (hours < 0 || hours > 23 || minutes < 0 || minutes > 59) {
         return null;
      }

      return (hours * 60) + minutes;
   }

   const displayTimeParts = normalizedTimeValue.match(/^(\d{1,2}):(\d{2})\s*(AM|PM)$/i);

   if (!displayTimeParts) {
      return null;
   }

   const displayHours = Number(displayTimeParts[1]);
   const displayMinutes = Number(displayTimeParts[2]);
   const period = displayTimeParts[3].toUpperCase();

   if (
      displayHours < 1
      || displayHours > 12
      || displayMinutes < 0
      || displayMinutes > 59
   ) {
      return null;
   }

   const hours = (displayHours % 12) + (period === 'PM' ? 12 : 0);

   return (hours * 60) + displayMinutes;
}

export function formatMinutesAsScheduleTimeKey(totalMinutes) {
   const hours = Math.floor(totalMinutes / 60);
   const minutes = totalMinutes % 60;

   return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
}

export function formatMinutesAsClockTime(totalMinutes) {
   return formatClockTime(formatMinutesAsScheduleTimeKey(totalMinutes));
}

export function buildArrivalTimeBounds(zooHours = {}) {
   const earlyAdmissionMinutes = parseClockTimeMinutes(zooHours.earlyAdmissionTime);
   const openMinutes = parseClockTimeMinutes(zooHours.openTime);
   const lastAdmissionMinutes = parseClockTimeMinutes(zooHours.lastAdmissionTime);
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
      minScheduleTime: formatMinutesAsScheduleTimeKey(minMinutes),
      maxScheduleTime: formatMinutesAsScheduleTimeKey(lastAdmissionMinutes),
      minClockTime: formatMinutesAsClockTime(minMinutes),
      maxClockTime: formatMinutesAsClockTime(lastAdmissionMinutes),
   };
}

function isTimeWithinBounds(timeValue, bounds) {
   if (!bounds) {
      return true;
   }

   const normalizedTimeValue = typeof timeValue === 'string'
      ? timeValue.trim()
      : '';

   if (!normalizedTimeValue) {
      return true;
   }

   const timeMinutes = parseClockTimeMinutes(normalizedTimeValue);

   if (!Number.isFinite(timeMinutes)) {
      return false;
   }

   return (
      timeMinutes >= bounds.minMinutes
      && timeMinutes <= bounds.maxMinutes
   );
}

export function isArrivalTimeWithinBounds(timeValue, bounds) {
   return isTimeWithinBounds(timeValue, bounds);
}

export function buildDepartureTimeBounds(zooHours = {}) {
   const openMinutes = parseClockTimeMinutes(zooHours.openTime);
   const closeMinutes = parseClockTimeMinutes(zooHours.closeTime);

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
      minScheduleTime: formatMinutesAsScheduleTimeKey(openMinutes),
      maxScheduleTime: formatMinutesAsScheduleTimeKey(closeMinutes),
      minClockTime: formatMinutesAsClockTime(openMinutes),
      maxClockTime: formatMinutesAsClockTime(closeMinutes),
   };
}

export function isDepartureTimeWithinBounds(timeValue, bounds) {
   return isTimeWithinBounds(timeValue, bounds);
}

export function areItineraryScheduleTimesOrdered(arrivalTime, departureTime) {
   const arrivalMinutes = parseClockTimeMinutes(
      typeof arrivalTime === 'string' ? arrivalTime.trim() : ''
   );
   const departureMinutes = parseClockTimeMinutes(
      typeof departureTime === 'string' ? departureTime.trim() : ''
   );

   if (!Number.isFinite(arrivalMinutes) || !Number.isFinite(departureMinutes)) {
      return true;
   }

   return departureMinutes > arrivalMinutes;
}

export function resolveArrivalTimeValidationError(
   timeValue,
   bounds,
   departureTime,
   strings = {}
) {
   if (!isArrivalTimeWithinBounds(timeValue, bounds)) {
      return strings.arrivalTimeInvalid;
   }

   if (!areItineraryScheduleTimesOrdered(timeValue, departureTime)) {
      return strings.arrivalTimeBeforeDepartureInvalid;
   }

   return null;
}

export function resolveDepartureTimeValidationError(
   timeValue,
   bounds,
   arrivalTime,
   strings = {}
) {
   if (!isDepartureTimeWithinBounds(timeValue, bounds)) {
      return strings.departureTimeInvalid;
   }

   if (!areItineraryScheduleTimesOrdered(arrivalTime, timeValue)) {
      return strings.departureTimeAfterArrivalInvalid;
   }

   return null;
}

export function buildHalfHourSlotStarts(openMinutes, closeMinutes) {
   if (
      !Number.isFinite(openMinutes)
      || !Number.isFinite(closeMinutes)
      || closeMinutes <= openMinutes
   ) {
      return [];
   }

   const slotStarts = [];
   const firstHalfHour = Math.ceil(openMinutes / TIMELINE_SLOT_MINUTES) * TIMELINE_SLOT_MINUTES;

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
