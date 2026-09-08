import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { TransportationScheduleItemKeyHelpers } from './transportationScheduleItemKeyHelpers.js';

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
      const name = ValueNormalizer.asTrimmedString(parts[0]);
      const addedAsAttraction = TransportationScheduleItemKeyHelpers.addedAsAttractionFromWire(parts[1]);

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
