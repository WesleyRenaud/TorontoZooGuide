import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItinerarySaveIssueItemType } from '../../shared/enums/itinerarySaveIssueItemType.js';
import { Strings } from '../../strings.js';
import { ScheduleConflictCompatibility } from '../wizard/scheduleConflictCompatibility.js';

export class FixedTimeItemLongWaitMessageBuilder {
   static resolveItemTypeMeta(item) {
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

   static fixedTimeItemLongWaitIssueType() {
      return ItineraryErrorTypes.getItineraryErrorTypes()?.FIXED_TIME_ITEM_LONG_WAIT;
   }

   static isLongWaitIssue(issue) {
      const issueType = FixedTimeItemLongWaitMessageBuilder.fixedTimeItemLongWaitIssueType();
      return Boolean(issueType) && issue.type === issueType;
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
