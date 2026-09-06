import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { Format } from './format.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItinerarySaveIssueItemType } from '../../shared/enums/itinerarySaveIssueItemType.js';
import { Strings } from '../../strings.js';
import { ScheduleConflictCompatibility } from '../wizard/scheduleConflictCompatibility.js';

function resolveItemTypeMeta(item) {
   if (ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)) {
      return {
         itemType: ItinerarySaveIssueItemType.guardiansTalk,
         typeLabel: Strings.entityLabels.guardiansTalk,
         typePhrase: Strings.entityPhrases.guardiansTalk,
      };
   }

   if (ScheduleConflictCompatibility.isWildEncounterConflictItem(item)) {
      return {
         itemType: ItinerarySaveIssueItemType.wildEncounter,
         typeLabel: Strings.entityLabels.wildEncounter,
         typePhrase: Strings.entityPhrases.wildEncounter,
      };
   }

   throw new Error(
      `Unsupported fixed-time long-wait item type: ${item.item_type}`
   );
}

function fixedTimeItemLongWaitIssueType() {
   return ItineraryErrorTypes.getItineraryErrorTypes()?.FIXED_TIME_ITEM_LONG_WAIT;
}

function isLongWaitIssue(issue) {
   const issueType = fixedTimeItemLongWaitIssueType();
   return Boolean(issueType) && issue.type === issueType;
}

function longWaitItems(issues = []) {
   return issues
      .filter(isLongWaitIssue)
      .flatMap((issue) => issue.items ?? []);
}

function longWaitConfirmMessage(item, strings) {
   const itemName = Format.normalizeText(item.itemName);

   return item.itemTime
      ? strings.fixedTimeItemLongWaitMessage(
         itemName,
         item.itemTime,
         item.typePhrase
      )
      : strings.fixedTimeItemLongWaitMessageWithoutTime(
         itemName,
         item.typePhrase
      );
}

export class FixedTimeItemLongWaitConfirmation {
   static hasFixedTimeItemLongWaitIssue(issues = []) {
      return issues.some(isLongWaitIssue);

   }

   static getFixedTimeItemsFromLongWaitIssues(issues = []) {
      const issueType = fixedTimeItemLongWaitIssueType();

      return longWaitItems(issues)
         .map((item) => {
            const itemName = Format.normalizeText(item?.name);

            if (!itemName) {
               return null;
            }

            const itemMeta = resolveItemTypeMeta(item);
            const itemTime = Format.formatClockTime(item.start_time);

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
      mountEl = Popup.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const strings = Strings.itinerary.confirmation;
      const items = FixedTimeItemLongWaitConfirmation.getFixedTimeItemsFromLongWaitIssues(issues);

      // Multi-item long waits use showItineraryBuildWarningsConfirmation.
      if (items.length !== 1) {
         return;
      }

      const [item] = items;

      ConfirmPopup.showItineraryConfirmPopup({
         title: strings.fixedTimeItemLongWaitTitle(item.typeLabel),
         message: longWaitConfirmMessage(item, strings),
         confirmText: strings.saveIssuesButton,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
