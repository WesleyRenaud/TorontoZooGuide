import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { Position } from '../../../shared/enums/position.js';
import { TransportationScheduleItemKeyHelper } from './transportationScheduleItemKeyHelper.js';

export class TransportationScheduleItemKey {
   static TRANSPORTATION_ITEM_KEY_SEPARATOR = '||';
   constructor(name, addedAsAttraction) {
      this.name = ValueNormalizer.asTrimmedString(name);
      this.addedAsAttraction = addedAsAttraction;
      Object.freeze(this);
   }

   static fromRow(row) {
      const name = ValueNormalizer.asTrimmedString(row?.name);

      if (!name || typeof row?.added_as_attraction !== 'boolean') {
         return null;
      }

      return new TransportationScheduleItemKey(name, row.added_as_attraction);
   }

   static fromWire(wire) {
      const parts = ValueNormalizer.asTrimmedString(wire).split(
         TransportationScheduleItemKey.TRANSPORTATION_ITEM_KEY_SEPARATOR,
         2
      );
      const name = ValueNormalizer.asTrimmedString(parts[Position.FIRST]);
      const addedAsAttraction = TransportationScheduleItemKeyHelper.addedAsAttractionFromWire(
         parts[Position.SECOND]
      );

      if (!name || parts.length !== 2 || addedAsAttraction === null) {
         return null;
      }

      return new TransportationScheduleItemKey(name, addedAsAttraction);
   }

   toWire() {
      return [
         this.name,
         this.addedAsAttraction ? '1' : '0',
      ].join(TransportationScheduleItemKey.TRANSPORTATION_ITEM_KEY_SEPARATOR);
   }
}
