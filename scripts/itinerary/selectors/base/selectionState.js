import {
   loadArray,
   saveArray,
} from '../../draftStorage.js';

function identity(items) {
   return items;
}

function cloneSelectedItems(items) {
   return items.slice();
}

function loadSelectedItems(storageKey, migrateSelected = identity) {
   return migrateSelected(loadArray(storageKey));
}

function persistSelectedItems(storageKey, selectedItems) {
   saveArray(storageKey, selectedItems);
}

function getSelectedIndexById(selectedItems, id) {
   return selectedItems.findIndex((item) => item?.id === id);
}

function buildSelectionItem(row, {
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

export function createSelectorSelectionState({
   storageKey,
   migrateSelected = identity,
   getId,
   makeSelection = (row) => ({ id: getId(row) }),
} = {}) {
   let selectedItems = loadSelectedItems(storageKey, migrateSelected);

   function getSelectedSnapshot() {
      return cloneSelectedItems(selectedItems);
   }

   function replaceSelectedItems(nextSelectedItems) {
      selectedItems = nextSelectedItems;
      persistSelectedItems(storageKey, selectedItems);
      return getSelectedSnapshot();
   }

   function reload() {
      selectedItems = loadSelectedItems(storageKey, migrateSelected);
      return getSelectedSnapshot();
   }

   function isSelected(id) {
      return getSelectedIndexById(selectedItems, id) !== -1;
   }

   function toggleRow(row) {
      const selectionItem = buildSelectionItem(row, {
         getId,
         makeSelection,
      });

      if (!selectionItem) {
         return getSelectedSnapshot();
      }

      const selectedIndex = getSelectedIndexById(
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
