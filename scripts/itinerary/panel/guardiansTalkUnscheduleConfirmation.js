import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { Format } from './format.js';
import { APP_STRINGS } from '../../strings.js';

const GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE = 'guardiansTalkWillUnscheduleItems';

export class GuardiansTalkUnscheduleConfirmation {
   static getGuardiansTalkNamesFromUnscheduleIssues(issues = []) {
      return issues
         .filter((issue) => issue?.type === GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE)
         .flatMap((issue) => (issue.items ?? [])
            .map((item) => Format.normalizeText(item?.name))
            .filter(Boolean));

   }

   static getPrimaryGuardiansTalkFromUnscheduleIssues(issues = []) {
      const [talkName] = GuardiansTalkUnscheduleConfirmation.getGuardiansTalkNamesFromUnscheduleIssues(issues);

      if (!talkName) {
         return null;
      }

      const talkItem = issues
         .filter((issue) => issue?.type === GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE)
         .flatMap((issue) => issue.items ?? [])
         .find((item) => Format.normalizeText(item?.name) === talkName);

      const talkTime = Format.formatClockTime(talkItem?.start_time);

      if (!talkTime) {
         return { talkName };
      }

      return { talkName, talkTime };

   }

   static showGuardiansTalkUnscheduleConfirmation({
      issues = [],
      onConfirm,
      onCancel,
      mountEl = Popup.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const strings = APP_STRINGS.itinerary.confirmation;
      const talk = GuardiansTalkUnscheduleConfirmation.getPrimaryGuardiansTalkFromUnscheduleIssues(issues);

      if (!talk?.talkName) {
         return;
      }

      const talkName = Format.normalizeText(talk.talkName);
      const message = talk.talkTime
         ? strings.guardiansTalkRescheduleMessage(
            talkName,
            talk.talkTime
         )
         : strings.guardiansTalkRescheduleMessageWithoutTime(talkName);

      ConfirmPopup.showItineraryConfirmPopup({
         title: strings.guardiansTalkRescheduleTitle,
         message,
         confirmText: strings.updatePlanConfirm,
         cancelText: APP_STRINGS.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
