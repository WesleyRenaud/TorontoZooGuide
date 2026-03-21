export function uniq(arr) {
   return Array.from(new Set((arr || []).map(s => String(s || '').trim()).filter(Boolean)));
}

export function uniqBy(arr, getKey) {
   const seen = new Set();
   const out = [];

   for(const item of (arr || [])) {
      const key = String(getKey(item) || '').trim();
      if (!key || seen.has(key)) continue;
      seen.add(key);
      out.push(item);
   }

   return out;
}

export function pluckAnimals(arr) {
   return (Array.isArray(arr) ? arr : [])
      .map(x => {
         if (x && typeof x === 'object') {
            return {
               species: String(x.species ?? x.SPECIES ?? x.name ?? '').trim(),
               exhibit: String(x.exhibit ?? x.EXHIBIT ?? '').trim(),
            };
         }

         return {
            species: String(x || '').trim(),
            exhibit: '',
         };
      })
      .filter(x => x.species);
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
            const name = x.name ?? x.NAME ?? x.title ?? x.TITLE ?? x.species ?? x.SPECIES ?? '';
            return String(name || '').trim();
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

export function dateToMonthDay(date) {
   let month = null;
   let day = null;

   if (!date) return { month, day };

   const d = new Date(`${date}T12:00:00`);
   if (!Number.isFinite(d.getTime())) return { month, day };

   const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
   month = months[d.getMonth()] || null;
   day = d.getDate();

   return { month, day };
}

export function isoDateToMonFirstDow(iso) {
   const d = iso ? new Date(`${iso}T12:00:00`) : new Date();
   if (!Number.isFinite(d.getTime())) return 1;
   const js = d.getDay();
   return js === 0 ? 7 : js;
}

export function parseItineraryIncludes(itin) {
   if (!itin || typeof itin !== 'object') {
      return {
         animalsToInclude: [],
         attractionsToInclude: [],
         guardiansTalksToInclude: [],
         wildEncountersToInclude: [],
      };
   }

   return {
      animalsToInclude: uniqBy(
         pluckAnimals(itin.animals),
         animal => `${animal.species}||${animal.exhibit}`
      ),
      attractionsToInclude: uniq(pluckName(itin.attractions)),
      guardiansTalksToInclude: uniq(pluckTalkNames(itin.guardiansTalks)),
      wildEncountersToInclude: uniq(pluckWildEncounterNames(itin.wildEncounters)),
   };
}