import { DetailImageBuilder } from '../../assets/detailImageBuilder.js';
import { DayPlannerScheduleController } from './dayPlannerScheduleController.js';
import { RowPresentationHelper } from './rowPresentationHelper.js';
import { ScheduledOccurrenceTimeModel } from '../scheduledOccurrenceTimeModel.js';
import { StepRounder } from '../../shared/stepRounder.js';
import { Strings } from '../../strings.js';

export class RowPresenter {
   static buildImageSrc(...pathParts) {
      return DetailImageBuilder.buildDetailImageSrcFromParts(pathParts);
   }

   static buildFieldLine(label, value) {
      if (!value) {
         return '';
      }

      return Strings.format.labeledValue(label, value);
   }

   static buildScheduledTimeFieldLine(item) {
      return RowPresentationHelper.buildTimeFieldLine(
         ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange(item)
      );
   }

   static buildApproximateStartTimeFieldLine(item) {
      const startMinutes = DayPlannerScheduleController.parseClockTimeMinutes(item?.start_time);

      if (!Number.isFinite(startMinutes)) {
         return '';
      }

      const roundedMinutes = StepRounder.roundToStep(startMinutes, 5);
      return RowPresentationHelper.buildTimeFieldLine(
         Strings.format.approximate(
            DayPlannerScheduleController.formatMinutesAsClockTime(roundedMinutes)
         )
      );
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
