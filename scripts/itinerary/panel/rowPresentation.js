import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import {
   formatMinutesAsClockTime,
   parseClockTimeMinutes,
} from './dayPlannerSchedule.js';
import { buildScheduledOccurrenceTimeRange } from '../scheduledOccurrenceTimeRange.js';
import { APP_STRINGS } from '../../strings.js';

export function buildImageSrc(...pathParts) {
   const normalizedParts = pathParts
      .map((part) => normalizeAssetKey(part))
      .filter(Boolean);

   if (normalizedParts.length !== pathParts.length) {
      return null;
   }

   return `images/details/${normalizedParts.join('/')}.png`;
}

export function buildFieldLine(label, value) {
   if (!value) {
      return '';
   }

   return `${label}: ${value}`;
}

function buildTimeFieldLine(value) {
   if (!value) {
      return '';
   }

   return `Time: ${value}`;
}

export function buildScheduledTimeFieldLine(item) {
   return buildTimeFieldLine(buildScheduledOccurrenceTimeRange(item));
}

export function buildApproximateStartTimeFieldLine(item) {
   const startMinutes = parseClockTimeMinutes(item?.start_time);

   if (!Number.isFinite(startMinutes)) {
      return '';
   }

   const roundedMinutes = Math.round(startMinutes / 5) * 5;
   return buildTimeFieldLine(`~${formatMinutesAsClockTime(roundedMinutes)}`);
}

export function buildMetaLines(lines = []) {
   return lines.filter(Boolean);
}

export function buildLinkRowProps(link) {
   if (!link) {
      return {};
   }

   return {
      linkText: APP_STRINGS.common.moreInfo,
      onLinkClick: () => window.open(link, '_blank'),
   };
}

export function buildTitleLinkRowProps(link) {
   if (!link) {
      return {};
   }

   return {
      onNameClick: () => window.open(link, '_blank'),
   };
}
