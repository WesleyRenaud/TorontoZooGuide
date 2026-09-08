import { SelectionStateHelper } from './selectionStateHelper.js';

export class SelectionStore {
   static createSelectorSelectionState({
      storageKey,
      migrateSelected = SelectionStateHelper.identity,
      getId,
      makeSelection = (row) => ({ id: getId(row) }),
   } = {}) {
      let selectedItems = SelectionStateHelper.loadSelectedItems(storageKey, migrateSelected);

      function getSelectedSnapshot() {
         return SelectionStateHelper.cloneSelectedItems(selectedItems);
      }

      function replaceSelectedItems(nextSelectedItems) {
         selectedItems = nextSelectedItems;
         SelectionStateHelper.persistSelectedItems(storageKey, selectedItems);
         return getSelectedSnapshot();
      }

      function reload() {
         selectedItems = SelectionStateHelper.loadSelectedItems(storageKey, migrateSelected);
         return getSelectedSnapshot();
      }

      function isSelected(id) {
         return SelectionStateHelper.getSelectedIndexById(selectedItems, id) !== -1;
      }

      function toggleRow(row) {
         const selectionItem = SelectionStateHelper.buildSelectionItem(row, {
            getId,
            makeSelection,
         });

         if (!selectionItem) {
            return getSelectedSnapshot();
         }

         const selectedIndex = SelectionStateHelper.getSelectedIndexById(
            selectedItems,
            selectionItem.id
         );

         if (selectedIndex === -1) {
            return replaceSelectedItems([
               ...selectedItems,
               selectionItem,
            ]);
         }

         return replaceSelectedItems(
            selectedItems.filter((_, index) => index !== selectedIndex)
         );
      }

      return {
         reload,
         isSelected,
         toggleRow,
         getSelectedSnapshot,
      };
   }
}
