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
