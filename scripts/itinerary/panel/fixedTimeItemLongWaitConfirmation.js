import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryOverlayMountEl } from './components/popup.js';
import { el } from './dom.js';
import {
   formatClockTime,
   normalizeText,
} from './format.js';
import { getItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItinerarySaveIssueItemType } from '../../shared/enums/itinerarySaveIssueItemType.js';
import { APP_STRINGS } from '../../strings.js';
import {
   isGuardiansTalkConflictItem,
   isWildEncounterConflictItem,
} from '../wizard/scheduleConflictCompatibility.js';

function resolveItemTypeMeta(item) {
   if (isGuardiansTalkConflictItem(item)) {
      return {
         itemType: ItinerarySaveIssueItemType.guardiansTalk,
         typeLabel: APP_STRINGS.entityLabels.guardiansTalk,
         typePhrase: APP_STRINGS.entityPhrases.guardiansTalk,
      };
   }

   if (isWildEncounterConflictItem(item)) {
      return {
         itemType: ItinerarySaveIssueItemType.wildEncounter,
         typeLabel: APP_STRINGS.entityLabels.wildEncounter,
         typePhrase: APP_STRINGS.entityPhrases.wildEncounter,
      };
   }

   throw new Error(
      `Unsupported fixed-time long-wait item type: ${item.item_type}`
   );
}

function fixedTimeItemLongWaitIssueType() {
   return getItineraryErrorTypes()?.FIXED_TIME_ITEM_LONG_WAIT;
}

function isLongWaitIssue(issue) {
   const issueType = fixedTimeItemLongWaitIssueType();
   return Boolean(issueType) && issue.type === issueType;
}

export function hasFixedTimeItemLongWaitIssue(issues = []) {
   return issues.some(isLongWaitIssue);
}

function longWaitItems(issues = []) {
   return issues
      .filter(isLongWaitIssue)
      .flatMap((issue) => issue.items ?? []);
}

export function getFixedTimeItemsFromLongWaitIssues(issues = []) {
   const issueType = fixedTimeItemLongWaitIssueType();

   return longWaitItems(issues)
      .filter((item) => item.name?.trim())
      .map((item) => {
         const itemMeta = resolveItemTypeMeta(item);
         const itemTime = formatClockTime(item.start_time);

         return {
            issueType,
            itemType: itemMeta.itemType,
            typeLabel: itemMeta.typeLabel,
            typePhrase: itemMeta.typePhrase,
            itemName: item.name.trim(),
            itemTime: itemTime || null,
         };
      });
}

function longWaitConfirmMessage(item, strings) {
   const itemName = normalizeText(item.itemName);

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

function createLongWaitConfirmBody(items, strings) {
   const content = el('div', 'itin-build-warnings tzg-popup-confirm-body');

   items.forEach((item) => {
      const moduleEl = el('div', 'itin-build-warning-module');
      moduleEl.append(
         el(
            'div',
            'itin-build-warning-module-title',
            strings.fixedTimeItemLongWaitTitle(item.typeLabel)
         ),
         el(
            'div',
            'itin-build-warning-module-message',
            longWaitConfirmMessage(item, strings)
         )
      );
      content.appendChild(moduleEl);
   });

   return content;
}

export function showFixedTimeItemLongWaitConfirmation({
   issues = [],
   onConfirm,
   onCancel,
   mountEl = getItineraryOverlayMountEl() ?? document.body,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;
   const items = getFixedTimeItemsFromLongWaitIssues(issues);

   if (items.length === 0) {
      return;
   }

   if (items.length === 1) {
      const [item] = items;

      showItineraryConfirmPopup({
         title: strings.fixedTimeItemLongWaitTitle(item.typeLabel),
         message: longWaitConfirmMessage(item, strings),
         confirmText: strings.saveIssuesButton,
         cancelText: APP_STRINGS.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
      return;
   }

   showItineraryConfirmPopup({
      title: strings.saveIssuesTitle,
      bodyContent: createLongWaitConfirmBody(items, strings),
      confirmText: strings.saveIssuesButton,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl,
      onConfirm,
      onCancel,
   });
}
