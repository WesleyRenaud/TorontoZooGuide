import { StoredSelectionNormalizer } from '../base/storedSelectionNormalizer.js';
import { TransportationScheduleItemKeyHelper } from './transportationScheduleItemKeyHelper.js';

export class TransportationScheduleItemKey {
   static TRANSPORTATION_ITEM_KEY_SEPARATOR = '||';
   constructor(name, addedAsAttraction) {
      this.name = StoredSelectionNormalizer.normalizeStoredString(name);
      this.addedAsAttraction = addedAsAttraction;
      Object.freeze(this);
   }

   static fromRow(row) {
      const name = StoredSelectionNormalizer.normalizeStoredString(row?.name);

      if (!name || typeof row?.added_as_attraction !== 'boolean') {
         return null;
      }

      return new TransportationScheduleItemKey(name, row.added_as_attraction);
   }

   static fromWire(wire) {
      const parts = StoredSelectionNormalizer.normalizeStoredString(wire).split(
         TransportationScheduleItemKey.TRANSPORTATION_ITEM_KEY_SEPARATOR,
         2
      );
      const name = StoredSelectionNormalizer.normalizeStoredString(parts[0]);
      const addedAsAttraction = TransportationScheduleItemKeyHelper.addedAsAttractionFromWire(parts[1]);

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
