import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';
import { Strings } from '../../strings.js';

export class ScheduleItemUnscheduleFragment {
   static getNamesFromUnscheduleIssues(issues = [], config) {
      return issues
         .filter((issue) => issue?.type === config.issueType)
         .flatMap((issue) => (issue.items ?? [])
            .map((item) => ValueNormalizer.asTrimmedString(item?.name))
            .filter(Boolean));

   }

   static getPrimaryFromUnscheduleIssues(issues = [], config) {
      const [name] = ScheduleItemUnscheduleFragment.getNamesFromUnscheduleIssues(issues, config);

      if (!name) {
         return null;
      }

      const item = issues
         .filter((issue) => issue?.type === config.issueType)
         .flatMap((issue) => issue.items ?? [])
         .find((issueItem) => ValueNormalizer.asTrimmedString(issueItem?.name) === name);

      const time = ItineraryItemFormatter.formatClockTime(item?.start_time);

      if (!time) {
         return { [config.nameKey]: name };
      }

      return { [config.nameKey]: name, [config.timeKey]: time };

   }

   static showUnscheduleConfirmation({
      issues = [],
      onConfirm,
      onCancel,
      mountEl = ItineraryPanelFragment.getItineraryOverlayMountEl() ?? document.body,
   } = {}, config) {
      const primary = ScheduleItemUnscheduleFragment.getPrimaryFromUnscheduleIssues(issues, config);

      if (!primary?.[config.nameKey]) {
         return;
      }

      const name = ValueNormalizer.asTrimmedString(primary[config.nameKey]);
      const message = primary[config.timeKey]
         ? config.getMessage(name, primary[config.timeKey])
         : config.getMessageWithoutTime(name);

      ConfirmFragment.showItineraryConfirmPopup({
         title: config.getTitle(),
         message,
         confirmText: Strings.itinerary.confirmation.updatePlanConfirm,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
