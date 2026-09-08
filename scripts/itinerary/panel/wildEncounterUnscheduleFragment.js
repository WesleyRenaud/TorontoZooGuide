import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';
import { Strings } from '../../strings.js';

export class WildEncounterUnscheduleFragment {
   static WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE = 'wildEncounterWillUnscheduleItems';

   static getWildEncounterNamesFromUnscheduleIssues(issues = []) {
      return issues
         .filter((issue) => issue?.type === WildEncounterUnscheduleFragment.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE)
         .flatMap((issue) => (issue.items ?? [])
            .map((item) => ValueNormalizer.asTrimmedString(item?.name))
            .filter(Boolean));

   }

   static getPrimaryWildEncounterFromUnscheduleIssues(issues = []) {
      const [encounterName] = WildEncounterUnscheduleFragment.getWildEncounterNamesFromUnscheduleIssues(issues);

      if (!encounterName) {
         return null;
      }

      const encounterItem = issues
         .filter((issue) => issue?.type === WildEncounterUnscheduleFragment.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE)
         .flatMap((issue) => issue.items ?? [])
         .find((item) => ValueNormalizer.asTrimmedString(item?.name) === encounterName);

      const encounterTime = ItineraryItemFormatter.formatClockTime(encounterItem?.start_time);

      if (!encounterTime) {
         return { encounterName };
      }

      return { encounterName, encounterTime };

   }

   static showWildEncounterUnscheduleConfirmation({
      issues = [],
      onConfirm,
      onCancel,
      mountEl = ItineraryPanelFragment.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const encounter = WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues(issues);

      if (!encounter?.encounterName) {
         return;
      }

      const encounterName = ValueNormalizer.asTrimmedString(encounter.encounterName);
      const message = encounter.encounterTime
         ? Strings.itinerary.confirmation.wildEncounterRescheduleMessage(
            encounterName,
            encounter.encounterTime
         )
         : Strings.itinerary.confirmation.wildEncounterRescheduleMessageWithoutTime(encounterName);

      ConfirmFragment.showItineraryConfirmPopup({
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
