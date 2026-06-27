export const WILD_ENCOUNTER_ITEM_KEY_SEPARATOR = '||';

function scheduleTimeFromWirePart(part) {
   return String(part ?? '').trim();
}

export class WildEncounterScheduleItemKey {
   constructor(name = '', startTime = '', endTime = '') {
      this.name = String(name ?? '').trim();
      this.startTime = String(startTime ?? '').trim();
      this.endTime = String(endTime ?? '').trim();
      Object.freeze(this);
   }

   static fromWire(wire) {
      const parts = String(wire ?? '').split(WILD_ENCOUNTER_ITEM_KEY_SEPARATOR, 3);
      const name = parts[0]?.trim() ?? '';

      if (!name || parts.length < 2) {
         return null;
      }

      const startTime = scheduleTimeFromWirePart(parts[1]);

      if (!startTime) {
         return null;
      }

      if (parts.length > 2) {
         const endTime = scheduleTimeFromWirePart(parts[2]);

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

      return parts.join(WILD_ENCOUNTER_ITEM_KEY_SEPARATOR);
   }

   equals(other) {
      return other instanceof WildEncounterScheduleItemKey
         && this.name === other.name
         && this.startTime === other.startTime
         && this.endTime === other.endTime;
   }
}
