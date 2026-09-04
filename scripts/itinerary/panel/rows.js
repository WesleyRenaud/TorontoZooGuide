import {
   normalizeAnimal,
   normalizeAttraction,
   normalizeTalk,
   normalizeTransportation,
   normalizeWild,
} from './format.js';
import {
   getGuardiansTalkLinkedAnimal,
   openGuardiansTalkLinkedAnimal,
} from '../../guardians/openGuardiansTalkLinkedAnimal.js';
import { openAnimalSpeciesOverlay } from '../../overlays/speciesOverlay.js';
import { RowActionProps } from './rowActionProps.js';
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
import { ScheduledOccurrenceSort } from '../scheduledOccurrenceSort.js';
import {
   getAnimalEnclosureName,
   getAnimalSpecies,
   getAnimalSubtitle,
} from '../selectors/animalSelector/model.js';
import {
   getGuardiansTalkName,
   getGuardiansTalkTitleSuffix,
} from '../selectors/guardiansTalkSelector/model.js';
import {
   buildTransportationStationsLine,
   getTransportationName,
} from '../selectors/transportationSelector/model.js';
import {
   getWildEncounterName,
   getWildEncounterTitleSuffix,
} from '../selectors/wildEncounterSelector/model.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../strings.js';

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
      prepareItems: (normalizedItems) => ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime(
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
            ...RowActionProps.buildRowScheduleActionProps(
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
      prepareItems: ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime,
      defaultName: APP_STRINGS.entityLabels.attraction,
      imageDirectory: 'attractions',
      getName: (attraction) => attraction.name,
      getMetaLines: (attraction) => [
         attraction.subtitle,
         buildFieldLine(APP_STRINGS.labels.location, attraction.region),
         buildFieldLine(APP_STRINGS.labels.price, attraction.price),
         buildApproximateStartTimeFieldLine(attraction),
      ],
      getAlertLine: buildAttractionRemovalReasonLine,
      extendRowProps: (attraction) => ({
         ...buildTitleLinkRowProps(attraction.infoLink),
         ...RowActionProps.buildRowScheduleActionProps(
            ScheduleItemKind.ATTRACTION.itemType,
            attraction,
            { onUnscheduleItem, onScheduleItem, onRemoveItem }
         ),
      }),
   });
}

export function buildTransportationRows(
   transportations = [],
   {
      onUnscheduleItem = null,
      onScheduleItem = null,
      onRemoveItem = null,
   } = {}
) {
   return buildNamedRows(transportations, {
      normalizeItem: normalizeTransportation,
      prepareItems: ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime,
      defaultName: APP_STRINGS.entityLabels.transportation,
      imageDirectory: 'transportations',
      getName: getTransportationName,
      getMetaLines: (transportation) => [
         buildTransportationStationsLine(transportation),
         buildApproximateStartTimeFieldLine(transportation),
      ],
      getAlertLine: buildAttractionRemovalReasonLine,
      extendRowProps: (transportation) => ({
         ...buildTitleLinkRowProps(transportation.infoLink),
         ...RowActionProps.buildRowScheduleActionProps(
            ScheduleItemKind.TRANSPORTATION.itemType,
            transportation,
            { onUnscheduleItem, onScheduleItem, onRemoveItem }
         ),
      }),
   });
}

export function buildGuardiansRows(
   guardiansTalks = [],
   { onRemoveItem = null } = {}
) {
   return buildNamedRows(guardiansTalks, {
      normalizeItem: normalizeTalk,
      prepareItems: ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime,
      defaultName: APP_STRINGS.entityLabels.guardiansTalk,
      imageDirectory: 'guardians-talks',
      getName: getGuardiansTalkName,
      getImageName: getGuardiansTalkName,
      getNameSuffix: getGuardiansTalkTitleSuffix,
      getMetaLines: (talk) => [
         buildFieldLine(APP_STRINGS.labels.location, talk.location),
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
         ...RowActionProps.buildRemoveRowProps(
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
      prepareItems: ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime,
      defaultName: APP_STRINGS.entityLabels.wildEncounter,
      imageDirectory: 'wild-encounters',
      getName: getWildEncounterName,
      getImageName: getWildEncounterName,
      getNameSuffix: getWildEncounterTitleSuffix,
      getMetaLines: (wild) => [
         buildFieldLine(APP_STRINGS.itinerary.selectors.meetingSpot, wild.meeting_spot),
         buildScheduledTimeFieldLine(wild),
      ],
      getAlertLine: buildWildRemovalReasonLine,
      extendRowProps: (wild) => ({
         ...buildTitleLinkRowProps(wild.link),
         ...RowActionProps.buildRemoveRowProps('wild_encounters', wild, onRemoveItem),
      }),
   });
}
