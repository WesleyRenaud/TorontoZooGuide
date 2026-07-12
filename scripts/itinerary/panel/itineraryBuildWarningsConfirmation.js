import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryOverlayMountEl } from './components/popup.js';
import { el } from './dom.js';
import { normalizeText } from './format.js';
import { getPrimaryGuardiansTalkFromLongWaitIssues } from './guardiansTalkLongWaitConfirmation.js';
import { getPrimaryGuardiansTalkFromUnscheduleIssues } from './guardiansTalkUnscheduleConfirmation.js';
import { getPrimaryGuardiansTalkFromWithoutAnimalIssues } from './guardiansTalkWithoutAnimalConfirmation.js';
import { APP_STRINGS } from '../../strings.js';
import { getPrimaryWildEncounterFromUnscheduleIssues } from './wildEncounterUnscheduleConfirmation.js';

export const ITINERARY_BUILD_WARNING_ISSUE_TYPES = Object.freeze([
   'guardiansTalkWillUnscheduleItems',
   'wildEncounterWillUnscheduleItems',
   'guardiansTalkWithoutAnimal',
   'guardiansTalkLongWait',
]);

const BUILD_WARNING_CONFIRM_FLAGS = Object.freeze({
   guardiansTalkWillUnscheduleItems: {
      confirmingGuardiansTalkUnschedule: true,
   },
   wildEncounterWillUnscheduleItems: {
      confirmingWildEncounterUnschedule: true,
   },
   guardiansTalkWithoutAnimal: {
      confirmingGuardiansTalkWithoutAnimal: true,
   },
   guardiansTalkLongWait: {
      confirmingGuardiansTalkLongWait: true,
   },
});

function issueType(issue) {
   return issue?.type || issue?.code || '';
}

function buildGuardiansTalkUnscheduleSection(issues, strings) {
   const talk = getPrimaryGuardiansTalkFromUnscheduleIssues(issues);

   if (!talk?.talkName) {
      return null;
   }

   const talkName = normalizeText(talk.talkName);
   const message = talk.talkTime
      ? strings.buildWarningScheduleOverlapMessage(talkName, talk.talkTime)
      : strings.buildWarningScheduleOverlapMessageWithoutTime(talkName);

   return {
      type: 'guardiansTalkWillUnscheduleItems',
      title: strings.buildWarningScheduleOverlapTitle,
      message,
   };
}

function buildWildEncounterUnscheduleSection(issues, strings) {
   const encounter = getPrimaryWildEncounterFromUnscheduleIssues(issues);

   if (!encounter?.encounterName) {
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
      type: 'wildEncounterWillUnscheduleItems',
      title: strings.buildWarningScheduleOverlapTitle,
      message,
   };
}

function buildGuardiansTalkWithoutAnimalSection(issues, strings) {
   const talk = getPrimaryGuardiansTalkFromWithoutAnimalIssues(issues);

   if (!talk?.talkName) {
      return null;
   }

   const talkName = normalizeText(talk.talkName);
   const message = talk.talkTime
      ? strings.buildWarningWithoutAnimalMessage(talkName, talk.talkTime)
      : strings.buildWarningWithoutAnimalMessageWithoutTime(talkName);

   return {
      type: 'guardiansTalkWithoutAnimal',
      title: strings.buildWarningWithoutAnimalTitle,
      message,
   };
}

function buildGuardiansTalkLongWaitSection(issues, strings) {
   const talk = getPrimaryGuardiansTalkFromLongWaitIssues(issues);

   if (!talk?.talkName) {
      return null;
   }

   const talkName = normalizeText(talk.talkName);
   const message = talk.talkTime
      ? strings.buildWarningLongWaitMessage(talkName, talk.talkTime)
      : strings.buildWarningLongWaitMessageWithoutTime(talkName);

   return {
      type: 'guardiansTalkLongWait',
      title: strings.buildWarningLongWaitTitle,
      message,
   };
}

const BUILD_WARNING_SECTION_BUILDERS = Object.freeze([
   buildGuardiansTalkUnscheduleSection,
   buildWildEncounterUnscheduleSection,
   buildGuardiansTalkWithoutAnimalSection,
   buildGuardiansTalkLongWaitSection,
]);

export function getItineraryBuildWarningTypes(issues = []) {
   const presentTypes = new Set(
      issues
         .map(issueType)
         .filter((type) => ITINERARY_BUILD_WARNING_ISSUE_TYPES.includes(type))
   );

   return ITINERARY_BUILD_WARNING_ISSUE_TYPES.filter(
      (type) => presentTypes.has(type)
   );
}

export function hasMultipleItineraryBuildWarnings(issues = []) {
   return getItineraryBuildWarningTypes(issues).length > 1;
}

export function buildConfirmedOptionsFromBuildWarnings(issues = []) {
   return getItineraryBuildWarningTypes(issues).reduce(
      (flags, type) => ({
         ...flags,
         ...BUILD_WARNING_CONFIRM_FLAGS[type],
      }),
      {}
   );
}

export function buildItineraryBuildWarningSections(issues = []) {
   const strings = APP_STRINGS.itinerary.confirmation;

   return BUILD_WARNING_SECTION_BUILDERS
      .map((buildSection) => buildSection(issues, strings))
      .filter(Boolean);
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
