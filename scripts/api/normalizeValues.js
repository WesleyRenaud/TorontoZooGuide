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

export function asTrimmedStringList(values) {
   return asArray(values)
      .map((value) => String(value ?? '').trim())
      .filter(Boolean);
}

export function asNullableString(value) {
   const stringValue = asTrimmedString(value);
   return stringValue || null;
}

export function asBoolean(value) {
   return value === true;
}

export function normalizeNumber(value) {
   const number = Number(value);
   return Number.isFinite(number) ? number : null;
}
