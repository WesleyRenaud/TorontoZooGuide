export function asArray(value) {
   return Array.isArray(value) ? value : [];
}

export function asObject(value) {
   return value && typeof value === 'object'
      ? value
      : {};
}

export function asTrimmedString(value) {
   return typeof value === 'string'
      ? value.trim()
      : '';
}

export function asNullableString(value) {
   const stringValue = asTrimmedString(value);
   return stringValue || null;
}

export function asBoolean(value) {
   return value === true;
}
