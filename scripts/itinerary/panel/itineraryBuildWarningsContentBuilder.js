import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { AttractionWithoutAnimalFragment } from './attractionWithoutAnimalFragment.js';
import { FixedTimeItemLongWaitFragment } from './fixedTimeItemLongWaitFragment.js';
import { GuardiansTalkUnscheduleFragment } from './guardiansTalkUnscheduleFragment.js';
import { GuardiansTalkWithoutAnimalFragment } from './guardiansTalkWithoutAnimalFragment.js';
import { ItineraryPanelHelper } from './itineraryPanelHelper.js';
import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';
import { WildEncounterUnscheduleFragment } from './wildEncounterUnscheduleFragment.js';

export class ItineraryBuildWarningsContentBuilder {
   static BUILD_WARNING_SECTION_LIST_BUILDERS = Object.freeze([
      (issues, strings) => ItineraryBuildWarningsContentBuilder.asSections(
         ItineraryBuildWarningsContentBuilder.buildGuardiansTalkUnscheduleSection(issues, strings)
      ),
      (issues, strings) => ItineraryBuildWarningsContentBuilder.asSections(
         ItineraryBuildWarningsContentBuilder.buildWildEncounterUnscheduleSection(issues, strings)
      ),
      ItineraryBuildWarningsContentBuilder.buildGuardiansTalkWithoutAnimalSections,
      ItineraryBuildWarningsContentBuilder.buildAttractionWithoutAnimalSections,
      ItineraryBuildWarningsContentBuilder.buildFixedTimeItemLongWaitSections,
   ]);

   static itineraryBuildWarningIssueTypes() {
      return [
         ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
         ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
         ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
      ];
   }

   static buildWarningConfirmFlags() {
      return {
         [ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS]: {
            confirmingGuardiansTalkUnschedule: true,
         },
         [ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS]: {
            confirmingWildEncounterUnschedule: true,
         },
         [ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL]: {
            confirmingGuardiansTalkWithoutAnimal: true,
         },
         [ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL]: {
            confirmingAttractionWithoutAnimal: true,
         },
         [ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT]: {
            confirmingFixedTimeItemLongWait: true,
         },
      };
   }

   static issueType(issue) {
      return issue?.type || issue?.code || '';
   }

   static asSections(section) {
      return section == null
         ? []
         : [section];
   }

   static buildGuardiansTalkUnscheduleSection(issues, strings) {
      const talk = GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues(issues);

      if (!talk?.talkName) {
         return null;
      }

      const talkName = ValueNormalizer.asTrimmedString(talk.talkName);
      const message = talk.talkTime
         ? strings.buildWarningScheduleOverlapMessage(talkName, talk.talkTime)
         : strings.buildWarningScheduleOverlapMessageWithoutTime(talkName);

      return {
         type: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         title: strings.buildWarningScheduleOverlapTitle,
         message,
      };
   }

   static buildWildEncounterUnscheduleSection(issues, strings) {
      const encounter = WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues(issues);

      if (!encounter?.encounterName) {
         return null;
      }

      const encounterName = ValueNormalizer.asTrimmedString(encounter.encounterName);
      const message = encounter.encounterTime
         ? strings.buildWarningWildEncounterOverlapMessage(
            encounterName,
            encounter.encounterTime
         )
         : strings.buildWarningWildEncounterOverlapMessageWithoutTime(encounterName);

      return {
         type: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         title: strings.buildWarningScheduleOverlapTitle,
         message,
      };
   }

   static buildGuardiansTalkWithoutAnimalSections(issues, strings) {
      return GuardiansTalkWithoutAnimalFragment.getGuardiansTalksFromWithoutAnimalIssues(issues).map((talk) => {
         const talkName = ValueNormalizer.asTrimmedString(talk.talkName);
         const message = talk.talkTime
            ? strings.buildWarningWithoutAnimalMessage(talkName, talk.talkTime)
            : strings.buildWarningWithoutAnimalMessageWithoutTime(talkName);

         return {
            type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
            title: strings.buildWarningWithoutAnimalTitle,
            message,
         };
      });
   }

   static buildAttractionWithoutAnimalSections(issues, strings) {
      return AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues(issues).map((attraction) => ({
         type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
         title: strings.buildWarningWithoutAnimalTitle,
         message: AttractionWithoutAnimalFragment.attractionWithoutAnimalMessage(attraction, { strings }),
      }));
   }

   static buildFixedTimeItemLongWaitSections(issues, strings) {
      return FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues(issues).map((item) => {
         const itemName = ValueNormalizer.asTrimmedString(item.itemName);
         const message = item.itemTime
            ? strings.buildWarningLongWaitMessage(
               itemName,
               item.itemTime,
               item.typePhrase
            )
            : strings.buildWarningLongWaitMessageWithoutTime(
               itemName,
               item.typePhrase
            );

         return {
            type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
            title: strings.buildWarningLongWaitTitle,
            message,
         };
      });
   }

   static createBuildWarningsContent(sections) {
      const content = ItineraryPanelHelper.el('div', 'itin-build-warnings tzg-popup-confirm-body');

      sections.forEach((section) => {
         const moduleEl = ItineraryPanelHelper.el('div', 'itin-build-warning-module');
         moduleEl.append(
            ItineraryPanelHelper.el('div', 'itin-build-warning-module-title', section.title),
            ItineraryPanelHelper.el('div', 'itin-build-warning-module-message', section.message)
         );
         content.appendChild(moduleEl);
      });

      return content;
   }
}
