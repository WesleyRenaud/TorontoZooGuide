import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { makeItemRow } from './components/itemRow.js';
import {
   normalizeAnimal,
   normalizeAttraction,
   normalizeTalk,
   normalizeWild,
} from './format.js';
import {
   buildAnimalAlert,
   buildAttractionRemovalReasonLine,
   buildGuardiansRemovalReasonLine,
   buildWildRemovalReasonLine,
} from './rowAlerts.js';
import { sortScheduledOccurrencesByStartTime } from '../scheduledOccurrenceSort.js';
import { buildScheduledOccurrenceTimeRange } from '../scheduledOccurrenceTimeRange.js';
import { getAnimalId } from '../selectors/animalSelector/model.js';
import { getAttractionId } from '../selectors/attractionSelector/model.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../strings.js';

function buildUnscheduleRowProps(itemType, item, onUnscheduleItem) {
   if (typeof onUnscheduleItem !== 'function') {
      return {};
   }

   const key = itemType === ScheduleItemKind.ANIMAL.itemType
      ? getAnimalId(item)
      : getAttractionId(item);

   if (!key) {
      return {};
   }

   const actionLabel = APP_STRINGS.itinerary.dayPlanner.unschedule;

   return {
      actionLabel,
      onAction: () => onUnscheduleItem({
         itemType,
         key,
      }),
   };
}

function buildImageSrc(...pathParts) {
   const normalizedParts = pathParts
      .map((part) => normalizeAssetKey(part))
      .filter(Boolean);

   if (normalizedParts.length !== pathParts.length) {
      return null;
   }

   return `images/details/${normalizedParts.join('/')}.png`;
}

function buildFieldLine(label, value) {
   if (!value) {
      return '';
   }

   return `${label}: ${value}`;
}

function buildTimeFieldLine(value) {
   if (!value) {
      return '';
   }

   return `Time: ${value}`;
}

function buildScheduledTimeFieldLine(item) {
   return buildTimeFieldLine(buildScheduledOccurrenceTimeRange(item));
}

function buildMetaLines(lines = []) {
   return lines.filter(Boolean);
}

function buildLinkRowProps(link) {
   if (!link) {
      return {};
   }

   return {
      linkText: APP_STRINGS.common.moreInfo,
      onLinkClick: () => window.open(link, '_blank'),
   };
}

function normalizeItems(items = [], normalizeItem) {
   return items.map((item) => normalizeItem(item));
}

function buildRows(
   items = [],
   {
      normalizeItem,
      prepareItems = (normalizedItems) => normalizedItems,
      buildRowProps,
   } = {}
) {
   const preparedItems = prepareItems(
      normalizeItems(items, normalizeItem)
   );

   return preparedItems.map((item) => makeItemRow(buildRowProps(item)));
}

function maxStoredLikelihood(...values) {
   const likelihoods = values
      .map((value) => (
         value == null || value === '' ? NaN : Number(value)
      ))
      .filter((value) => Number.isFinite(value));

   if (!likelihoods.length) {
      return null;
   }

   return Math.max(...likelihoods);
}

function buildUniqueAnimals(animals = []) {
   const uniqueAnimalsBySpecies = new Map();

   animals.forEach((animal) => {
      const speciesKey = String(animal.species || '').trim().toLowerCase();

      if (!speciesKey) {
         return;
      }

      const existing = uniqueAnimalsBySpecies.get(speciesKey);

      if (!existing) {
         uniqueAnimalsBySpecies.set(speciesKey, animal);
         return;
      }

      uniqueAnimalsBySpecies.set(speciesKey, {
         ...existing,
         likelihood: maxStoredLikelihood(existing.likelihood, animal.likelihood),
         old_likelihood: maxStoredLikelihood(
            existing.old_likelihood,
            animal.old_likelihood
         ),
         likelihoodBefore: maxStoredLikelihood(
            existing.likelihoodBefore,
            animal.likelihoodBefore
         ),
         likelihoodAfter: maxStoredLikelihood(
            existing.likelihoodAfter,
            animal.likelihoodAfter
         ),
      });
   });

   return Array.from(uniqueAnimalsBySpecies.values());
}

function buildNamedRows(
   items = [],
   {
      normalizeItem,
      prepareItems = (normalizedItems) => normalizedItems,
      defaultName,
      imageDirectory,
      getName,
      getMetaLines = () => [],
      getAlertLine = () => '',
      getLink = () => null,
      extendRowProps = null,
   } = {}
) {
   return buildRows(items, {
      normalizeItem,
      prepareItems,
      buildRowProps: (item) => {
         const name = getName(item) || defaultName;

         return {
            name,
            imageSrc: buildImageSrc(imageDirectory, name),
            metaLines: buildMetaLines(getMetaLines(item)),
            alertLine: getAlertLine(item),
            ...buildLinkRowProps(getLink(item)),
            ...(typeof extendRowProps === 'function' ? extendRowProps(item) : {}),
         };
      },
   });
}

export function buildAnimalRows(
   animals = [],
   { onUnscheduleItem = null } = {}
) {
   return buildRows(animals, {
      normalizeItem: normalizeAnimal,
      prepareItems: buildUniqueAnimals,
      buildRowProps: (animal) => {
         const name = animal.species || 'Animal';
         const alert = buildAnimalAlert(animal);

         return {
            name,
            imageSrc: buildImageSrc('animals', animal.exhibit, name),
            metaLines: buildMetaLines([
               buildFieldLine('Exhibit', animal.exhibit),
               buildScheduledTimeFieldLine(animal),
            ]),
            alertLine: alert.line,
            alertTone: alert.tone,
            ...buildLinkRowProps(animal.link),
            ...buildUnscheduleRowProps(
               ScheduleItemKind.ANIMAL.itemType,
               animal,
               onUnscheduleItem
            ),
         };
      },
   });
}

export function buildAttractionRows(
   attractions = [],
   { onUnscheduleItem = null } = {}
) {
   return buildNamedRows(attractions, {
      normalizeItem: normalizeAttraction,
      defaultName: 'Attraction',
      imageDirectory: 'attractions',
      getName: (attraction) => attraction.name,
      getMetaLines: (attraction) => [
         attraction.subtitle,
         buildFieldLine('Location', attraction.location),
         buildFieldLine('Price', attraction.price),
         buildScheduledTimeFieldLine(attraction),
      ],
      getAlertLine: buildAttractionRemovalReasonLine,
      getLink: (attraction) => attraction.infoLink,
      extendRowProps: (attraction) => buildUnscheduleRowProps(
         ScheduleItemKind.ATTRACTION.itemType,
         attraction,
         onUnscheduleItem
      ),
   });
}

export function buildGuardiansRows(guardiansTalks = []) {
   return buildNamedRows(guardiansTalks, {
      normalizeItem: normalizeTalk,
      prepareItems: sortScheduledOccurrencesByStartTime,
      defaultName: 'Talk',
      imageDirectory: 'guardians-talks',
      getName: (talk) => talk.name,
      getMetaLines: (talk) => [
         buildFieldLine('Location', talk.location),
         buildScheduledTimeFieldLine(talk),
      ],
      getAlertLine: buildGuardiansRemovalReasonLine,
      getLink: (talk) => talk.link,
   });
}

export function buildWildRows(wildEncounters = []) {
   return buildNamedRows(wildEncounters, {
      normalizeItem: normalizeWild,
      prepareItems: sortScheduledOccurrencesByStartTime,
      defaultName: 'Wild Encounter',
      imageDirectory: 'wild-encounters',
      getName: (wild) => wild.name,
      getMetaLines: (wild) => [
         buildFieldLine('Meeting Spot', wild.meeting_spot),
         buildScheduledTimeFieldLine(wild),
      ],
      getAlertLine: buildWildRemovalReasonLine,
      getLink: (wild) => wild.link,
   });
}
