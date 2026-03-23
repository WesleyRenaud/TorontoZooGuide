import {
   normalizeAnimal,
   normalizeAttraction,
   normalizeTalk,
   normalizeWild,
} from './format.js';

import { makeItemRow } from './components/itemRow.js';

function normalizeForPath(str = '') {
   return String(str)
      .toLowerCase()
      .trim()
      .replace(/&/g, 'and')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
}

function buildAnimalImageSrc(exhibit, species) {
   if (!exhibit || !species) return null;

   const normalizedExhibit = normalizeForPath(exhibit);
   const normalizedSpecies = normalizeForPath(species);

   return `images/animals/${normalizedExhibit}/${normalizedSpecies}.png`;
}

function buildAttractionImageSrc(name) {
   if (!name) return null;

   const normalizedName = normalizeForPath(name);
   return `images/attractions/${normalizedName}.png`;
}

function buildGuardiansTalkImageSrc(name) {
   if (!name) return null;

   const normalizedName = normalizeForPath(name);
   return `images/guardians-talks/${normalizedName}.png`;
}

function buildWildEncounterImageSrc(name) {
   if (!name) return null;

   const normalizedName = normalizeForPath(name);
   return `images/wild-encounters/${normalizedName}.png`;
}

function toPercent(value) {
   if (typeof value !== 'number' || !Number.isFinite(value)) return null;
   return Math.round(value > 1 ? value : value * 100);
}

function getLikelihoodPair(animal) {
   const beforeRaw =
      animal?.likelihoodBefore ??
      animal?.likelihood_before ??
      animal?.previousLikelihood ??
      animal?.previous_likelihood ??
      animal?.oldLikelihood ??
      animal?.old_likelihood;

   const afterRaw =
      animal?.likelihoodAfter ??
      animal?.likelihood_after ??
      animal?.currentLikelihood ??
      animal?.current_likelihood ??
      animal?.newLikelihood ??
      animal?.new_likelihood ??
      animal?.likelihood ??
      animal?.LIKELIHOOD;

   const before = toPercent(Number(beforeRaw));
   const after = toPercent(Number(afterRaw));

   return { before, after };
}

function buildAnimalRemovalReasonLine(animal) {
   const reason =
      animal.removalReason ??
      animal.removal_reason ??
      animal.off_display_message ??
      animal.OFF_DISPLAY_MESSAGE ??
      animal.display_message ??
      animal.DISPLAY_MESSAGE ??
      '';

   if (!reason) return '';

   return `Unavailable: ${reason}`;
}

function buildAnimalVisibilityChange(animal) {
   const { before, after } = getLikelihoodPair(animal);

   if (before == null || after == null || before === after) {
      return {
         line: '',
         tone: 'default',
      };
   }

   if (after < before) {
      return {
         line: `Projected visibility changed from ${before}% to ${after}% on your new date.`,
         tone: 'default',
      };
   }

   return {
      line: `Projected visibility changed from ${before}% to ${after}% on your new date.`,
      tone: 'positive',
   };
}

function buildAnimalAlert(animal) {
   const removalLine = buildAnimalRemovalReasonLine(animal);
   if (removalLine) {
      return {
         line: removalLine,
         tone: 'default',
      };
   }

   return buildAnimalVisibilityChange(animal);
}

function buildAttractionRemovalReasonLine(attraction) {
   const reason =
      attraction.removalReason ??
      attraction.removal_reason ??
      attraction.closed_message ??
      attraction.CLOSED_MESSAGE ??
      attraction.display_message ??
      attraction.DISPLAY_MESSAGE ??
      '';

   if (!reason) return '';

   return `Not available on this date: ${reason}`;
}

function buildGuardiansRemovalReasonLine(guardiansTalk) {
   const reason =
      guardiansTalk.removalReason ??
      guardiansTalk.removal_reason ??
      guardiansTalk.unavailable_message ??
      guardiansTalk.UNAVAILABLE_MESSAGE ??
      guardiansTalk.display_message ??
      guardiansTalk.DISPLAY_MESSAGE ??
      '';

   if (!reason) return '';

   return `Not available on this date: ${reason}`;
}

function buildWildRemovalReasonLine(wildEncounter) {
   const reason =
      wildEncounter.removalReason ??
      wildEncounter.removal_reason ??
      wildEncounter.unavailable_message ??
      wildEncounter.UNAVAILABLE_MESSAGE ??
      wildEncounter.display_message ??
      wildEncounter.DISPLAY_MESSAGE ??
      '';

   if (!reason) return '';

   return `Not available on this date: ${reason}`;
}

export function buildAnimalRows(animals = []) {
   const uniqueAnimals = [];
   const seenSpecies = new Set();

   animals.forEach((rawAnimal) => {
      const a = normalizeAnimal(rawAnimal);

      const name = a.species ?? a.SPECIES ?? a.name ?? a.species_name ?? 'Animal';
      const speciesKey = String(name).trim().toLowerCase();

      if (!speciesKey || seenSpecies.has(speciesKey)) {
         return;
      }

      seenSpecies.add(speciesKey);
      uniqueAnimals.push({ ...rawAnimal, ...a });
   });

   return uniqueAnimals.map((a) => {
      const name = a.species ?? a.SPECIES ?? a.name ?? a.species_name ?? 'Animal';
      const exhibit = a.exhibit ?? a.EXHIBIT ?? a.exhibit_name ?? '';
      const link = a.link ?? a.infoLink ?? a.INFO_LINK ?? null;
      const imageSrc = buildAnimalImageSrc(exhibit, name);
      const alert = buildAnimalAlert(a);

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [
            exhibit ? `Exhibit: ${exhibit}` : '',
         ],
         alertLine: alert.line,
         alertTone: alert.tone,
         linkText: link ? 'More Info' : null,
         onLinkClick: link ? () => window.open(link, '_blank') : null,
      });
   });
}

export function buildAttractionRows(attractions = []) {
   return attractions.map((rawAttr) => {
      const x = normalizeAttraction(rawAttr);
      const attraction = { ...rawAttr, ...x };

      const name = attraction.name ?? attraction.NAME ?? 'Attraction';
      const subtitle = attraction.subtitle ?? '';
      const imageSrc = buildAttractionImageSrc(name);
      const infoLink =
         attraction.infoLink ??
         attraction.info_link ??
         attraction.link ??
         attraction.LINK ??
         null;

      const location = attraction.location ?? '';
      const price = attraction.price ?? '';
      const alertLine = buildAttractionRemovalReasonLine(attraction);

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [
            subtitle || '',
            location ? `Location: ${location}` : '',
            price ? `Price: ${price}` : '',
         ],
         alertLine,
         linkText: infoLink ? 'More Info' : null,
         onLinkClick: infoLink ? () => window.open(infoLink, '_blank') : null,
      });
   });
}

export function buildGuardiansRows(guardiansTalks = []) {
   return guardiansTalks.map((rawTalk) => {
      const t = normalizeTalk(rawTalk);
      const talk = { ...rawTalk, ...t };

      const name = talk.name ?? talk.NAME ?? 'Talk';
      const location = talk.location ?? talk.LOCATION ?? '';
      const time = talk.time_of_day ?? talk.TIME_OF_DAY ?? talk.time ?? talk.TIME ?? '';
      const link = talk.link ?? talk.LINK ?? talk.infoLink ?? talk.info_link ?? null;
      const imageSrc = buildGuardiansTalkImageSrc(name);
      const alertLine = buildGuardiansRemovalReasonLine(talk);

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [
            location ? `Location: ${location}` : '',
            time ? `Time: ${time}` : '',
         ],
         alertLine,
         linkText: link ? 'More Info' : null,
         onLinkClick: link ? () => window.open(link, '_blank') : null,
      });
   });
}

export function buildWildRows(wildEncounters = []) {
   return wildEncounters.map((rawWild) => {
      const w = normalizeWild(rawWild);
      const wild = { ...rawWild, ...w };

      const name = wild.name ?? wild.NAME ?? 'Wild Encounter';
      const meetingSpot =
         wild.meeting_spot ?? wild.MEETING_SPOT ?? wild.meetingSpot ?? wild.location ?? wild.LOCATION ?? '';
      const time = wild.time_of_day ?? wild.TIME_OF_DAY ?? wild.time ?? wild.TIME ?? '';
      const link = wild.link ?? wild.LINK ?? wild.infoLink ?? wild.info_link ?? null;
      const imageSrc = buildWildEncounterImageSrc(name);
      const alertLine = buildWildRemovalReasonLine(wild);

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [
            meetingSpot ? `Meeting Spot: ${meetingSpot}` : '',
            time ? `Time: ${time}` : '',
         ],
         alertLine,
         linkText: link ? 'More Info' : null,
         onLinkClick: link ? () => window.open(link, '_blank') : null,
      });
   });
}