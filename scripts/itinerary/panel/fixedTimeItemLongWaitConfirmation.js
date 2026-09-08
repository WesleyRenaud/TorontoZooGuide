import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ConfirmPopup } from './components/confirmPopup.js';
import { ItineraryPanelPopup } from './components/itineraryPanelPopup.js';
import { FixedTimeItemLongWaitMessageBuilder } from './fixedTimeItemLongWaitMessageBuilder.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';
import { Strings } from '../../strings.js';

export class FixedTimeItemLongWaitConfirmation {
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
      mountEl = ItineraryPanelPopup.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const items = FixedTimeItemLongWaitConfirmation.getFixedTimeItemsFromLongWaitIssues(issues);

      // Multi-item long waits use showItineraryBuildWarningsConfirmation.
      if (items.length !== 1) {
         return;
      }

      const [item] = items;

      ConfirmPopup.showItineraryConfirmPopup({
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
