import { SelectionStateHelpers } from './selectionStateHelpers.js';

export class SelectionState {
   static createSelectorSelectionState({
      storageKey,
      migrateSelected = SelectionStateHelpers.identity,
      getId,
      makeSelection = (row) => ({ id: getId(row) }),
   } = {}) {
      let selectedItems = SelectionStateHelpers.loadSelectedItems(storageKey, migrateSelected);

      function getSelectedSnapshot() {
         return SelectionStateHelpers.cloneSelectedItems(selectedItems);
      }

      function replaceSelectedItems(nextSelectedItems) {
         selectedItems = nextSelectedItems;
         SelectionStateHelpers.persistSelectedItems(storageKey, selectedItems);
         return getSelectedSnapshot();
      }

      function reload() {
         selectedItems = SelectionStateHelpers.loadSelectedItems(storageKey, migrateSelected);
         return getSelectedSnapshot();
      }

      function isSelected(id) {
         return SelectionStateHelpers.getSelectedIndexById(selectedItems, id) !== -1;
      }

      function toggleRow(row) {
         const selectionItem = SelectionStateHelpers.buildSelectionItem(row, {
            getId,
            makeSelection,
         });

         if (!selectionItem) {
            return getSelectedSnapshot();
         }

         const selectedIndex = SelectionStateHelpers.getSelectedIndexById(
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
