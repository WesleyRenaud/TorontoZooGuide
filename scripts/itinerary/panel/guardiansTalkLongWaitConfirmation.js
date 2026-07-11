import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryOverlayMountEl } from './components/popup.js';
import {
   formatClockTime,
   normalizeText,
} from './format.js';
import { APP_STRINGS } from '../../strings.js';

const GUARDIANS_TALK_LONG_WAIT_ISSUE = 'guardiansTalkLongWait';

export function hasGuardiansTalkLongWaitIssue(issues = []) {
   return issues.some(
      (issue) => issue?.type === GUARDIANS_TALK_LONG_WAIT_ISSUE
   );
}

export function getGuardiansTalkNamesFromLongWaitIssues(issues = []) {
   return issues
      .filter((issue) => issue?.type === GUARDIANS_TALK_LONG_WAIT_ISSUE)
      .flatMap((issue) => (issue.items ?? [])
         .map((item) => (item?.name ?? '').trim())
         .filter(Boolean));
}

export function getPrimaryGuardiansTalkFromLongWaitIssues(issues = []) {
   const [talkName] = getGuardiansTalkNamesFromLongWaitIssues(issues);

   if (!talkName) {
      return null;
   }

   const talkItem = issues
      .filter((issue) => issue?.type === GUARDIANS_TALK_LONG_WAIT_ISSUE)
      .flatMap((issue) => issue.items ?? [])
      .find((item) => (item?.name ?? '').trim() === talkName);

   const talkTime = formatClockTime(
      talkItem?.start_time ?? talkItem?.startTime
   );

   if (!talkTime) {
      return { talkName };
   }

   return { talkName, talkTime };
}

export function showGuardiansTalkLongWaitConfirmation({
   issues = [],
   onConfirm,
   onCancel,
   mountEl = getItineraryOverlayMountEl() ?? document.body,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;
   const talk = getPrimaryGuardiansTalkFromLongWaitIssues(issues);

   if (!talk?.talkName) {
      return;
   }

   const talkName = normalizeText(talk.talkName);
   const message = talk.talkTime
      ? strings.guardiansTalkLongWaitMessage(talkName, talk.talkTime)
      : strings.guardiansTalkLongWaitMessageWithoutTime(talkName);

   showItineraryConfirmPopup({
      title: strings.guardiansTalkLongWaitTitle,
      message,
      confirmText: strings.saveIssuesButton,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl,
      onConfirm,
      onCancel,
   });
}
