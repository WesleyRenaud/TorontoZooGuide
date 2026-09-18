import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';
import { Strings } from '../../strings.js';

export class ItinerarySettingsWarningCopy {
   static WARNING_ORDER = Object.freeze([
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
      ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
   ]);

   static copyForStatus(status, strings = Strings) {
      const confirmation = strings.itinerary.confirmation;

      if (status === ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE) {
         return {
            title: confirmation.shortVisitTitle,
            description: confirmation.shortVisitMessage,
         };
      }

      if (status === ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP) {
         return {
            title: confirmation.earlyAdmissionTitle,
            description: confirmation.earlyAdmissionMessage,
         };
      }

      if (status === ItineraryErrorType.ITEM_NOT_ON_ITINERARY) {
         return {
            title: confirmation.scheduleItemNotOnItineraryTitle,
            description: confirmation.scheduleItemNotOnItineraryMessage,
         };
      }

      return {
         title: status,
         description: '',
      };
   }

   static suppressableStatuses(itineraryConfig = {}) {
      return ItinerarySettingsWarningCopy.sortSuppressableStatuses(
         itineraryConfig.statuses
      ).filter((entry) => entry.isSuppressable);
   }

   static sortSuppressableStatuses(statuses = []) {
      const byStatus = new Map(statuses.map((entry) => [entry.status, entry]));

      return ItinerarySettingsWarningCopy.WARNING_ORDER.flatMap((status) => {
         const entry = byStatus.get(status);
         return entry ? [entry] : [];
      });
   }
}
