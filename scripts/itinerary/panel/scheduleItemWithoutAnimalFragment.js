import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';
import { Strings } from '../../strings.js';

export class ScheduleItemWithoutAnimalFragment {
   static hasWithoutAnimalIssue(issues = [], config) {
      return issues.some(
         (issue) => issue?.type === config.issueType
      );

   }

   static getItemsFromWithoutAnimalIssues(issues = [], config) {
      const itemsByName = new Map();

      issues
         .filter((issue) => issue?.type === config.issueType)
         .flatMap((issue) => issue.items ?? [])
         .forEach((item) => {
            const name = ValueNormalizer.asTrimmedString(item?.name);

            if (!name) {
               return;
            }

            const time = ItineraryItemFormatter.formatClockTime(item?.start_time);

            itemsByName.set(
               name,
               time
                  ? { [config.nameKey]: name, [config.timeKey]: time }
                  : { [config.nameKey]: name }
            );
         });

      return [...itemsByName.values()];

   }

   static getNamesFromWithoutAnimalIssues(issues = [], config) {
      return ScheduleItemWithoutAnimalFragment.getItemsFromWithoutAnimalIssues(issues, config)
         .map((item) => item[config.nameKey]);

   }

   static getPrimaryFromWithoutAnimalIssues(issues = [], config) {
      const [item] = ScheduleItemWithoutAnimalFragment.getItemsFromWithoutAnimalIssues(issues, config);

      return item ?? null;

   }

   static withoutAnimalMessage(item, config, {
      includeConfirmPrompt = false,
      strings = Strings.itinerary.confirmation,
   } = {}) {
      const name = ValueNormalizer.asTrimmedString(item[config.nameKey]);
      const body = item[config.timeKey]
         ? config.getBodyMessage(name, item[config.timeKey], strings)
         : config.getBodyMessageWithoutTime(name, strings);

      if (!includeConfirmPrompt) {
         return body;
      }

      return `${body}${config.getConfirmPrompt(strings)}`;

   }

   static showWithoutAnimalConfirmation({
      issues = [],
      onConfirm,
      onCancel,
      mountEl = ItineraryPanelFragment.getItineraryOverlayMountEl() ?? document.body,
   } = {}, config) {
      const items = ScheduleItemWithoutAnimalFragment.getItemsFromWithoutAnimalIssues(issues, config);

      // Multi-item without-animal warnings use showItineraryBuildWarningsConfirmation.
      if (items.length !== 1) {
         return;
      }

      const [item] = items;
      const name = ValueNormalizer.asTrimmedString(item[config.nameKey]);
      const message = item[config.timeKey]
         ? config.getMessage(name, item[config.timeKey])
         : config.getMessageWithoutTime(name);

      ConfirmFragment.showItineraryConfirmPopup({
         title: config.getTitle(),
         message,
         confirmText: Strings.itinerary.confirmation.saveIssuesButton,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
