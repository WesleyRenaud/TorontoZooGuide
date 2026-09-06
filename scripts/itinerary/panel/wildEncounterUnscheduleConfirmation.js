import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { Format } from './format.js';
import { Strings } from '../../strings.js';

const WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE = 'wildEncounterWillUnscheduleItems';

export class WildEncounterUnscheduleConfirmation {
   static getWildEncounterNamesFromUnscheduleIssues(issues = []) {
      return issues
         .filter((issue) => issue?.type === WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE)
         .flatMap((issue) => (issue.items ?? [])
            .map((item) => Format.normalizeText(item?.name))
            .filter(Boolean));

   }

   static getPrimaryWildEncounterFromUnscheduleIssues(issues = []) {
      const [encounterName] = WildEncounterUnscheduleConfirmation.getWildEncounterNamesFromUnscheduleIssues(issues);

      if (!encounterName) {
         return null;
      }

      const encounterItem = issues
         .filter((issue) => issue?.type === WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE)
         .flatMap((issue) => issue.items ?? [])
         .find((item) => Format.normalizeText(item?.name) === encounterName);

      const encounterTime = Format.formatClockTime(encounterItem?.start_time);

      if (!encounterTime) {
         return { encounterName };
      }

      return { encounterName, encounterTime };

   }

   static showWildEncounterUnscheduleConfirmation({
      issues = [],
      onConfirm,
      onCancel,
      mountEl = Popup.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const encounter = WildEncounterUnscheduleConfirmation.getPrimaryWildEncounterFromUnscheduleIssues(issues);

      if (!encounter?.encounterName) {
         return;
      }

      const encounterName = Format.normalizeText(encounter.encounterName);
      const message = encounter.encounterTime
         ? Strings.itinerary.confirmation.wildEncounterRescheduleMessage(
            encounterName,
            encounter.encounterTime
         )
         : Strings.itinerary.confirmation.wildEncounterRescheduleMessageWithoutTime(encounterName);

      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.wildEncounterRescheduleTitle,
         message,
         confirmText: Strings.itinerary.confirmation.updatePlanConfirm,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
