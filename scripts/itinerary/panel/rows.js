import { Format } from './format.js';
import { OpenGuardiansTalkLinkedAnimal } from '../../guardians/openGuardiansTalkLinkedAnimal.js';
import { SpeciesOverlay } from '../../overlays/speciesOverlay.js';
import { RowActionProps } from './rowActionProps.js';
import { RowAlerts } from './rowAlerts.js';
import { RowBuilders } from './rowBuilders.js';
import { RowPresentation } from './rowPresentation.js';
import { ScheduledOccurrenceSort } from '../scheduledOccurrenceSort.js';
import { AnimalSelectorModel } from '../selectors/animalSelector/animalSelectorModel.js';
import { GuardiansTalkSelectorModel } from '../selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { TransportationSelectorModel } from '../selectors/transportationSelector/transportationSelectorModel.js';
import { WildEncounterSelectorModel } from '../selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { Strings } from '../../strings.js';

export class Rows {
   static buildAnimalRows(
      animals = [],
      {
         onUnscheduleItem = null,
         onScheduleItem = null,
         onRemoveItem = null,
      } = {}
   ) {
      return RowBuilders.buildRows(animals, {
         normalizeItem: Format.normalizeAnimal,
         prepareItems: (normalizedItems) => ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime(
            RowBuilders.buildUniqueAnimals(normalizedItems)
         ),
         buildRowProps: (animal) => {
            const alert = RowAlerts.buildAnimalAlert(animal);

            return {
               species: AnimalSelectorModel.getAnimalSpecies(animal),
               enclosureName: AnimalSelectorModel.getAnimalEnclosureName(animal),
               imageSrc: RowPresentation.buildImageSrc(
                  'animals',
                  animal.exhibit,
                  AnimalSelectorModel.getAnimalSpecies(animal)
               ),
               metaLines: RowPresentation.buildMetaLines([
                  AnimalSelectorModel.getAnimalSubtitle(animal),
               ]),
               alertLine: alert.line,
               alertTone: alert.tone,
               onNameClick: () => SpeciesOverlay.openAnimalSpeciesOverlay(animal),
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

   static buildAttractionRows(
      attractions = [],
      {
         onUnscheduleItem = null,
         onScheduleItem = null,
         onRemoveItem = null,
      } = {}
   ) {
      return RowBuilders.buildNamedRows(attractions, {
         normalizeItem: Format.normalizeAttraction,
         prepareItems: ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime,
         defaultName: Strings.entityLabels.attraction,
         imageDirectory: 'attractions',
         getName: (attraction) => attraction.name,
         getMetaLines: (attraction) => [
            attraction.subtitle,
            RowPresentation.buildFieldLine(Strings.labels.location, attraction.region),
            RowPresentation.buildFieldLine(Strings.labels.price, attraction.price),
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

   static buildTransportationRows(
      transportations = [],
      {
         onUnscheduleItem = null,
         onScheduleItem = null,
         onRemoveItem = null,
      } = {}
   ) {
      return RowBuilders.buildNamedRows(transportations, {
         normalizeItem: Format.normalizeTransportation,
         prepareItems: ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime,
         defaultName: Strings.entityLabels.transportation,
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

   static buildGuardiansRows(
      guardiansTalks = [],
      { onRemoveItem = null } = {}
   ) {
      return RowBuilders.buildNamedRows(guardiansTalks, {
         normalizeItem: Format.normalizeTalk,
         prepareItems: ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime,
         defaultName: Strings.entityLabels.guardiansTalk,
         imageDirectory: 'guardians-talks',
         getName: GuardiansTalkSelectorModel.getGuardiansTalkName,
         getImageName: GuardiansTalkSelectorModel.getGuardiansTalkName,
         getNameSuffix: GuardiansTalkSelectorModel.getGuardiansTalkTitleSuffix,
         getMetaLines: (talk) => [
            RowPresentation.buildFieldLine(Strings.labels.location, talk.location),
            RowPresentation.buildScheduledTimeFieldLine(talk),
         ],
         getAlertLine: RowAlerts.buildGuardiansRemovalReasonLine,
         getLink: (talk) => talk.link,
         extendRowProps: (talk) => ({
            ...(
               OpenGuardiansTalkLinkedAnimal.getGuardiansTalkLinkedAnimal(talk)
                  ? {
                     onNameClick: () => {
                        void OpenGuardiansTalkLinkedAnimal.openGuardiansTalkLinkedAnimal(talk);
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

   static buildWildRows(
      wildEncounters = [],
      { onRemoveItem = null } = {}
   ) {
      return RowBuilders.buildNamedRows(wildEncounters, {
         normalizeItem: Format.normalizeWild,
         prepareItems: ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime,
         defaultName: Strings.entityLabels.wildEncounter,
         imageDirectory: 'wild-encounters',
         getName: WildEncounterSelectorModel.getWildEncounterName,
         getImageName: WildEncounterSelectorModel.getWildEncounterName,
         getNameSuffix: WildEncounterSelectorModel.getWildEncounterTitleSuffix,
         getMetaLines: (wild) => [
            RowPresentation.buildFieldLine(
               Strings.itinerary.selectors.meetingSpot,
               wild.meeting_spot
            ),
            RowPresentation.buildScheduledTimeFieldLine(wild),
         ],
         getAlertLine: RowAlerts.buildWildRemovalReasonLine,
         extendRowProps: (wild) => ({
            ...RowPresentation.buildTitleLinkRowProps(wild.link),
            ...RowActionProps.buildRemoveRowProps('wild_encounters', wild, onRemoveItem),
         }),
      });
   }
}
