import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryOverlayMountEl } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

const GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE = 'guardiansTalkWillUnscheduleItems';

export function getGuardiansTalkNamesFromUnscheduleIssues(issues = []) {
   return issues
      .filter((issue) => issue?.type === GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE)
      .flatMap((issue) => (issue.items ?? [])
         .map((item) => (item?.name ?? '').trim())
         .filter(Boolean));
}

export function showGuardiansTalkUnscheduleConfirmation({
   issues = [],
   onConfirm,
   onCancel,
   mountEl = getItineraryOverlayMountEl() ?? document.body,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;
   const talkNames = getGuardiansTalkNamesFromUnscheduleIssues(issues);

   showItineraryConfirmPopup({
      title: strings.guardiansTalkUnscheduleTitle,
      message: strings.guardiansTalkUnscheduleMessage(talkNames.join(', ')),
      confirmText: strings.guardiansTalkUnscheduleConfirm,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl,
      onConfirm,
      onCancel,
   });
}
