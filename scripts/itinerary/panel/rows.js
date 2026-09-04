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
import { RowAlerts } from './rowAlerts.js';
import {
   buildNamedRows,
   buildRows,
   buildUniqueAnimals,
} from './rowBuilders.js';
import { RowPresentation } from './rowPresentation.js';
import { ScheduledOccurrenceSort } from '../scheduledOccurrenceSort.js';
import { AnimalSelectorModel } from '../selectors/animalSelector/animalSelectorModel.js';
import { GuardiansTalkSelectorModel } from '../selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { TransportationSelectorModel } from '../selectors/transportationSelector/transportationSelectorModel.js';
import { WildEncounterSelectorModel } from '../selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
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
         const alert = RowAlerts.buildAnimalAlert(animal);

         return {
            species: AnimalSelectorModel.getAnimalSpecies(animal),
            enclosureName: AnimalSelectorModel.getAnimalEnclosureName(animal),
            imageSrc: RowPresentation.buildImageSrc('animals', animal.exhibit, AnimalSelectorModel.getAnimalSpecies(animal)),
            metaLines: RowPresentation.buildMetaLines([
               AnimalSelectorModel.getAnimalSubtitle(animal),
            ]),
            alertLine: alert.line,
            alertTone: alert.tone,
            onNameClick: () => openAnimalSpeciesOverlay(animal),
            ...RowPresentation.buildLinkRowProps(animal.link),
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
         RowPresentation.buildFieldLine(APP_STRINGS.labels.location, attraction.region),
         RowPresentation.buildFieldLine(APP_STRINGS.labels.price, attraction.price),
         RowPresentation.buildApproximateStartTimeFieldLine(attraction),
      ],
      getAlertLine: RowAlerts.buildAttractionRemovalReasonLine,
      extendRowProps: (attraction) => ({
         ...RowPresentation.buildTitleLinkRowProps(attraction.infoLink),
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
      getName: TransportationSelectorModel.getTransportationName,
      getMetaLines: (transportation) => [
         TransportationSelectorModel.buildTransportationStationsLine(transportation),
         RowPresentation.buildApproximateStartTimeFieldLine(transportation),
      ],
      getAlertLine: RowAlerts.buildAttractionRemovalReasonLine,
      extendRowProps: (transportation) => ({
         ...RowPresentation.buildTitleLinkRowProps(transportation.infoLink),
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
      getName: GuardiansTalkSelectorModel.getGuardiansTalkName,
      getImageName: GuardiansTalkSelectorModel.getGuardiansTalkName,
      getNameSuffix: GuardiansTalkSelectorModel.getGuardiansTalkTitleSuffix,
      getMetaLines: (talk) => [
         RowPresentation.buildFieldLine(APP_STRINGS.labels.location, talk.location),
         RowPresentation.buildScheduledTimeFieldLine(talk),
      ],
      getAlertLine: RowAlerts.buildGuardiansRemovalReasonLine,
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
      getName: WildEncounterSelectorModel.getWildEncounterName,
      getImageName: WildEncounterSelectorModel.getWildEncounterName,
      getNameSuffix: WildEncounterSelectorModel.getWildEncounterTitleSuffix,
      getMetaLines: (wild) => [
         RowPresentation.buildFieldLine(APP_STRINGS.itinerary.selectors.meetingSpot, wild.meeting_spot),
         RowPresentation.buildScheduledTimeFieldLine(wild),
      ],
      getAlertLine: RowAlerts.buildWildRemovalReasonLine,
      extendRowProps: (wild) => ({
         ...RowPresentation.buildTitleLinkRowProps(wild.link),
         ...RowActionProps.buildRemoveRowProps('wild_encounters', wild, onRemoveItem),
      }),
   });
}
