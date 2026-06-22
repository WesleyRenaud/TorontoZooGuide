import { normalizeStoredString } from '../base/storedSelection.js';
import {
   buildOccurrenceDetailImageSrc,
   buildOccurrenceSubtitle,
} from '../../scheduledOccurrencePresentation.js';
import { buildScheduledOccurrenceTimeRange } from '../../scheduledOccurrenceTimeRange.js';
import { APP_STRINGS } from '../../../strings.js';

export function getGuardiansTalkName(row) {
   return typeof row?.name === 'string'
      ? row.name
      : '';
}

export function formatGuardiansTalkSearchTitle(name) {
   const trimmed = String(name ?? '').trim();

   return trimmed
      ? `${trimmed} ${APP_STRINGS.entityLabels.guardiansTalk}`
      : APP_STRINGS.entityLabels.guardiansTalk;
}

export function getGuardiansTalkSearchTitle(row) {
   return formatGuardiansTalkSearchTitle(getGuardiansTalkName(row));
}

export function getGuardiansTalkId(row) {
   return getGuardiansTalkName(row).trim();
}

export function getGuardiansTalkLocation(row) {
   return typeof row?.location === 'string'
      ? row.location
      : '';
}

export function getGuardiansTalkScheduleStart(row) {
   return normalizeStoredString(row?.start_time);
}

export function getGuardiansTalkSubtitle(row) {
   return buildOccurrenceSubtitle({
      primaryValue: getGuardiansTalkLocation(row),
      timeRange: buildScheduledOccurrenceTimeRange(row),
   });
}

export function buildGuardiansTalkImageSrc(row) {
   return buildOccurrenceDetailImageSrc(
      'guardians-talks',
      getGuardiansTalkName(row)
   );
}

export function readGuardiansTalkStoredFields(item) {
   return {
      location: normalizeStoredString(item?.location),
      start_time: normalizeStoredString(item?.start_time),
      end_time: normalizeStoredString(item?.end_time),
   };
}

export function buildGuardiansTalkSelectionFields(row) {
   return {
      location: getGuardiansTalkLocation(row),
      start_time: getGuardiansTalkScheduleStart(row),
      end_time: normalizeStoredString(row?.end_time),
   };
}
