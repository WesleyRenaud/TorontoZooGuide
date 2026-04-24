export function normalizeStoredBoolean(value) {
   return value === true;
}

export function normalizeStoredString(value) {
   return typeof value === 'string'
      ? value.trim()
      : '';
}

export function normalizeStoredLink(value) {
   const link = normalizeStoredString(value);
   return link || null;
}

export function normalizeStoredId(value, fallback = '') {
   return normalizeStoredString(value)
      || normalizeStoredString(fallback);
}

function normalizeStoredSelectionItems(items) {
   return Array.isArray(items)
      ? items
      : [];
}

function migrateStoredSelectionItem(item, {
   fromString = null,
   fromObject = null,
} = {}) {
   if (typeof item === 'string') {
      return typeof fromString === 'function'
         ? fromString(item)
         : null;
   }

   if (item && typeof item === 'object') {
      return typeof fromObject === 'function'
         ? fromObject(item)
         : null;
   }

   return null;
}

export function migrateStoredSelectionItems(items, {
   fromString = null,
   fromObject = null,
} = {}) {
   return normalizeStoredSelectionItems(items)
      .map((item) => migrateStoredSelectionItem(item, {
         fromString,
         fromObject,
      }))
      .filter(Boolean);
}
