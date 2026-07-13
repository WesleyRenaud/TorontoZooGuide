import {
   normalizeAnimal,
   normalizeAttraction,
   normalizeTalk,
   normalizeWild,
} from './format.js';
import {
   getGuardiansTalkLinkedAnimal,
   openGuardiansTalkLinkedAnimal,
} from '../../guardians/openGuardiansTalkLinkedAnimal.js';
import { openAnimalSpeciesOverlay } from '../../overlays/speciesOverlay.js';
import {
   buildRemoveRowProps,
   buildRowScheduleActionProps,
} from './rowActionProps.js';
import {
   buildAnimalAlert,
   buildAttractionRemovalReasonLine,
   buildGuardiansRemovalReasonLine,
   buildWildRemovalReasonLine,
} from './rowAlerts.js';
import {
   buildNamedRows,
   buildRows,
   buildUniqueAnimals,
   sortScheduledOccurrencesByStartTime,
} from './rowBuilders.js';
import {
   buildApproximateStartTimeFieldLine,
   buildFieldLine,
   buildImageSrc,
   buildLinkRowProps,
   buildMetaLines,
   buildScheduledTimeFieldLine,
   buildTitleLinkRowProps,
} from './rowPresentation.js';
import {
   getAnimalEnclosureName,
   getAnimalSpecies,
   getAnimalSubtitle,
} from '../selectors/animalSelector/model.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';

export function buildAnimalRows(
   animals = [],
   {
      onUnscheduleItem = null,
      onScheduleItem = null,
      onRemoveItem = null,
   } = {}
) {
   return buildRows(animals, {
      normalizeItem: normalizeAnimal,
      prepareItems: (normalizedItems) => sortScheduledOccurrencesByStartTime(
         buildUniqueAnimals(normalizedItems)
      ),
      buildRowProps: (animal) => {
         const alert = buildAnimalAlert(animal);

         return {
            species: getAnimalSpecies(animal),
            enclosureName: getAnimalEnclosureName(animal),
            imageSrc: buildImageSrc('animals', animal.exhibit, getAnimalSpecies(animal)),
            metaLines: buildMetaLines([
               getAnimalSubtitle(animal),
            ]),
            alertLine: alert.line,
            alertTone: alert.tone,
            onNameClick: () => openAnimalSpeciesOverlay(animal),
            ...buildLinkRowProps(animal.link),
            ...buildRowScheduleActionProps(
               ScheduleItemKind.ANIMAL.itemType,
               animal,
               { onUnscheduleItem, onScheduleItem, onRemoveItem }
            ),
         };
      },
   });
}

export function buildAttractionRows(
   attractions = [],
   {
      onUnscheduleItem = null,
      onScheduleItem = null,
      onRemoveItem = null,
   } = {}
) {
   return buildNamedRows(attractions, {
      normalizeItem: normalizeAttraction,
      prepareItems: sortScheduledOccurrencesByStartTime,
      defaultName: 'Attraction',
      imageDirectory: 'attractions',
      getName: (attraction) => attraction.name,
      getMetaLines: (attraction) => [
         attraction.subtitle,
         buildFieldLine('Location', attraction.location),
         buildFieldLine('Price', attraction.price),
         buildApproximateStartTimeFieldLine(attraction),
      ],
      getAlertLine: buildAttractionRemovalReasonLine,
      getLink: (attraction) => attraction.infoLink,
      extendRowProps: (attraction) => buildRowScheduleActionProps(
         ScheduleItemKind.ATTRACTION.itemType,
         attraction,
         { onUnscheduleItem, onScheduleItem, onRemoveItem }
      ),
   });
}

export function buildGuardiansRows(
   guardiansTalks = [],
   { onRemoveItem = null } = {}
) {
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
      extendRowProps: (talk) => ({
         ...(
            getGuardiansTalkLinkedAnimal(talk)
               ? {
                  onNameClick: () => {
                     void openGuardiansTalkLinkedAnimal(talk);
                  },
               }
               : {}
         ),
         ...buildRemoveRowProps(
            'guardians_talks',
            talk,
            onRemoveItem,
            { useSecondaryAction: false }
         ),
      }),
   });
}

export function buildWildRows(
   wildEncounters = [],
   { onRemoveItem = null } = {}
) {
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
      extendRowProps: (wild) => ({
         ...buildTitleLinkRowProps(wild.link),
         ...buildRemoveRowProps('wild_encounters', wild, onRemoveItem),
      }),
   });
}
