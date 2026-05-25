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

function normalizeMaximumDuration(value) {
   const maximumDuration = normalizeNumber(value);
   return maximumDuration && maximumDuration > 0 ? maximumDuration : null;
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

export function formatISODateFull(iso, fallback = '') {
   if (!iso || typeof iso !== 'string') return fallback;

   const dateParts = iso.trim().match(/^(\d{4})-(\d{2})-(\d{2})$/);

   if (!dateParts) {
      return iso.trim() || fallback;
   }

   const date = new Date(
      Number(dateParts[1]),
      Number(dateParts[2]) - 1,
      Number(dateParts[3])
   );

   return new Intl.DateTimeFormat('en-CA', {
      weekday: 'long',
      month: 'long',
      day: 'numeric',
      year: 'numeric',
   }).format(date);
}

export function formatClockTime(timeValue, fallback = '') {
   if (typeof timeValue !== 'string' || !timeValue.trim()) {
      return fallback;
   }

   const timeParts = timeValue.trim().match(/^(\d{1,2}):(\d{2})$/);

   if (!timeParts) {
      return timeValue.trim();
   }

   const hours = Number(timeParts[1]);
   const minutes = Number(timeParts[2]);
   const period = hours >= 12 ? 'PM' : 'AM';
   const displayHours = hours % 12 || 12;

   return `${displayHours}:${String(minutes).padStart(2, '0')} ${period}`;
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
      start_time: normalizeText(source.start_time),
      maximum_duration: normalizeMaximumDuration(source.maximum_duration),
      end_time: normalizeText(source.end_time),
      link: normalizeOptionalText(source.link),
      removalReason: normalizeOptionalText(source.removalReason),
   };
}

export function normalizeGuardiansTalkForSave(value) {
   const source = asObject(value);

   return {
      name: normalizeText(source.name),
      start_time: normalizeOptionalText(source.start_time),
      end_time: normalizeOptionalText(source.end_time),
   };
}

function normalizeItineraryNameForSave(value) {
   if (typeof value === 'string') {
      return normalizeText(value);
   }

   return normalizeText(asObject(value).name);
}

export function normalizeItineraryNamesForSave(items) {
   if (!Array.isArray(items)) {
      return [];
   }

   return items
      .map(normalizeItineraryNameForSave)
      .filter(Boolean);
}

export function normalizeWild(value) {
   const source = asObject(value);

   return {
      ...source,
      name: normalizeText(source.name),
      meeting_spot: normalizeText(source.meeting_spot),
      start_time: normalizeText(source.start_time),
      maximum_duration: normalizeMaximumDuration(source.maximum_duration),
      end_time: normalizeText(source.end_time),
      link: normalizeOptionalText(source.link),
      removalReason: normalizeOptionalText(source.removalReason),
   };
}
