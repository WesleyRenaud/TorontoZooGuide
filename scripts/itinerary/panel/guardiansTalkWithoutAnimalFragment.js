import { ScheduleItemWithoutAnimalFragment } from './scheduleItemWithoutAnimalFragment.js';
import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';
import { Strings } from '../../strings.js';

export class GuardiansTalkWithoutAnimalFragment {
   static GUARDIANS_TALK_WITHOUT_ANIMAL_CONFIG = Object.freeze({
      issueType: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      nameKey: 'talkName',
      timeKey: 'talkTime',
      getTitle: () => Strings.itinerary.confirmation.guardiansTalkWithoutAnimalTitle,
      getMessage: (name, time) => Strings.itinerary.confirmation.guardiansTalkWithoutAnimalMessage(
         name,
         time
      ),
      getMessageWithoutTime: (name) => Strings.itinerary.confirmation.guardiansTalkWithoutAnimalMessageWithoutTime(name),
      getBodyMessage: (name, time, strings) => strings.guardiansTalkWithoutAnimalMessage(name, time),
      getBodyMessageWithoutTime: (name, strings) => strings.guardiansTalkWithoutAnimalMessageWithoutTime(name),
      getConfirmPrompt: () => '',
   });

   static hasGuardiansTalkWithoutAnimalIssue(issues = []) {
      return ScheduleItemWithoutAnimalFragment.hasWithoutAnimalIssue(
         issues,
         GuardiansTalkWithoutAnimalFragment.GUARDIANS_TALK_WITHOUT_ANIMAL_CONFIG
      );

   }

   static getGuardiansTalkNamesFromWithoutAnimalIssues(issues = []) {
      return ScheduleItemWithoutAnimalFragment.getNamesFromWithoutAnimalIssues(
         issues,
         GuardiansTalkWithoutAnimalFragment.GUARDIANS_TALK_WITHOUT_ANIMAL_CONFIG
      );

   }

   static getGuardiansTalksFromWithoutAnimalIssues(issues = []) {
      return ScheduleItemWithoutAnimalFragment.getItemsFromWithoutAnimalIssues(
         issues,
         GuardiansTalkWithoutAnimalFragment.GUARDIANS_TALK_WITHOUT_ANIMAL_CONFIG
      );

   }

   static getPrimaryGuardiansTalkFromWithoutAnimalIssues(issues = []) {
      return ScheduleItemWithoutAnimalFragment.getPrimaryFromWithoutAnimalIssues(
         issues,
         GuardiansTalkWithoutAnimalFragment.GUARDIANS_TALK_WITHOUT_ANIMAL_CONFIG
      );

   }

   static showGuardiansTalkWithoutAnimalConfirmation(options = {}) {
      ScheduleItemWithoutAnimalFragment.showWithoutAnimalConfirmation(
         options,
         GuardiansTalkWithoutAnimalFragment.GUARDIANS_TALK_WITHOUT_ANIMAL_CONFIG
      );
   }
}
