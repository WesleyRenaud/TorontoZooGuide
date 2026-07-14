import {
   normalizeStoredLink,
   normalizeStoredString,
} from '../base/storedSelection.js';
import {
   buildOccurrenceDetailImageSrc,
   buildOccurrenceSubtitle,
   formatOccurrenceSearchTitle,
   formatOccurrenceTitleSuffix,
} from '../../scheduledOccurrencePresentation.js';
import { buildScheduledOccurrenceTimeRange } from '../../scheduledOccurrenceTimeRange.js';
import { WildEncounterScheduleItemKey } from './scheduleItemKey.js';
import { APP_STRINGS } from '../../../strings.js';

export function getWildEncounterName(row) {
   return typeof row?.name === 'string'
      ? row.name
      : '';
}

export function getWildEncounterKey(row) {
   return WildEncounterScheduleItemKey.fromRow(row);
}

export function getWildEncounterId(row) {
   return getWildEncounterKey(row).toWire();
}

export function formatWildEncounterTitleSuffix(name) {
   return formatOccurrenceTitleSuffix(
      name,
      APP_STRINGS.entityLabels.wildEncounter
   );
}

export function formatWildEncounterSearchTitle(name) {
   return formatOccurrenceSearchTitle(
      name,
      APP_STRINGS.entityLabels.wildEncounter
   );
}

export function getWildEncounterSearchTitle(row) {
   return formatWildEncounterSearchTitle(getWildEncounterName(row));
}

export function getWildEncounterTitleSuffix(row) {
   return formatWildEncounterTitleSuffix(getWildEncounterName(row));
}

export function getWildEncounterMeetingSpot(row) {
   return typeof row?.meeting_spot === 'string'
      ? row.meeting_spot
      : '';
}

export function getWildEncounterLink(row) {
   return normalizeStoredLink(row?.link);
}

export function getWildEncounterScheduleStart(row) {
   return normalizeStoredString(row?.start_time);
}

export function getWildEncounterSubtitle(row) {
   return buildOccurrenceSubtitle({
      primaryValue: getWildEncounterMeetingSpot(row),
      timeRange: buildScheduledOccurrenceTimeRange(row),
   });
}

export function buildWildEncounterImageSrc(row) {
   return buildOccurrenceDetailImageSrc(
      'wild-encounters',
      getWildEncounterName(row)
   );
}

export function readWildEncounterStoredFields(item) {
   return {
      meeting_spot: normalizeStoredString(item?.meeting_spot),
      start_time: normalizeStoredString(item?.start_time),
      end_time: normalizeStoredString(item?.end_time),
   };
}

export function buildWildEncounterSelectionFields(row) {
   return {
      meeting_spot: getWildEncounterMeetingSpot(row),
      start_time: getWildEncounterScheduleStart(row),
      end_time: normalizeStoredString(row?.end_time),
   };
}
