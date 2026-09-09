import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ScheduleItemKeySeparator } from '../scheduleItemKeySeparator.js';
import { Position } from '../../shared/enums/position.js';

export class TimedScheduleItemKey {
   static NAME_FIELDS = ['name'];

   constructor(name = '', startTime = '', endTime = '') {
      this.name = ValueNormalizer.asTrimmedString(name);
      this.startTime = ValueNormalizer.asTrimmedString(startTime);
      this.endTime = ValueNormalizer.asTrimmedString(endTime);
      Object.freeze(this);
   }

   static fromWire(wire) {
      const parts = ValueNormalizer.asTrimmedString(wire).split(
         ScheduleItemKeySeparator.VALUE,
         3
      );
      const name = ValueNormalizer.asTrimmedString(parts[Position.FIRST]);

      if (!name || parts.length < 2) {
         return null;
      }

      const startTime = ValueNormalizer.asTrimmedString(parts[Position.SECOND]);

      if (!startTime) {
         return null;
      }

      if (parts.length > 2) {
         const endTime = ValueNormalizer.asTrimmedString(parts[Position.THIRD]);

         if (!endTime) {
            return null;
         }

         return new this(name, startTime, endTime);
      }

      return new this(name, startTime);
   }

   static fromRow(row) {
      const name = this.NAME_FIELDS
         .map(field => row?.[field])
         .find(value => value !== undefined && value !== null) ?? '';
      const startTime = ValueNormalizer.asTrimmedString(row?.start_time);
      const endTime = ValueNormalizer.asTrimmedString(row?.end_time);

      if (!ValueNormalizer.asTrimmedString(name) || !startTime) {
         return null;
      }

      return new this(name, startTime, endTime);
   }

   toWire() {
      const parts = [this.name, this.startTime];

      if (this.endTime) {
         parts.push(this.endTime);
      }

      return parts.join(ScheduleItemKeySeparator.VALUE);
   }

   equals(other) {
      return other?.constructor === this.constructor
         && this.name === other.name
         && this.startTime === other.startTime
         && this.endTime === other.endTime;
   }
}
