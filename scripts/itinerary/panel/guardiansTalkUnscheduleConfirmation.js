import { ConfirmPopup } from './components/confirmPopup.js';
import { ItineraryPanelPopup } from './components/itineraryPanelPopup.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';
import { Strings } from '../../strings.js';

export class GuardiansTalkUnscheduleConfirmation {
   static GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE = 'guardiansTalkWillUnscheduleItems';

   static getGuardiansTalkNamesFromUnscheduleIssues(issues = []) {
      return issues
         .filter((issue) => issue?.type === GuardiansTalkUnscheduleConfirmation.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE)
         .flatMap((issue) => (issue.items ?? [])
            .map((item) => ItineraryItemFormatter.normalizeText(item?.name))
            .filter(Boolean));

   }

   static getPrimaryGuardiansTalkFromUnscheduleIssues(issues = []) {
      const [talkName] = GuardiansTalkUnscheduleConfirmation.getGuardiansTalkNamesFromUnscheduleIssues(issues);

      if (!talkName) {
         return null;
      }

      const talkItem = issues
         .filter((issue) => issue?.type === GuardiansTalkUnscheduleConfirmation.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE)
         .flatMap((issue) => issue.items ?? [])
         .find((item) => ItineraryItemFormatter.normalizeText(item?.name) === talkName);

      const talkTime = ItineraryItemFormatter.formatClockTime(talkItem?.start_time);

      if (!talkTime) {
         return { talkName };
      }

      return { talkName, talkTime };

   }

   static showGuardiansTalkUnscheduleConfirmation({
      issues = [],
      onConfirm,
      onCancel,
      mountEl = ItineraryPanelPopup.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const talk = GuardiansTalkUnscheduleConfirmation.getPrimaryGuardiansTalkFromUnscheduleIssues(issues);

      if (!talk?.talkName) {
         return;
      }

      const talkName = ItineraryItemFormatter.normalizeText(talk.talkName);
      const message = talk.talkTime
         ? Strings.itinerary.confirmation.guardiansTalkRescheduleMessage(
            talkName,
            talk.talkTime
         )
         : Strings.itinerary.confirmation.guardiansTalkRescheduleMessageWithoutTime(talkName);

      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.guardiansTalkRescheduleTitle,
         message,
         confirmText: Strings.itinerary.confirmation.updatePlanConfirm,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
