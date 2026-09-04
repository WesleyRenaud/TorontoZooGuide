import { StoredSelection } from '../base/storedSelection.js';

export const TRANSPORTATION_ITEM_KEY_SEPARATOR = '||';

function addedAsAttractionFromWire(part) {
   const wire = StoredSelection.normalizeStoredString(part);

   if (wire === '1') {
      return true;
   }

   if (wire === '0') {
      return false;
   }

   return null;
}

export class TransportationScheduleItemKey {
   constructor(name, addedAsAttraction) {
      this.name = StoredSelection.normalizeStoredString(name);
      this.addedAsAttraction = addedAsAttraction;
      Object.freeze(this);
   }

   static fromRow(row) {
      const name = StoredSelection.normalizeStoredString(row?.name);

      if (!name || typeof row?.added_as_attraction !== 'boolean') {
         return null;
      }

      return new TransportationScheduleItemKey(name, row.added_as_attraction);
   }

   static fromWire(wire) {
      const parts = StoredSelection.normalizeStoredString(wire).split(
         TRANSPORTATION_ITEM_KEY_SEPARATOR,
         2
      );
      const name = StoredSelection.normalizeStoredString(parts[0]);
      const addedAsAttraction = addedAsAttractionFromWire(parts[1]);

      if (!name || parts.length !== 2 || addedAsAttraction === null) {
         return null;
      }

      return new TransportationScheduleItemKey(name, addedAsAttraction);
   }

   toWire() {
      return [
         this.name,
         this.addedAsAttraction ? '1' : '0',
      ].join(TRANSPORTATION_ITEM_KEY_SEPARATOR);
   }
}
