import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { FixedTimeItemLongWaitMessageBuilder } from './fixedTimeItemLongWaitMessageBuilder.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';
import { Strings } from '../../strings.js';

export class FixedTimeItemLongWaitFragment {
   static hasFixedTimeItemLongWaitIssue(issues = []) {
      return issues.some(FixedTimeItemLongWaitMessageBuilder.isLongWaitIssue);

   }

   static getFixedTimeItemsFromLongWaitIssues(issues = []) {
      const issueType = FixedTimeItemLongWaitMessageBuilder.fixedTimeItemLongWaitIssueType();

      return FixedTimeItemLongWaitMessageBuilder.longWaitItems(issues)
         .map((item) => {
            const itemName = ValueNormalizer.asTrimmedString(item?.name);

            if (!itemName) {
               return null;
            }

            const itemMeta = FixedTimeItemLongWaitMessageBuilder.resolveItemTypeMeta(item);
            const itemTime = ItineraryItemFormatter.formatClockTime(item.start_time);

            return {
               issueType,
               itemType: itemMeta.itemType,
               typeLabel: itemMeta.typeLabel,
               typePhrase: itemMeta.typePhrase,
               itemName,
               itemTime: itemTime || null,
            };
         })
         .filter(Boolean);

   }

   static showFixedTimeItemLongWaitConfirmation({
      issues = [],
      onConfirm,
      onCancel,
      mountEl = ItineraryPanelFragment.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const items = FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues(issues);

      // Multi-item long waits use showItineraryBuildWarningsConfirmation.
      if (items.length !== 1) {
         return;
      }

      const [item] = items;

      ConfirmFragment.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.fixedTimeItemLongWaitTitle(item.typeLabel),
         message: FixedTimeItemLongWaitMessageBuilder.longWaitConfirmMessage(item, Strings.itinerary.confirmation),
         confirmText: Strings.itinerary.confirmation.saveIssuesButton,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
