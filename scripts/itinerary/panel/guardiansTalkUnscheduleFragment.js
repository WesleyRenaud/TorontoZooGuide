import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';
import { Strings } from '../../strings.js';

export class GuardiansTalkUnscheduleFragment {
   static GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE = 'guardiansTalkWillUnscheduleItems';

   static getGuardiansTalkNamesFromUnscheduleIssues(issues = []) {
      return issues
         .filter((issue) => issue?.type === GuardiansTalkUnscheduleFragment.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE)
         .flatMap((issue) => (issue.items ?? [])
            .map((item) => ValueNormalizer.asTrimmedString(item?.name))
            .filter(Boolean));

   }

   static getPrimaryGuardiansTalkFromUnscheduleIssues(issues = []) {
      const [talkName] = GuardiansTalkUnscheduleFragment.getGuardiansTalkNamesFromUnscheduleIssues(issues);

      if (!talkName) {
         return null;
      }

      const talkItem = issues
         .filter((issue) => issue?.type === GuardiansTalkUnscheduleFragment.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE)
         .flatMap((issue) => issue.items ?? [])
         .find((item) => ValueNormalizer.asTrimmedString(item?.name) === talkName);

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
      mountEl = ItineraryPanelFragment.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const talk = GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues(issues);

      if (!talk?.talkName) {
         return;
      }

      const talkName = ValueNormalizer.asTrimmedString(talk.talkName);
      const message = talk.talkTime
         ? Strings.itinerary.confirmation.guardiansTalkRescheduleMessage(
            talkName,
            talk.talkTime
         )
         : Strings.itinerary.confirmation.guardiansTalkRescheduleMessageWithoutTime(talkName);

      ConfirmFragment.showItineraryConfirmPopup({
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
