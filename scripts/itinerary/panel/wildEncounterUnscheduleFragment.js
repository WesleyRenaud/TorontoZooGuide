import { ScheduleItemUnscheduleFragment } from './scheduleItemUnscheduleFragment.js';
import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';
import { Strings } from '../../strings.js';

export class WildEncounterUnscheduleFragment {
   static WILD_ENCOUNTER_UNSCHEDULE_CONFIG = Object.freeze({
      issueType: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
      nameKey: 'encounterName',
      timeKey: 'encounterTime',
      getTitle: () => Strings.itinerary.confirmation.wildEncounterRescheduleTitle,
      getMessage: (name, time) => Strings.itinerary.confirmation.wildEncounterRescheduleMessage(
         name,
         time
      ),
      getMessageWithoutTime: (name) => Strings.itinerary.confirmation.wildEncounterRescheduleMessageWithoutTime(name),
   });

   static getWildEncounterNamesFromUnscheduleIssues(issues = []) {
      return ScheduleItemUnscheduleFragment.getNamesFromUnscheduleIssues(
         issues,
         WildEncounterUnscheduleFragment.WILD_ENCOUNTER_UNSCHEDULE_CONFIG
      );

   }

   static getPrimaryWildEncounterFromUnscheduleIssues(issues = []) {
      return ScheduleItemUnscheduleFragment.getPrimaryFromUnscheduleIssues(
         issues,
         WildEncounterUnscheduleFragment.WILD_ENCOUNTER_UNSCHEDULE_CONFIG
      );

   }

   static showWildEncounterUnscheduleConfirmation(options = {}) {
      ScheduleItemUnscheduleFragment.showUnscheduleConfirmation(
         options,
         WildEncounterUnscheduleFragment.WILD_ENCOUNTER_UNSCHEDULE_CONFIG
      );
   }
}
