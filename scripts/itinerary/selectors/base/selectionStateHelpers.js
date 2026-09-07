import { DraftStorage } from '../../draftStorage.js';

export class SelectionStateHelpers {
   static identity(items) {
      return items;
   }

   static cloneSelectedItems(items) {
      return items.slice();
   }

   static loadSelectedItems(storageKey, migrateSelected = identity) {
      return migrateSelected(DraftStorage.loadArray(storageKey));
   }

   static persistSelectedItems(storageKey, selectedItems) {
      DraftStorage.saveArray(storageKey, selectedItems);
   }

   static getSelectedIndexById(selectedItems, id) {
      return selectedItems.findIndex((item) => item?.id === id);
   }

   static buildSelectionItem(row, {
      getId,
      makeSelection,
   } = {}) {
      const id = getId(row);

      if (!id) {
         return null;
      }

      const selection = makeSelection(row);
      const selectionItem = selection && typeof selection === 'object'
         ? selection
         : {};

      return {
         ...selectionItem,
         id: selectionItem.id || id,
      };
   }
}
