import { WildEncounterScheduleItemKey } from '../selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';

export class ScheduleItemSearchRowTagger {
   static itineraryWildEncounterId(encounter) {
      return WildEncounterScheduleItemKey.fromRow(encounter)?.toWire() ?? null;
   }

   static tagRows(rows = [], scheduleItemKind) {
      return rows.map((row) => ({
         ...row,
         scheduleItemKind,
      }));
   }

   static tagAnimalRows(rows = []) {
      return ScheduleItemSearchRowTagger.tagRows(rows, ScheduleItemKind.ANIMAL.itemType);
   }

   static tagAttractionRows(rows = []) {
      return ScheduleItemSearchRowTagger.tagRows(rows, ScheduleItemKind.ATTRACTION.itemType);
   }

   static tagTransportationRows(rows = []) {
      return ScheduleItemSearchRowTagger.tagRows(rows, ScheduleItemKind.TRANSPORTATION.itemType);
   }

   static tagGuardiansTalkRows(rows = []) {
      return ScheduleItemSearchRowTagger.tagRows(rows, ScheduleItemKind.GUARDIANS_TALK.itemType);
   }

   static tagWildEncounterRows(rows = []) {
      return ScheduleItemSearchRowTagger.tagRows(rows, ScheduleItemKind.WILD_ENCOUNTER.itemType);
   }
}
