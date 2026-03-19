export function asString(x) {
   if (x == null) return '';
   return typeof x === 'string' ? x : String(x);
}

export function formatISODateLong(iso) {
   if (!iso || typeof iso !== 'string') return '';
   const d = new Date(`${iso}T12:00:00`);
   if (!Number.isFinite(d.getTime())) return '';
   return d.toLocaleDateString(undefined, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
   });
}

export function normalizeAnimal(a) {
   if (typeof a === 'string') return { species: a };
   return a && typeof a === 'object' ? a : { species: asString(a) };
}

export function normalizeAttraction(a) {
   if (typeof a === 'string') return { name: a };
   return a && typeof a === 'object' ? a : { name: asString(a) };
}

export function normalizeTalk(t) {
   if (typeof t === 'string') return { name: t };
   return t && typeof t === 'object' ? t : { name: asString(t) };
}

export function normalizeWild(w) {
   if (typeof w === 'string') return { name: w };
   return w && typeof w === 'object' ? w : { name: asString(w) };
}