import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryOverlayMountEl } from './components/popup.js';
import { Format } from './format.js';
import { APP_STRINGS } from '../../strings.js';

const GUARDIANS_TALK_WITHOUT_ANIMAL_ISSUE = 'guardiansTalkWithoutAnimal';

export class GuardiansTalkWithoutAnimalConfirmation {
   static hasGuardiansTalkWithoutAnimalIssue(issues = []) {
      return issues.some(
         (issue) => issue?.type === GUARDIANS_TALK_WITHOUT_ANIMAL_ISSUE
      );

   }

   static getGuardiansTalkNamesFromWithoutAnimalIssues(issues = []) {
      return GuardiansTalkWithoutAnimalConfirmation.getGuardiansTalksFromWithoutAnimalIssues(issues)
         .map((talk) => talk.talkName);

   }

   static getGuardiansTalksFromWithoutAnimalIssues(issues = []) {
      const talksByName = new Map();

      issues
         .filter((issue) => issue?.type === GUARDIANS_TALK_WITHOUT_ANIMAL_ISSUE)
         .flatMap((issue) => issue.items ?? [])
         .forEach((item) => {
            const talkName = Format.normalizeText(item?.name);

            if (!talkName) {
               return;
            }

            const talkTime = Format.formatClockTime(item?.start_time);

            talksByName.set(
               talkName,
               talkTime
                  ? { talkName, talkTime }
                  : { talkName }
            );
         });

      return [...talksByName.values()];

   }

   static getPrimaryGuardiansTalkFromWithoutAnimalIssues(issues = []) {
      const [talk] = GuardiansTalkWithoutAnimalConfirmation.getGuardiansTalksFromWithoutAnimalIssues(issues);

      return talk ?? null;

   }

   static showGuardiansTalkWithoutAnimalConfirmation({
      issues = [],
      onConfirm,
      onCancel,
      mountEl = getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const strings = APP_STRINGS.itinerary.confirmation;
      const talks = GuardiansTalkWithoutAnimalConfirmation.getGuardiansTalksFromWithoutAnimalIssues(issues);

      // Multi-item without-animal warnings use showItineraryBuildWarningsConfirmation.
      if (talks.length !== 1) {
         return;
      }

      const [talk] = talks;
      const talkName = Format.normalizeText(talk.talkName);
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
}
