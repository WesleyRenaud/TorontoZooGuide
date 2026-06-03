import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryOverlayMountEl } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

const WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE = 'wildEncounterWillUnscheduleItems';

export function getWildEncounterNamesFromUnscheduleIssues(issues = []) {
   return issues
      .filter((issue) => issue?.type === WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE)
      .flatMap((issue) => (issue.items ?? [])
         .map((item) => (item?.name ?? '').trim())
         .filter(Boolean));
}

export function showWildEncounterUnscheduleConfirmation({
   issues = [],
   onConfirm,
   onCancel,
   mountEl = getItineraryOverlayMountEl() ?? document.body,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;
   const encounterNames = getWildEncounterNamesFromUnscheduleIssues(issues);

   showItineraryConfirmPopup({
      title: strings.guardiansTalkUnscheduleTitle,
      message: strings.wildEncounterUnscheduleMessage(encounterNames.join(', ')),
      confirmText: strings.guardiansTalkUnscheduleConfirm,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl,
      onConfirm,
      onCancel,
   });
}
