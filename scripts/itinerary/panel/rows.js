import {
   normalizeAnimal,
   normalizeAttraction,
   normalizeTalk,
   normalizeWild,
} from './format.js';

import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { makeItemRow } from './components/itemRow.js';
import {
   buildAnimalAlert,
   buildAttractionRemovalReasonLine,
   buildGuardiansRemovalReasonLine,
   buildWildRemovalReasonLine,
} from './rowAlerts.js';

function buildImageSrc(directory, name) {
   if (!name) return null;

   const normalizedName = normalizeAssetKey(name);
   return `images/${directory}/${normalizedName}.png`;
}

function buildAnimalImageSrc(exhibit, species) {
   if (!exhibit || !species) return null;

   const normalizedExhibit = normalizeAssetKey(exhibit);
   const normalizedSpecies = normalizeAssetKey(species);

   return `images/animals/${normalizedExhibit}/${normalizedSpecies}.png`;
}

function mergeNormalizedItem(rawItem, normalizeItem) {
   const normalizedItem = normalizeItem(rawItem);

   return rawItem && typeof rawItem === 'object'
      ? { ...rawItem, ...normalizedItem }
      : normalizedItem;
}

function buildLinkRowProps(link) {
   if (!link) {
      return {
         linkText: null,
         onLinkClick: null,
      };
   }

   return {
      linkText: 'More Info',
      onLinkClick: () => window.open(link, '_blank'),
   };
}

function buildRows(items = [], normalizeItem, buildRowProps) {
   return items.map((rawItem) => {
      const item = mergeNormalizedItem(rawItem, normalizeItem);

      return makeItemRow({
         ...buildRowProps(item),
      });
   });
}

function buildUniqueAnimals(animals = []) {
   const uniqueAnimals = [];
   const seenSpecies = new Set();

   animals.forEach((rawAnimal) => {
      const animal = mergeNormalizedItem(rawAnimal, normalizeAnimal);
      const speciesKey = String(animal.species || '').trim().toLowerCase();

      if (!speciesKey || seenSpecies.has(speciesKey)) {
         return;
      }

      seenSpecies.add(speciesKey);
      uniqueAnimals.push(animal);
   });

   return uniqueAnimals;
}

export function buildAnimalRows(animals = []) {
   return buildRows(buildUniqueAnimals(animals), normalizeAnimal, (animal) => {
      const name = animal.species || 'Animal';
      const exhibit = animal.exhibit || '';
      const alert = buildAnimalAlert(animal);

      return {
         name,
         imageSrc: buildAnimalImageSrc(exhibit, name),
         metaLines: [
            exhibit ? `Exhibit: ${exhibit}` : '',
         ],
         alertLine: alert.line,
         alertTone: alert.tone,
         ...buildLinkRowProps(animal.link || null),
      };
   });
}

export function buildAttractionRows(attractions = []) {
   return buildRows(attractions, normalizeAttraction, (attraction) => {
      const name = attraction.name || 'Attraction';
      const subtitle = attraction.subtitle ?? '';
      const location = attraction.location ?? '';
      const price = attraction.price ?? '';
      const infoLink = attraction.infoLink || null;

      return {
         name,
         imageSrc: buildImageSrc('attractions', name),
         metaLines: [
            subtitle || '',
            location ? `Location: ${location}` : '',
            price ? `Price: ${price}` : '',
         ],
         alertLine: buildAttractionRemovalReasonLine(attraction),
         ...buildLinkRowProps(infoLink),
      };
   });
}

export function buildGuardiansRows(guardiansTalks = []) {
   return buildRows(guardiansTalks, normalizeTalk, (talk) => {
      const name = talk.name || 'Talk';
      const location = talk.location || '';
      const time = talk.time_of_day || '';

      return {
         name,
         imageSrc: buildImageSrc('guardians-talks', name),
         metaLines: [
            location ? `Location: ${location}` : '',
            time ? `Time: ${time}` : '',
         ],
         alertLine: buildGuardiansRemovalReasonLine(talk),
         ...buildLinkRowProps(talk.link || null),
      };
   });
}

export function buildWildRows(wildEncounters = []) {
   return buildRows(wildEncounters, normalizeWild, (wild) => {
      const name = wild.name || 'Wild Encounter';
      const meetingSpot = wild.meeting_spot || '';
      const time = wild.time_of_day || '';

      return {
         name,
         imageSrc: buildImageSrc('wild-encounters', name),
         metaLines: [
            meetingSpot ? `Meeting Spot: ${meetingSpot}` : '',
            time ? `Time: ${time}` : '',
         ],
         alertLine: buildWildRemovalReasonLine(wild),
         ...buildLinkRowProps(wild.link || null),
      };
   });
}
