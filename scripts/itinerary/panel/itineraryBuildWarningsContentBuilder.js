import { AttractionWithoutAnimalFragment } from './attractionWithoutAnimalFragment.js';
import { FixedTimeItemLongWaitFragment } from './fixedTimeItemLongWaitFragment.js';
import { GuardiansTalkUnscheduleFragment } from './guardiansTalkUnscheduleFragment.js';
import { GuardiansTalkWithoutAnimalFragment } from './guardiansTalkWithoutAnimalFragment.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';
import { ItineraryPanelHelper } from './itineraryPanelHelper.js';
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
      const types = ItineraryErrorTypes.getItineraryErrorTypes();

      return [
         types?.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         types?.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         types?.GUARDIANS_TALK_WITHOUT_ANIMAL,
         types?.ATTRACTION_WITHOUT_ANIMAL,
         types?.FIXED_TIME_ITEM_LONG_WAIT,
      ].filter(Boolean);
   }

   static buildWarningConfirmFlags() {
      const types = ItineraryErrorTypes.getItineraryErrorTypes();

      return Object.fromEntries(
         [
            [
               types?.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
               { confirmingGuardiansTalkUnschedule: true },
            ],
            [
               types?.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
               { confirmingWildEncounterUnschedule: true },
            ],
            [
               types?.GUARDIANS_TALK_WITHOUT_ANIMAL,
               { confirmingGuardiansTalkWithoutAnimal: true },
            ],
            [
               types?.ATTRACTION_WITHOUT_ANIMAL,
               { confirmingAttractionWithoutAnimal: true },
            ],
            [
               types?.FIXED_TIME_ITEM_LONG_WAIT,
               { confirmingFixedTimeItemLongWait: true },
            ],
         ].filter(([type]) => Boolean(type))
      );
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
      const type = ItineraryErrorTypes.getItineraryErrorTypes()?.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS;

      if (!talk?.talkName || !type) {
         return null;
      }

      const talkName = ItineraryItemFormatter.normalizeText(talk.talkName);
      const message = talk.talkTime
         ? strings.buildWarningScheduleOverlapMessage(talkName, talk.talkTime)
         : strings.buildWarningScheduleOverlapMessageWithoutTime(talkName);

      return {
         type,
         title: strings.buildWarningScheduleOverlapTitle,
         message,
      };
   }

   static buildWildEncounterUnscheduleSection(issues, strings) {
      const encounter = WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues(issues);
      const type = ItineraryErrorTypes.getItineraryErrorTypes()?.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS;

      if (!encounter?.encounterName || !type) {
         return null;
      }

      const encounterName = ItineraryItemFormatter.normalizeText(encounter.encounterName);
      const message = encounter.encounterTime
         ? strings.buildWarningWildEncounterOverlapMessage(
            encounterName,
            encounter.encounterTime
         )
         : strings.buildWarningWildEncounterOverlapMessageWithoutTime(encounterName);

      return {
         type,
         title: strings.buildWarningScheduleOverlapTitle,
         message,
      };
   }

   static buildGuardiansTalkWithoutAnimalSections(issues, strings) {
      const type = ItineraryErrorTypes.getItineraryErrorTypes()?.GUARDIANS_TALK_WITHOUT_ANIMAL;

      if (!type) {
         return [];
      }

      return GuardiansTalkWithoutAnimalFragment.getGuardiansTalksFromWithoutAnimalIssues(issues).map((talk) => {
         const talkName = ItineraryItemFormatter.normalizeText(talk.talkName);
         const message = talk.talkTime
            ? strings.buildWarningWithoutAnimalMessage(talkName, talk.talkTime)
            : strings.buildWarningWithoutAnimalMessageWithoutTime(talkName);

         return {
            type,
            title: strings.buildWarningWithoutAnimalTitle,
            message,
         };
      });
   }

   static buildAttractionWithoutAnimalSections(issues, strings) {
      const type = ItineraryErrorTypes.getItineraryErrorTypes()?.ATTRACTION_WITHOUT_ANIMAL;

      if (!type) {
         return [];
      }

      return AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues(issues).map((attraction) => ({
         type,
         title: strings.buildWarningWithoutAnimalTitle,
         message: AttractionWithoutAnimalFragment.attractionWithoutAnimalMessage(attraction, { strings }),
      }));
   }

   static buildFixedTimeItemLongWaitSections(issues, strings) {
      const type = ItineraryErrorTypes.getItineraryErrorTypes()?.FIXED_TIME_ITEM_LONG_WAIT;

      if (!type) {
         return [];
      }

      return FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues(issues).map((item) => {
         const itemName = ItineraryItemFormatter.normalizeText(item.itemName);
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
            type,
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
