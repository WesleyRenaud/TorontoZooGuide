import { ConfirmPopup } from './components/confirmPopup.js';
import { ItineraryPanelPopup } from './components/itineraryPanelPopup.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';
import { Strings } from '../../strings.js';

export class GuardiansTalkWithoutAnimalConfirmation {
   static GUARDIANS_TALK_WITHOUT_ANIMAL_ISSUE = 'guardiansTalkWithoutAnimal';

   static hasGuardiansTalkWithoutAnimalIssue(issues = []) {
      return issues.some(
         (issue) => issue?.type === GuardiansTalkWithoutAnimalConfirmation.GUARDIANS_TALK_WITHOUT_ANIMAL_ISSUE
      );

   }

   static getGuardiansTalkNamesFromWithoutAnimalIssues(issues = []) {
      return GuardiansTalkWithoutAnimalConfirmation.getGuardiansTalksFromWithoutAnimalIssues(issues)
         .map((talk) => talk.talkName);

   }

   static getGuardiansTalksFromWithoutAnimalIssues(issues = []) {
      const talksByName = new Map();

      issues
         .filter((issue) => issue?.type === GuardiansTalkWithoutAnimalConfirmation.GUARDIANS_TALK_WITHOUT_ANIMAL_ISSUE)
         .flatMap((issue) => issue.items ?? [])
         .forEach((item) => {
            const talkName = ItineraryItemFormatter.normalizeText(item?.name);

            if (!talkName) {
               return;
            }

            const talkTime = ItineraryItemFormatter.formatClockTime(item?.start_time);

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
      mountEl = ItineraryPanelPopup.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const talks = GuardiansTalkWithoutAnimalConfirmation.getGuardiansTalksFromWithoutAnimalIssues(issues);

      // Multi-item without-animal warnings use showItineraryBuildWarningsConfirmation.
      if (talks.length !== 1) {
         return;
      }

      const [talk] = talks;
      const talkName = ItineraryItemFormatter.normalizeText(talk.talkName);
      const message = talk.talkTime
         ? Strings.itinerary.confirmation.guardiansTalkWithoutAnimalMessage(talkName, talk.talkTime)
         : Strings.itinerary.confirmation.guardiansTalkWithoutAnimalMessageWithoutTime(talkName);

      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.guardiansTalkWithoutAnimalTitle,
         message,
         confirmText: Strings.itinerary.confirmation.saveIssuesButton,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
