import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { DayPlannerSchedule } from './dayPlannerSchedule.js';
import { ScheduledOccurrenceTimeRange } from '../scheduledOccurrenceTimeRange.js';
import { Strings } from '../../strings.js';

function buildTimeFieldLine(value) {
   if (!value) {
      return '';
   }

   return `${Strings.labels.time}: ${value}`;
}

export class RowPresentation {
   static buildImageSrc(...pathParts) {
      const normalizedParts = pathParts
         .map((part) => AssetKeyNormalizer.normalize(part))
         .filter(Boolean);

      if (normalizedParts.length !== pathParts.length) {
         return null;
      }

      return `images/details/${normalizedParts.join('/')}.png`;
   }

   static buildFieldLine(label, value) {
      if (!value) {
         return '';
      }

      return `${label}: ${value}`;
   }

   static buildScheduledTimeFieldLine(item) {
      return buildTimeFieldLine(
         ScheduledOccurrenceTimeRange.buildScheduledOccurrenceTimeRange(item)
      );
   }

   static buildApproximateStartTimeFieldLine(item) {
      const startMinutes = DayPlannerSchedule.parseClockTimeMinutes(item?.start_time);

      if (!Number.isFinite(startMinutes)) {
         return '';
      }

      const roundedMinutes = Math.round(startMinutes / 5) * 5;
      return buildTimeFieldLine(`~${DayPlannerSchedule.formatMinutesAsClockTime(roundedMinutes)}`);
   }

   static buildMetaLines(lines = []) {
      return lines.filter(Boolean);
   }

   static buildLinkRowProps(link) {
      if (!link) {
         return {};
      }

      return {
         linkText: Strings.common.moreInfo,
         onLinkClick: () => window.open(link, '_blank'),
      };
   }

   static buildTitleLinkRowProps(link) {
      if (!link) {
         return {};
      }

      return {
         onNameClick: () => window.open(link, '_blank'),
      };
   }
}
