import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryOverlayMountEl } from './components/popup.js';
import {
   formatClockTime,
   normalizeText,
} from './format.js';
import { APP_STRINGS } from '../../strings.js';

const GUARDIANS_TALK_WITHOUT_ANIMAL_ISSUE = 'guardiansTalkWithoutAnimal';

export function hasGuardiansTalkWithoutAnimalIssue(issues = []) {
   return issues.some(
      (issue) => issue?.type === GUARDIANS_TALK_WITHOUT_ANIMAL_ISSUE
   );
}

export function getGuardiansTalkNamesFromWithoutAnimalIssues(issues = []) {
   return issues
      .filter((issue) => issue?.type === GUARDIANS_TALK_WITHOUT_ANIMAL_ISSUE)
      .flatMap((issue) => (issue.items ?? [])
         .map((item) => (item?.name ?? '').trim())
         .filter(Boolean));
}

export function getPrimaryGuardiansTalkFromWithoutAnimalIssues(issues = []) {
   const [talkName] = getGuardiansTalkNamesFromWithoutAnimalIssues(issues);

   if (!talkName) {
      return null;
   }

   const talkItem = issues
      .filter((issue) => issue?.type === GUARDIANS_TALK_WITHOUT_ANIMAL_ISSUE)
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

export function showGuardiansTalkWithoutAnimalConfirmation({
   issues = [],
   onConfirm,
   onCancel,
   mountEl = getItineraryOverlayMountEl() ?? document.body,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;
   const talk = getPrimaryGuardiansTalkFromWithoutAnimalIssues(issues);

   if (!talk?.talkName) {
      return;
   }

   const talkName = normalizeText(talk.talkName);
   const message = talk.talkTime
      ? strings.guardiansTalkWithoutAnimalMessage(talkName, talk.talkTime)
      : strings.guardiansTalkWithoutAnimalMessageWithoutTime(talkName);

   showItineraryConfirmPopup({
      title: strings.guardiansTalkWithoutAnimalTitle,
      message,
      confirmText: strings.saveIssuesButton,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl,
      onConfirm,
      onCancel,
   });
}
