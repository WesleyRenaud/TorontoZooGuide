import { ValueNormalizer } from '../../../api/valueNormalizer.js';

export class GuardiansTalkScheduleItemKey {
   static GUARDIANS_TALK_ITEM_KEY_SEPARATOR = '||';
   constructor(name = '', startTime = '', endTime = '') {
      this.name = ValueNormalizer.asTrimmedString(name);
      this.startTime = ValueNormalizer.asTrimmedString(startTime);
      this.endTime = ValueNormalizer.asTrimmedString(endTime);
      Object.freeze(this);
   }

   static fromWire(wire) {
      const parts = ValueNormalizer.asTrimmedString(wire).split(
         GuardiansTalkScheduleItemKey.GUARDIANS_TALK_ITEM_KEY_SEPARATOR,
         3
      );
      const name = ValueNormalizer.asTrimmedString(parts[0]);

      if (!name || parts.length < 2) {
         return null;
      }

      const startTime = ValueNormalizer.asTrimmedString(parts[1]);

      if (!startTime) {
         return null;
      }

      if (parts.length > 2) {
         const endTime = ValueNormalizer.asTrimmedString(parts[2]);

         if (!endTime) {
            return null;
         }

         return new GuardiansTalkScheduleItemKey(name, startTime, endTime);
      }

      return new GuardiansTalkScheduleItemKey(name, startTime);
   }

   static fromRow(row) {
      const name = row?.name ?? row?.talk_name ?? '';
      const startTime = ValueNormalizer.asTrimmedString(row?.start_time);
      const endTime = ValueNormalizer.asTrimmedString(row?.end_time);

      if (!ValueNormalizer.asTrimmedString(name) || !startTime) {
         return null;
      }

      return new GuardiansTalkScheduleItemKey(name, startTime, endTime);
   }

   toWire() {
      const parts = [this.name, this.startTime];

      if (this.endTime) {
         parts.push(this.endTime);
      }

      return parts.join(GuardiansTalkScheduleItemKey.GUARDIANS_TALK_ITEM_KEY_SEPARATOR);
   }

   equals(other) {
      return other instanceof GuardiansTalkScheduleItemKey
         && this.name === other.name
         && this.startTime === other.startTime
         && this.endTime === other.endTime;
   }
}
