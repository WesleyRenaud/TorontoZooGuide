import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryOverlayMountEl } from './components/popup.js';
import { Format } from './format.js';
import { APP_STRINGS } from '../../strings.js';

const WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE = 'wildEncounterWillUnscheduleItems';

export function getWildEncounterNamesFromUnscheduleIssues(issues = []) {
   return issues
      .filter((issue) => issue?.type === WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE)
      .flatMap((issue) => (issue.items ?? [])
         .map((item) => Format.normalizeText(item?.name))
         .filter(Boolean));
}

export function getPrimaryWildEncounterFromUnscheduleIssues(issues = []) {
   const [encounterName] = getWildEncounterNamesFromUnscheduleIssues(issues);

   if (!encounterName) {
      return null;
   }

   const encounterItem = issues
      .filter((issue) => issue?.type === WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE)
      .flatMap((issue) => issue.items ?? [])
      .find((item) => Format.normalizeText(item?.name) === encounterName);

   const encounterTime = Format.formatClockTime(encounterItem?.start_time);

   if (!encounterTime) {
      return { encounterName };
   }

   return { encounterName, encounterTime };
}

export function showWildEncounterUnscheduleConfirmation({
   issues = [],
   onConfirm,
   onCancel,
   mountEl = getItineraryOverlayMountEl() ?? document.body,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;
   const encounter = getPrimaryWildEncounterFromUnscheduleIssues(issues);

   if (!encounter?.encounterName) {
      return;
   }

   const encounterName = Format.normalizeText(encounter.encounterName);
   const message = encounter.encounterTime
      ? strings.wildEncounterRescheduleMessage(
         encounterName,
         encounter.encounterTime
      )
      : strings.wildEncounterRescheduleMessageWithoutTime(encounterName);

   showItineraryConfirmPopup({
      title: strings.wildEncounterRescheduleTitle,
      message,
      confirmText: strings.updatePlanConfirm,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl,
      onConfirm,
      onCancel,
   });
}
