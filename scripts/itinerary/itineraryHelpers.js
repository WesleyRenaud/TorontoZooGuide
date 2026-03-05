// scripts/itinerary/itineraryHelpers.js

export function uniq(arr) {
   return Array.from(new Set((arr || []).map(s => String(s || '').trim()).filter(Boolean)));
}

export function pluckSpecies(arr) {
   return (Array.isArray(arr) ? arr : [])
      .map(x => (x && typeof x === 'object' ? (x.species ?? x.SPECIES ?? x.name ?? '') : String(x)))
      .map(s => String(s || '').trim())
      .filter(Boolean);
}

export function pluckName(arr) {
   return (Array.isArray(arr) ? arr : [])
      .map(x => (x && typeof x === 'object' ? (x.name ?? x.NAME ?? '') : String(x)))
      .map(s => String(s || '').trim())
      .filter(Boolean);
}

export function pluckTalkNames(arr) {
   return (Array.isArray(arr) ? arr : [])
      .map(x => {
         if (x && typeof x === 'object') {
            // prefer explicit fields if present
            const name = x.name ?? x.NAME ?? x.title ?? x.TITLE ?? x.species ?? x.SPECIES ?? '';
            return String(name || '').trim();
         }

         const s = String(x || '').trim();
         if (!s) return '';

         // legacy stored display strings
         if (s.includes('||')) return s.split('||')[0].trim();
         if (s.includes('–')) return s.split('–')[0].trim();
         if (s.includes(' - ')) return s.split(' - ')[0].trim();

         return s;
      })
      .filter(Boolean);
}

// ✅ WILD ENCOUNTERS: NAME ONLY
// Strips "Name||Meeting Spot||dow||time" and similar display formats.
export function pluckWildEncounterNames(arr) {
   return (Array.isArray(arr) ? arr : [])
      .map(x => {
         if (x && typeof x === 'object') {
            return String(x.name ?? x.NAME ?? '').trim();
         }

         const s = String(x || '').trim();
         if (!s) return '';

         if (s.includes('||')) return s.split('||')[0].trim();
         if (s.includes('–')) return s.split('–')[0].trim();
         if (s.includes(' - ')) return s.split(' - ')[0].trim();

         return s;
      })
      .filter(Boolean);
}

// Used by main-itinerary.js
export function dateISOToMonthDay(dateISO) {
   let month = null;
   let day = null;

   if (!dateISO) return { month, day };

   const d = new Date(`${dateISO}T12:00:00`);
   if (!Number.isFinite(d.getTime())) return { month, day };

   const months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
   month = months[d.getMonth()] || null;
   day = d.getDate();

   return { month, day };
}

// Monday=1 ... Sunday=7 (Mon-first)
export function isoDateToMonFirstDow(iso) {
   const d = iso ? new Date(`${iso}T12:00:00`) : new Date();
   if (!Number.isFinite(d.getTime())) return 1;
   const js = d.getDay(); // Sun=0 ... Sat=6
   return js === 0 ? 7 : js; // Mon=1 ... Sun=7
}

// Used in updater.js
export function parseItineraryIncludes(itin) {
   if (!itin || typeof itin !== 'object') {
      return {
         speciesToInclude: [],
         attractionsToInclude: [],
         guardiansTalksToInclude: [],
         wildEncountersToInclude: [],
      };
   }

   return {
      speciesToInclude: uniq(pluckSpecies(itin.animals)),
      attractionsToInclude: uniq(pluckName(itin.attractions)),
      guardiansTalksToInclude: uniq(pluckTalkNames(itin.guardiansTalks)),
      wildEncountersToInclude: uniq(pluckWildEncounterNames(itin.wildEncounters)),
   };
}