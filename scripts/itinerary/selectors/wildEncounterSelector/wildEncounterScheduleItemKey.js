import { WildEncounterScheduleItemKeyHelper } from './wildEncounterScheduleItemKeyHelper.js';

export class WildEncounterScheduleItemKey {
   static WILD_ENCOUNTER_ITEM_KEY_SEPARATOR = '||';
   constructor(name = '', startTime = '', endTime = '') {
      this.name = String(name ?? '').trim();
      this.startTime = String(startTime ?? '').trim();
      this.endTime = String(endTime ?? '').trim();
      Object.freeze(this);
   }

   static fromWire(wire) {
      const parts = String(wire ?? '').split(WildEncounterScheduleItemKey.WILD_ENCOUNTER_ITEM_KEY_SEPARATOR, 3);
      const name = parts[0]?.trim() ?? '';

      if (!name || parts.length < 2) {
         return null;
      }

      const startTime = WildEncounterScheduleItemKeyHelper.scheduleTimeFromWirePart(parts[1]);

      if (!startTime) {
         return null;
      }

      if (parts.length > 2) {
         const endTime = WildEncounterScheduleItemKeyHelper.scheduleTimeFromWirePart(parts[2]);

         if (!endTime) {
            return null;
         }

         return new WildEncounterScheduleItemKey(name, startTime, endTime);
      }

      return new WildEncounterScheduleItemKey(name, startTime);
   }

   static fromRow(row) {
      const name = row?.name ?? row?.wild_encounter ?? '';
      const startTime = String(row?.start_time ?? '').trim();
      const endTime = String(row?.end_time ?? '').trim();

      if (!String(name).trim() || !startTime) {
         return null;
      }

      return new WildEncounterScheduleItemKey(name, startTime, endTime);
   }

   toWire() {
      const parts = [this.name, this.startTime];

      if (this.endTime) {
         parts.push(this.endTime);
      }

      return parts.join(WildEncounterScheduleItemKey.WILD_ENCOUNTER_ITEM_KEY_SEPARATOR);
   }

   equals(other) {
      return other instanceof WildEncounterScheduleItemKey
         && this.name === other.name
         && this.startTime === other.startTime
         && this.endTime === other.endTime;
   }
}
