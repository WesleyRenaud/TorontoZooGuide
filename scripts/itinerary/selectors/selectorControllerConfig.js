export function defaultMigrateSelected(items) {
   return items;
}

export function buildSelectionFingerprint(items = []) {
   return items
      .map((item) => String(item.id).trim())
      .filter(Boolean)
      .sort((left, right) => left.localeCompare(right, undefined, { sensitivity: 'base' }))
      .join('\0');
}

export function validateSelectorConfig({
   storageKey,
   getId,
   extractRows,
} = {}) {
   if (!storageKey) {
      throw new Error('createItinerarySelectorController: storageKey is required');
   }

   if (typeof getId !== 'function') {
      throw new Error('createItinerarySelectorController: getId(row) is required');
   }

   if (typeof extractRows !== 'function') {
      throw new Error('createItinerarySelectorController: extractRows(response) is required');
   }
}
