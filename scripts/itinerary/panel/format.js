function asObject(value) {
   return value && typeof value === 'object'
      ? value
      : {};
}

function normalizeText(value) {
   return typeof value === 'string'
      ? value.trim()
      : '';
}

function normalizeOptionalText(value) {
   const text = normalizeText(value);
   return text || null;
}

function normalizeNumber(value) {
   const number = Number(value);
   return Number.isFinite(number) ? number : null;
}

export function formatISODateLong(iso) {
   if (!iso || typeof iso !== 'string') return '';

   const date = new Date(`${iso}T12:00:00`);

   if (!Number.isFinite(date.getTime())) return '';

   return date.toLocaleDateString(undefined, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
   });
}

export function normalizeAnimal(value) {
   const source = asObject(value);

   return {
      ...source,
      species: normalizeText(source.species),
      exhibit: normalizeText(source.exhibit),
      link: normalizeOptionalText(source.link),
      removalReason: normalizeOptionalText(source.removalReason),
      likelihoodBefore: normalizeNumber(source.likelihoodBefore),
      likelihoodAfter: normalizeNumber(source.likelihoodAfter),
   };
}

export function normalizeAttraction(value) {
   const source = asObject(value);

   return {
      ...source,
      name: normalizeText(source.name),
      subtitle: normalizeText(source.subtitle),
      location: normalizeText(source.location),
      price: normalizeText(source.price),
      infoLink: normalizeOptionalText(source.infoLink ?? source.info_link),
      removalReason: normalizeOptionalText(source.removalReason),
   };
}

export function normalizeTalk(value) {
   const source = asObject(value);

   return {
      ...source,
      name: normalizeText(source.name),
      location: normalizeText(source.location),
      time_of_day: normalizeText(source.time_of_day),
      link: normalizeOptionalText(source.link),
      removalReason: normalizeOptionalText(source.removalReason),
   };
}

export function normalizeWild(value) {
   const source = asObject(value);

   return {
      ...source,
      name: normalizeText(source.name),
      meeting_spot: normalizeText(source.meeting_spot),
      time_of_day: normalizeText(source.time_of_day),
      link: normalizeOptionalText(source.link),
      removalReason: normalizeOptionalText(source.removalReason),
   };
}
