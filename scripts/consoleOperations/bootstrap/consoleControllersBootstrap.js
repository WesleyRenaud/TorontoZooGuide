import { ConsoleControllersBootstrapHelpers } from './consoleControllersBootstrapHelpers.js';
import { GuardiansTalkLocationFilter } from '../guardiansTalks/controllers/guardiansTalkLocationFilter.js';
import { GuardiansTalkOccurrenceFilter } from '../guardiansTalks/controllers/guardiansTalkOccurrenceFilter.js';
import { GuardiansTalkScheduleTimesFilter } from '../guardiansTalks/controllers/guardiansTalkScheduleTimesFilter.js';
import { WildEncounterOccurrenceFilter } from '../wildEncounters/controllers/wildEncounterOccurrenceFilter.js';
import { WildEncounterScheduleTimesFilter } from '../wildEncounters/controllers/wildEncounterScheduleTimesFilter.js';

export class ConsoleControllersBootstrap {
   static createConsoleSpecialControllers({ guardiansTalks, wildEncounters }) {
      return {
         guardiansTalkScheduleLocationFilterController:
            GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
               locationEl: guardiansTalks.schedule.locationEl,
               talkNameEl: guardiansTalks.schedule.talkNameEl,
            }),
         endGuardiansTalkScheduleLocationFilterController:
            GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
               locationEl: guardiansTalks.endSchedule.locationEl,
               talkNameEl: guardiansTalks.endSchedule.talkNameEl,
            }),
         addGuardiansTalkOccurrenceLocationFilterController:
            GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
               locationEl: guardiansTalks.addOccurrence.locationEl,
               talkNameEl: guardiansTalks.addOccurrence.talkNameEl,
            }),
         cancelGuardiansTalkOccurrenceLocationFilterController:
            GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
               locationEl: guardiansTalks.cancelOccurrence.locationEl,
               talkNameEl: guardiansTalks.cancelOccurrence.talkNameEl,
            }),
         cancelGuardiansTalkOccurrenceFilterController:
            GuardiansTalkOccurrenceFilter.createGuardiansTalkOccurrenceFilterController({
               locationEl: guardiansTalks.cancelOccurrence.locationEl,
               talkNameEl: guardiansTalks.cancelOccurrence.talkNameEl,
               dateEl: guardiansTalks.cancelOccurrence.dateEl,
               timesEl: guardiansTalks.cancelOccurrence.timesEl,
            }),
         guardiansTalkScheduleTimesFilterController:
            GuardiansTalkScheduleTimesFilter.createGuardiansTalkScheduleTimesFilterController({
               locationEl: guardiansTalks.endSchedule.locationEl,
               talkNameEl: guardiansTalks.endSchedule.talkNameEl,
               timesEl: guardiansTalks.endSchedule.timesEl,
            }),
         wildEncounterOccurrenceFilterController:
            WildEncounterOccurrenceFilter.createWildEncounterOccurrenceFilterController({
               wildEncounterEl: wildEncounters.cancelOccurrence.wildEncounterEl,
               dateEl: wildEncounters.cancelOccurrence.dateEl,
               timesEl: wildEncounters.cancelOccurrence.timesEl,
            }),
         wildEncounterScheduleTimesFilterController:
            WildEncounterScheduleTimesFilter.createWildEncounterScheduleTimesFilterController({
               wildEncounterEl: wildEncounters.endSchedule.wildEncounterEl,
               timesEl: wildEncounters.endSchedule.timesEl,
            }),
      };
   }

   static wireConsoleOperationControllers({
   refs,
   activatePanel,
   guardiansTalkScheduleLocationFilterController,
   endGuardiansTalkScheduleLocationFilterController,
   addGuardiansTalkOccurrenceLocationFilterController,
   cancelGuardiansTalkOccurrenceLocationFilterController,
   cancelGuardiansTalkOccurrenceFilterController,
   guardiansTalkScheduleTimesFilterController,
   wildEncounterOccurrenceFilterController,
   wildEncounterScheduleTimesFilterController,
}) {
      ConsoleControllersBootstrapHelpers.initAnimalSpeciesAutocompletes(refs.animals);

      ConsoleControllersBootstrapHelpers.wireControllerBindings({
         refs,
         activatePanel,
         specialControllers: {
            guardiansTalkScheduleLocationFilterController,
            endGuardiansTalkScheduleLocationFilterController,
            addGuardiansTalkOccurrenceLocationFilterController,
            cancelGuardiansTalkOccurrenceLocationFilterController,
            cancelGuardiansTalkOccurrenceFilterController,
            guardiansTalkScheduleTimesFilterController,
            wildEncounterOccurrenceFilterController,
            wildEncounterScheduleTimesFilterController,
         },
      });
   }
}
