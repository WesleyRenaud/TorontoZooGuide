function safeParse(raw, fallback) {
   try {
      return JSON.parse(raw);
   } catch {
      return fallback;
   }
}

function defaultMigrate(arr) {
   return Array.isArray(arr) ? arr : [];
}

function loadSelected(storageKey, migrate = defaultMigrate) {
   const raw = localStorage.getItem(storageKey);
   const arr = safeParse(raw || '[]', []);
   return migrate(arr);
}

function saveSelected(storageKey, selected) {
   localStorage.setItem(storageKey, JSON.stringify(selected));
}

export function createSelectorSelectionState({
   storageKey,
   migrateSelected = defaultMigrate,
   getId,
   makeSelection,
} = {}) {
   let selected = loadSelected(storageKey, migrateSelected);

   function reload() {
      selected = loadSelected(storageKey, migrateSelected);
      return selected;
   }

   function isSelected(id) {
      return selected.some((item) => item?.id === id);
   }

   function toggleRow(row) {
      const id = getId(row);

      if (!id) {
         return selected.slice();
      }

      if (isSelected(id)) {
         selected = selected.filter((item) => item?.id !== id);
      } else {
         const next = makeSelection(row) || {};
         selected = [
            ...selected,
            {
               ...next,
               id: next.id || id,
            },
         ];
      }

      saveSelected(storageKey, selected);
      return selected.slice();
   }

   function getSelectedSnapshot() {
      return selected.slice();
   }

   return {
      reload,
      isSelected,
      toggleRow,
      getSelectedSnapshot,
   };
}
