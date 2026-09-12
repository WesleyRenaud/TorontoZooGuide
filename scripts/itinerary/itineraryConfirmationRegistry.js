import { AttractionOutsideOperatingHoursFragment } from './panel/attractionOutsideOperatingHoursFragment.js';
import { AttractionWithoutAnimalFragment } from './panel/attractionWithoutAnimalFragment.js';
import { EarlyAdmissionFragment } from './panel/earlyAdmissionFragment.js';
import { FixedTimeItemLongWaitFragment } from './panel/fixedTimeItemLongWaitFragment.js';
import { GuardiansTalkUnscheduleFragment } from './panel/guardiansTalkUnscheduleFragment.js';
import { GuardiansTalkWithoutAnimalFragment } from './panel/guardiansTalkWithoutAnimalFragment.js';
import { ScheduleItemNotOnItineraryFragment } from './panel/scheduleItemNotOnItineraryFragment.js';
import { ShortVisitFragment } from './panel/shortVisitFragment.js';
import { WildEncounterUnscheduleFragment } from './panel/wildEncounterUnscheduleFragment.js';
import { PersistItineraryWarningSuppressor } from './persistItineraryWarningSuppressor.js';
import { ItineraryErrorType } from '../shared/enums/itineraryErrorType.js';

export class ItineraryConfirmationRegistry {
   static SCHEDULE_ITEM_CONFIRMATIONS_BEFORE_WARNINGS = Object.freeze({
      [ItineraryErrorType.ITEM_NOT_ON_ITINERARY]: Object.freeze({
         requiresMethod: 'requiresScheduleItemNotOnItineraryConfirmation',
         showConfirmation: ScheduleItemNotOnItineraryFragment.showScheduleItemNotOnItineraryConfirmation,
         confirmFlag: 'confirmingScheduleItemNotOnItinerary',
         suppressKey: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
         resolveConfirmErrorAsSaveFailed: true,
      }),
      [ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS]: Object.freeze({
         requiresMethod: 'requiresAttractionOutsideOperatingHoursConfirmation',
         showConfirmation: AttractionOutsideOperatingHoursFragment.showAttractionOutsideOperatingHoursConfirmation,
         confirmFlag: 'confirmingAttractionOutsideOperatingHours',
         resolveConfirmErrorAsSaveFailed: true,
      }),
   });

   static SCHEDULE_ITEM_CONFIRMATIONS_AFTER_WARNINGS = Object.freeze({
      [ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS]: Object.freeze({
         requiresMethod: 'requiresGuardiansTalkUnscheduleConfirmation',
         showConfirmation: GuardiansTalkUnscheduleFragment.showGuardiansTalkUnscheduleConfirmation,
         confirmFlag: 'confirmingGuardiansTalkUnschedule',
         confirmationPropsWithIssues: true,
      }),
      [ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL]: Object.freeze({
         requiresMethod: 'requiresGuardiansTalkWithoutAnimalConfirmation',
         showConfirmation: GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation,
         confirmFlag: 'confirmingGuardiansTalkWithoutAnimal',
         confirmationPropsWithIssues: true,
      }),
      [ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT]: Object.freeze({
         requiresMethod: 'requiresFixedTimeItemLongWaitConfirmation',
         showConfirmation: FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation,
         confirmFlag: 'confirmingFixedTimeItemLongWait',
         confirmationPropsWithIssues: true,
      }),
      [ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS]: Object.freeze({
         requiresMethod: 'requiresWildEncounterUnscheduleConfirmation',
         showConfirmation: WildEncounterUnscheduleFragment.showWildEncounterUnscheduleConfirmation,
         confirmFlag: 'confirmingWildEncounterUnschedule',
         confirmationPropsWithIssues: true,
      }),
   });

   static SET_ITINERARY_CONFIRMATIONS = Object.freeze({
      [ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP]: Object.freeze({
         requiresMethod: 'requiresEarlyAdmissionConfirmation',
         showConfirmation: EarlyAdmissionFragment.showEarlyAdmissionConfirmation,
         confirmFlag: 'confirmingEarlyAdmission',
         suppressKey: ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
      }),
      [ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS]: Object.freeze({
         requiresMethod: 'requiresGuardiansTalkUnscheduleConfirmation',
         showConfirmation: GuardiansTalkUnscheduleFragment.showGuardiansTalkUnscheduleConfirmation,
         confirmFlag: 'confirmingGuardiansTalkUnschedule',
      }),
      [ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL]: Object.freeze({
         requiresMethod: 'requiresGuardiansTalkWithoutAnimalConfirmation',
         showConfirmation: GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation,
         confirmFlag: 'confirmingGuardiansTalkWithoutAnimal',
      }),
      [ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL]: Object.freeze({
         requiresMethod: 'requiresAttractionWithoutAnimalConfirmation',
         showConfirmation: AttractionWithoutAnimalFragment.showAttractionWithoutAnimalConfirmation,
         confirmFlag: 'confirmingAttractionWithoutAnimal',
      }),
      [ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT]: Object.freeze({
         requiresMethod: 'requiresFixedTimeItemLongWaitConfirmation',
         showConfirmation: FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation,
         confirmFlag: 'confirmingFixedTimeItemLongWait',
      }),
      [ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS]: Object.freeze({
         requiresMethod: 'requiresWildEncounterUnscheduleConfirmation',
         showConfirmation: WildEncounterUnscheduleFragment.showWildEncounterUnscheduleConfirmation,
         confirmFlag: 'confirmingWildEncounterUnschedule',
      }),
   });

   static TIME_CHANGE_CONFIRMATIONS = Object.freeze({
      [ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP]: Object.freeze({
         requiresMethod: 'requiresEarlyAdmissionConfirmation',
         showConfirmation: EarlyAdmissionFragment.showEarlyAdmissionConfirmation,
         confirmFlag: 'confirmingEarlyAdmission',
         suppressKey: ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
      }),
      [ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE]: Object.freeze({
         requiresMethod: 'requiresShortVisitConfirmation',
         showConfirmation: ShortVisitFragment.showShortVisitConfirmation,
         confirmFlag: 'confirmingShortVisit',
         suppressKey: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
      }),
   });

   static getConfirmationEntry(errorType) {
      return ItineraryConfirmationRegistry.SCHEDULE_ITEM_CONFIRMATIONS_BEFORE_WARNINGS[errorType]
         ?? ItineraryConfirmationRegistry.SCHEDULE_ITEM_CONFIRMATIONS_AFTER_WARNINGS[errorType]
         ?? ItineraryConfirmationRegistry.SET_ITINERARY_CONFIRMATIONS[errorType]
         ?? ItineraryConfirmationRegistry.TIME_CHANGE_CONFIRMATIONS[errorType]
         ?? null;
   }

   static getScheduleItemConfirmationEntries() {
      return [
         ...Object.values(ItineraryConfirmationRegistry.SCHEDULE_ITEM_CONFIRMATIONS_BEFORE_WARNINGS),
         ...Object.values(ItineraryConfirmationRegistry.SCHEDULE_ITEM_CONFIRMATIONS_AFTER_WARNINGS),
      ];
   }

   static getScheduleItemConfirmationEntriesBeforeWarnings() {
      return Object.values(ItineraryConfirmationRegistry.SCHEDULE_ITEM_CONFIRMATIONS_BEFORE_WARNINGS);
   }

   static getScheduleItemConfirmationEntriesAfterWarnings() {
      return Object.values(ItineraryConfirmationRegistry.SCHEDULE_ITEM_CONFIRMATIONS_AFTER_WARNINGS);
   }

   static getSetItineraryConfirmationEntries() {
      return Object.values(ItineraryConfirmationRegistry.SET_ITINERARY_CONFIRMATIONS);
   }

   static getTimeChangeConfirmationEntries() {
      return Object.values(ItineraryConfirmationRegistry.TIME_CHANGE_CONFIRMATIONS);
   }

   static requiresConfirmation(
      errorType,
      expectedErrorType,
      isSuppressed = () => false
   ) {
      const entry = ItineraryConfirmationRegistry.getConfirmationEntry(expectedErrorType);

      if (entry?.suppressKey && isSuppressed(entry.suppressKey)) {
         return false;
      }

      return errorType === expectedErrorType;
   }

   static buildConfirmedOptions(entry) {
      return () => ({
         [entry.confirmFlag]: true,
      });
   }

   static buildConfirmedPayload(entry, payload) {
      return () => ({
         ...payload,
         [entry.confirmFlag]: true,
      });
   }

   static buildBeforeConfirm(entry) {
      if (!entry.suppressKey) {
         return undefined;
      }

      return async ({ doNotShowAgain = false } = {}) => {
         if (doNotShowAgain) {
            await PersistItineraryWarningSuppressor.persistItineraryWarningSuppression(entry.suppressKey);
         }
      };
   }

   static buildTimeChangeConfirmationOptions(entry) {
      return {
         showConfirmation: entry.showConfirmation,
         suppressionType: entry.suppressKey,
         confirmationOptions: {
            [entry.confirmFlag]: true,
         },
      };
   }
}
