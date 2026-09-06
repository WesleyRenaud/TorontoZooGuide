import { AttractionWithoutAnimalConfirmation } from './attractionWithoutAnimalConfirmation.js';
import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { Dom } from './dom.js';
import { FixedTimeItemLongWaitConfirmation } from './fixedTimeItemLongWaitConfirmation.js';
import { Format } from './format.js';
import { GuardiansTalkUnscheduleConfirmation } from './guardiansTalkUnscheduleConfirmation.js';
import { GuardiansTalkWithoutAnimalConfirmation } from './guardiansTalkWithoutAnimalConfirmation.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { Strings } from '../../strings.js';
import { WildEncounterUnscheduleConfirmation } from './wildEncounterUnscheduleConfirmation.js';

function itineraryBuildWarningIssueTypes() {
   const types = ItineraryErrorTypes.getItineraryErrorTypes();

   return [
      types?.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      types?.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
      types?.GUARDIANS_TALK_WITHOUT_ANIMAL,
      types?.ATTRACTION_WITHOUT_ANIMAL,
      types?.FIXED_TIME_ITEM_LONG_WAIT,
   ].filter(Boolean);
}

function buildWarningConfirmFlags() {
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

function issueType(issue) {
   return issue?.type || issue?.code || '';
}

function asSections(section) {
   return section == null
      ? []
      : [section];
}

function buildGuardiansTalkUnscheduleSection(issues, strings) {
   const talk = GuardiansTalkUnscheduleConfirmation.getPrimaryGuardiansTalkFromUnscheduleIssues(issues);
   const type = ItineraryErrorTypes.getItineraryErrorTypes()?.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS;

   if (!talk?.talkName || !type) {
      return null;
   }

   const talkName = Format.normalizeText(talk.talkName);
   const message = talk.talkTime
      ? strings.buildWarningScheduleOverlapMessage(talkName, talk.talkTime)
      : strings.buildWarningScheduleOverlapMessageWithoutTime(talkName);

   return {
      type,
      title: strings.buildWarningScheduleOverlapTitle,
      message,
   };
}

function buildWildEncounterUnscheduleSection(issues, strings) {
   const encounter = WildEncounterUnscheduleConfirmation.getPrimaryWildEncounterFromUnscheduleIssues(issues);
   const type = ItineraryErrorTypes.getItineraryErrorTypes()?.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS;

   if (!encounter?.encounterName || !type) {
      return null;
   }

   const encounterName = Format.normalizeText(encounter.encounterName);
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

function buildGuardiansTalkWithoutAnimalSections(issues, strings) {
   const type = ItineraryErrorTypes.getItineraryErrorTypes()?.GUARDIANS_TALK_WITHOUT_ANIMAL;

   if (!type) {
      return [];
   }

   return GuardiansTalkWithoutAnimalConfirmation.getGuardiansTalksFromWithoutAnimalIssues(issues).map((talk) => {
      const talkName = Format.normalizeText(talk.talkName);
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

function buildAttractionWithoutAnimalSections(issues, strings) {
   const type = ItineraryErrorTypes.getItineraryErrorTypes()?.ATTRACTION_WITHOUT_ANIMAL;

   if (!type) {
      return [];
   }

   return AttractionWithoutAnimalConfirmation.getAttractionsFromWithoutAnimalIssues(issues).map((attraction) => ({
      type,
      title: strings.buildWarningWithoutAnimalTitle,
      message: AttractionWithoutAnimalConfirmation.attractionWithoutAnimalMessage(attraction, { strings }),
   }));
}

function buildFixedTimeItemLongWaitSections(issues, strings) {
   const type = ItineraryErrorTypes.getItineraryErrorTypes()?.FIXED_TIME_ITEM_LONG_WAIT;

   if (!type) {
      return [];
   }

   return FixedTimeItemLongWaitConfirmation.getFixedTimeItemsFromLongWaitIssues(issues).map((item) => {
      const itemName = Format.normalizeText(item.itemName);
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

const BUILD_WARNING_SECTION_LIST_BUILDERS = Object.freeze([
   (issues, strings) => asSections(
      buildGuardiansTalkUnscheduleSection(issues, strings)
   ),
   (issues, strings) => asSections(
      buildWildEncounterUnscheduleSection(issues, strings)
   ),
   buildGuardiansTalkWithoutAnimalSections,
   buildAttractionWithoutAnimalSections,
   buildFixedTimeItemLongWaitSections,
]);

function createBuildWarningsContent(sections) {
   const content = Dom.el('div', 'itin-build-warnings tzg-popup-confirm-body');

   sections.forEach((section) => {
      const moduleEl = Dom.el('div', 'itin-build-warning-module');
      moduleEl.append(
         Dom.el('div', 'itin-build-warning-module-title', section.title),
         Dom.el('div', 'itin-build-warning-module-message', section.message)
      );
      content.appendChild(moduleEl);
   });

   return content;
}

export class ItineraryBuildWarningsConfirmation {
   static getItineraryBuildWarningTypes(issues = []) {
      const warningTypes = itineraryBuildWarningIssueTypes();
      const presentTypes = new Set(
         issues
            .map(issueType)
            .filter((type) => warningTypes.includes(type))
      );

      return warningTypes.filter((type) => presentTypes.has(type));

   }

   static buildConfirmedOptionsFromBuildWarnings(issues = []) {
      const confirmFlags = buildWarningConfirmFlags();

      return ItineraryBuildWarningsConfirmation.getItineraryBuildWarningTypes(issues).reduce(
         (flags, type) => ({
            ...flags,
            ...confirmFlags[type],
         }),
         {}
      );

   }

   static buildItineraryBuildWarningSections(issues = []) {
      const strings = Strings.itinerary.confirmation;

      return BUILD_WARNING_SECTION_LIST_BUILDERS.flatMap((buildSections) => (
         buildSections(issues, strings)
      ));

   }

   static hasMultipleItineraryBuildWarnings(issues = []) {
      return ItineraryBuildWarningsConfirmation.buildItineraryBuildWarningSections(issues).length > 1;

   }

   static showItineraryBuildWarningsConfirmation({
      issues = [],
      onConfirm,
      onCancel,
      mountEl = Popup.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const sections = ItineraryBuildWarningsConfirmation.buildItineraryBuildWarningSections(issues);

      if (sections.length === 0) {
         onCancel?.();
         return;
      }

      const strings = Strings.itinerary.confirmation;

      ConfirmPopup.showItineraryConfirmPopup({
         title: strings.saveIssuesTitle,
         bodyContent: createBuildWarningsContent(sections),
         confirmText: strings.saveIssuesButton,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
