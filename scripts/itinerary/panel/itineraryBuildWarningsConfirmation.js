import {
   attractionWithoutAnimalMessage,
   getAttractionsFromWithoutAnimalIssues,
} from './attractionWithoutAnimalConfirmation.js';
import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryOverlayMountEl } from './components/popup.js';
import { el } from './dom.js';
import { getFixedTimeItemsFromLongWaitIssues } from './fixedTimeItemLongWaitConfirmation.js';
import { normalizeText } from './format.js';
import { getPrimaryGuardiansTalkFromUnscheduleIssues } from './guardiansTalkUnscheduleConfirmation.js';
import { getGuardiansTalksFromWithoutAnimalIssues } from './guardiansTalkWithoutAnimalConfirmation.js';
import { getItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { APP_STRINGS } from '../../strings.js';
import { getPrimaryWildEncounterFromUnscheduleIssues } from './wildEncounterUnscheduleConfirmation.js';

function itineraryBuildWarningIssueTypes() {
   const types = getItineraryErrorTypes();

   return [
      types?.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      types?.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
      types?.GUARDIANS_TALK_WITHOUT_ANIMAL,
      types?.ATTRACTION_WITHOUT_ANIMAL,
      types?.FIXED_TIME_ITEM_LONG_WAIT,
   ].filter(Boolean);
}

function buildWarningConfirmFlags() {
   const types = getItineraryErrorTypes();

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
   const talk = getPrimaryGuardiansTalkFromUnscheduleIssues(issues);
   const type = getItineraryErrorTypes()?.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS;

   if (!talk?.talkName || !type) {
      return null;
   }

   const talkName = normalizeText(talk.talkName);
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
   const encounter = getPrimaryWildEncounterFromUnscheduleIssues(issues);
   const type = getItineraryErrorTypes()?.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS;

   if (!encounter?.encounterName || !type) {
      return null;
   }

   const encounterName = normalizeText(encounter.encounterName);
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
   const type = getItineraryErrorTypes()?.GUARDIANS_TALK_WITHOUT_ANIMAL;

   if (!type) {
      return [];
   }

   return getGuardiansTalksFromWithoutAnimalIssues(issues).map((talk) => {
      const talkName = normalizeText(talk.talkName);
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
   const type = getItineraryErrorTypes()?.ATTRACTION_WITHOUT_ANIMAL;

   if (!type) {
      return [];
   }

   return getAttractionsFromWithoutAnimalIssues(issues).map((attraction) => ({
      type,
      title: strings.buildWarningWithoutAnimalTitle,
      message: attractionWithoutAnimalMessage(attraction, { strings }),
   }));
}

function buildFixedTimeItemLongWaitSections(issues, strings) {
   const type = getItineraryErrorTypes()?.FIXED_TIME_ITEM_LONG_WAIT;

   if (!type) {
      return [];
   }

   return getFixedTimeItemsFromLongWaitIssues(issues).map((item) => {
      const itemName = normalizeText(item.itemName);
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

export function getItineraryBuildWarningTypes(issues = []) {
   const warningTypes = itineraryBuildWarningIssueTypes();
   const presentTypes = new Set(
      issues
         .map(issueType)
         .filter((type) => warningTypes.includes(type))
   );

   return warningTypes.filter((type) => presentTypes.has(type));
}

export function buildConfirmedOptionsFromBuildWarnings(issues = []) {
   const confirmFlags = buildWarningConfirmFlags();

   return getItineraryBuildWarningTypes(issues).reduce(
      (flags, type) => ({
         ...flags,
         ...confirmFlags[type],
      }),
      {}
   );
}

export function buildItineraryBuildWarningSections(issues = []) {
   const strings = APP_STRINGS.itinerary.confirmation;

   return BUILD_WARNING_SECTION_LIST_BUILDERS.flatMap((buildSections) => (
      buildSections(issues, strings)
   ));
}

export function hasMultipleItineraryBuildWarnings(issues = []) {
   return buildItineraryBuildWarningSections(issues).length > 1;
}

function createBuildWarningsContent(sections) {
   const content = el('div', 'itin-build-warnings tzg-popup-confirm-body');

   sections.forEach((section) => {
      const moduleEl = el('div', 'itin-build-warning-module');
      moduleEl.append(
         el('div', 'itin-build-warning-module-title', section.title),
         el('div', 'itin-build-warning-module-message', section.message)
      );
      content.appendChild(moduleEl);
   });

   return content;
}

export function showItineraryBuildWarningsConfirmation({
   issues = [],
   onConfirm,
   onCancel,
   mountEl = getItineraryOverlayMountEl() ?? document.body,
} = {}) {
   const sections = buildItineraryBuildWarningSections(issues);

   if (sections.length === 0) {
      onCancel?.();
      return;
   }

   const strings = APP_STRINGS.itinerary.confirmation;

   showItineraryConfirmPopup({
      title: strings.saveIssuesTitle,
      bodyContent: createBuildWarningsContent(sections),
      confirmText: strings.saveIssuesButton,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl,
      onConfirm,
      onCancel,
   });
}
