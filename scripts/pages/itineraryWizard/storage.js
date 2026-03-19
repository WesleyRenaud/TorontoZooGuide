export function safeParseJSON(raw, fallback) {
   try {
      return JSON.parse(raw);
   } catch {
      return fallback;
   }
}

export function loadArray(key) {
   try {
      const raw = localStorage.getItem(key);
      const arr = JSON.parse(raw || '[]');
      return Array.isArray(arr) ? arr : [];
   } catch {
      return [];
   }
}

export function isItineraryEmpty(itin) {
   if (!itin || typeof itin !== 'object') return true;

   const animals = Array.isArray(itin.animals) ? itin.animals : [];
   const attractions = Array.isArray(itin.attractions) ? itin.attractions : [];
   const guardiansTalks = Array.isArray(itin.guardiansTalks) ? itin.guardiansTalks : [];
   const wildEncounters = Array.isArray(itin.wildEncounters) ? itin.wildEncounters : [];

   return !animals.length && !attractions.length && !guardiansTalks.length && !wildEncounters.length;
}