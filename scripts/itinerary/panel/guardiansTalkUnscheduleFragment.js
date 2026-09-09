import { ScheduleItemUnscheduleFragment } from './scheduleItemUnscheduleFragment.js';
import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';
import { Strings } from '../../strings.js';

export class GuardiansTalkUnscheduleFragment {
   static GUARDIANS_TALK_UNSCHEDULE_CONFIG = Object.freeze({
      issueType: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      nameKey: 'talkName',
      timeKey: 'talkTime',
      getTitle: () => Strings.itinerary.confirmation.guardiansTalkRescheduleTitle,
      getMessage: (name, time) => Strings.itinerary.confirmation.guardiansTalkRescheduleMessage(
         name,
         time
      ),
      getMessageWithoutTime: (name) => Strings.itinerary.confirmation.guardiansTalkRescheduleMessageWithoutTime(name),
   });

   static getGuardiansTalkNamesFromUnscheduleIssues(issues = []) {
      return ScheduleItemUnscheduleFragment.getNamesFromUnscheduleIssues(
         issues,
         GuardiansTalkUnscheduleFragment.GUARDIANS_TALK_UNSCHEDULE_CONFIG
      );

   }

   static getPrimaryGuardiansTalkFromUnscheduleIssues(issues = []) {
      return ScheduleItemUnscheduleFragment.getPrimaryFromUnscheduleIssues(
         issues,
         GuardiansTalkUnscheduleFragment.GUARDIANS_TALK_UNSCHEDULE_CONFIG
      );

   }

   static showGuardiansTalkUnscheduleConfirmation(options = {}) {
      ScheduleItemUnscheduleFragment.showUnscheduleConfirmation(
         options,
         GuardiansTalkUnscheduleFragment.GUARDIANS_TALK_UNSCHEDULE_CONFIG
      );
   }
}
