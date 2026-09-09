import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../shared/enums/itinerarySaveIssueItemType.js';
import { Strings } from '../../strings.js';
import { ScheduleConflictChecker } from '../wizard/scheduleConflictChecker.js';

export class FixedTimeItemLongWaitMessageBuilder {
   static resolveItemTypeMeta(item) {
      if (ScheduleConflictChecker.isGuardiansTalkConflictItem(item)) {
         return {
            itemType: ItinerarySaveIssueItemType.GUARDIANS_TALK,
            typeLabel: Strings.entityLabels.guardiansTalk,
            typePhrase: Strings.entityPhrases.guardiansTalk,
         };
      }

      if (ScheduleConflictChecker.isWildEncounterConflictItem(item)) {
         return {
            itemType: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
            typeLabel: Strings.entityLabels.wildEncounter,
            typePhrase: Strings.entityPhrases.wildEncounter,
         };
      }

      throw new Error(
         `Unsupported fixed-time long-wait item type: ${item.item_type}`
      );
   }

   static fixedTimeItemLongWaitIssueType() {
      return ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT;
   }

   static isLongWaitIssue(issue) {
      return issue.type === ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT;
   }

   static longWaitItems(issues = []) {
      return issues
         .filter(FixedTimeItemLongWaitMessageBuilder.isLongWaitIssue)
         .flatMap((issue) => issue.items ?? []);
   }

   static longWaitConfirmMessage(item, strings) {
      const itemName = ValueNormalizer.asTrimmedString(item.itemName);

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
}
