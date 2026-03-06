// scripts/itinerary/panel/rows.js
import {
   normalizeAnimal,
   normalizeAttraction,
   normalizeTalk,
   normalizeWild,
} from './format.js';

import { makeItemRow } from './components/itemRow.js';

export function buildAnimalRows(animals = []) {
   return animals.map((rawAnimal) => {
      const a = normalizeAnimal(rawAnimal);

      const name = a.species ?? a.SPECIES ?? a.name ?? a.species_name ?? 'Animal';
      const exhibit = a.exhibit ?? a.EXHIBIT ?? a.exhibit_name ?? '';
      const imageSrc = a.imageSrc ?? a.image_src ?? a.image ?? null;
      const link = a.link ?? a.infoLink ?? a.INFO_LINK ?? null;

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [exhibit ? `Exhibit: ${exhibit}` : ''],
         linkText: link ? 'More Info' : null,
         onLinkClick: link ? () => window.open(link, '_blank') : null,
      });
   });
}

export function buildAttractionRows(attractions = []) {
   return attractions.map((rawAttr) => {
      const x = normalizeAttraction(rawAttr);

      const name = x.name ?? x.NAME ?? 'Attraction';
      const subtitle = x.subtitle ?? '';
      const imageSrc = x.imageSrc ?? x.image_src ?? null;
      const infoLink = x.infoLink ?? x.info_link ?? x.link ?? x.LINK ?? null;

      const location = x.location ?? '';
      const price = x.price ?? '';

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [
            subtitle || '',
            location ? `Location: ${location}` : '',
            price ? `Price: ${price}` : '',
         ],
         linkText: infoLink ? 'More Info' : null,
         onLinkClick: infoLink ? () => window.open(infoLink, '_blank') : null,
      });
   });
}

export function buildGuardiansRows(guardiansTalks = []) {
   return guardiansTalks.map((rawTalk) => {
      const t = normalizeTalk(rawTalk);

      const name = t.name ?? t.NAME ?? 'Talk';
      const location = t.location ?? t.LOCATION ?? '';
      const time = t.time_of_day ?? t.TIME_OF_DAY ?? t.time ?? t.TIME ?? '';
      const link = t.link ?? t.LINK ?? t.infoLink ?? t.info_link ?? null;

      const imageSrc =
         t.imageSrc ??
         t.image_src ??
         (name ? `../images/meet-the-guardians-talks/${name}.png` : null);

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [
            location ? `Location: ${location}` : '',
            time ? `Time: ${time}` : '',
         ],
         linkText: link ? 'More Info' : null,
         onLinkClick: link ? () => window.open(link, '_blank') : null,
      });
   });
}

export function buildWildRows(wildEncounters = []) {
   return wildEncounters.map((rawWild) => {
      const w = normalizeWild(rawWild);

      const name = w.name ?? w.NAME ?? 'Wild Encounter';
      const meetingSpot =
         w.meeting_spot ?? w.MEETING_SPOT ?? w.meetingSpot ?? w.location ?? w.LOCATION ?? '';
      const time = w.time_of_day ?? w.TIME_OF_DAY ?? w.time ?? w.TIME ?? '';
      const link = w.link ?? w.LINK ?? w.infoLink ?? w.info_link ?? null;

      const imageSrc =
         w.imageSrc ??
         w.image_src ??
         (name ? `../images/wild-encounters/${name}.png` : null);

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [
            meetingSpot ? `Meeting Spot: ${meetingSpot}` : '',
            time ? `Time: ${time}` : '',
         ],
         linkText: link ? 'More Info' : null,
         onLinkClick: link ? () => window.open(link, '_blank') : null,
      });
   });
}