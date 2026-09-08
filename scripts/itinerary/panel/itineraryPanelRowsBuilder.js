import { GuardiansTalkLinkedAnimalOpener } from '../../guardians/guardiansTalkLinkedAnimalOpener.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';
import { SpeciesFragment } from '../../overlays/speciesFragment.js';
import { RowActionPresenter } from './rowActionPresenter.js';
import { RowAlertPresenter } from './rowAlertPresenter.js';
import { RowBuilder } from './rowBuilder.js';
import { RowPresenter } from './rowPresenter.js';
import { ScheduledOccurrenceSorter } from '../scheduledOccurrenceSorter.js';
import { AnimalSelectorModel } from '../selectors/animalSelector/animalSelectorModel.js';
import { GuardiansTalkSelectorModel } from '../selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { TransportationSelectorModel } from '../selectors/transportationSelector/transportationSelectorModel.js';
import { WildEncounterSelectorModel } from '../selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { Strings } from '../../strings.js';

export class ItineraryPanelRowsBuilder {
   static buildAnimalRows(
      animals = [],
      {
         onUnscheduleItem = null,
         onScheduleItem = null,
         onRemoveItem = null,
      } = {}
   ) {
      return RowBuilder.buildRows(animals, {
         normalizeItem: ItineraryItemFormatter.normalizeAnimal,
         prepareItems: (normalizedItems) => ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime(
            RowBuilder.buildUniqueAnimals(normalizedItems)
         ),
         buildRowProps: (animal) => {
            const alert = RowAlertPresenter.buildAnimalAlert(animal);

            return {
               species: AnimalSelectorModel.getAnimalSpecies(animal),
               enclosureName: AnimalSelectorModel.getAnimalEnclosureName(animal),
               imageSrc: RowPresenter.buildImageSrc(
                  'animals',
                  animal.exhibit,
                  AnimalSelectorModel.getAnimalSpecies(animal)
               ),
               metaLines: RowPresenter.buildMetaLines([
                  AnimalSelectorModel.getAnimalSubtitle(animal),
               ]),
               alertLine: alert.line,
               alertTone: alert.tone,
               onNameClick: () => SpeciesFragment.openAnimalSpeciesOverlay(animal),
               ...RowPresenter.buildLinkRowProps(animal.link),
               ...RowActionPresenter.buildRowScheduleActionProps(
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
      return RowBuilder.buildNamedRows(attractions, {
         normalizeItem: ItineraryItemFormatter.normalizeAttraction,
         prepareItems: ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime,
         defaultName: Strings.entityLabels.attraction,
         imageDirectory: 'attractions',
         getName: (attraction) => attraction.name,
         getMetaLines: (attraction) => [
            attraction.subtitle,
            RowPresenter.buildFieldLine(Strings.labels.location, attraction.region),
            RowPresenter.buildFieldLine(Strings.labels.price, attraction.price),
            RowPresenter.buildApproximateStartTimeFieldLine(attraction),
         ],
         getAlertLine: RowAlertPresenter.buildAttractionRemovalReasonLine,
         extendRowProps: (attraction) => ({
            ...RowPresenter.buildTitleLinkRowProps(attraction.infoLink),
            ...RowActionPresenter.buildRowScheduleActionProps(
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
      return RowBuilder.buildNamedRows(transportations, {
         normalizeItem: ItineraryItemFormatter.normalizeTransportation,
         prepareItems: ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime,
         defaultName: Strings.entityLabels.transportation,
         imageDirectory: 'transportations',
         getName: TransportationSelectorModel.getTransportationName,
         getMetaLines: (transportation) => [
            TransportationSelectorModel.buildTransportationStationsLine(transportation),
            RowPresenter.buildApproximateStartTimeFieldLine(transportation),
         ],
         getAlertLine: RowAlertPresenter.buildAttractionRemovalReasonLine,
         extendRowProps: (transportation) => ({
            ...RowPresenter.buildTitleLinkRowProps(transportation.infoLink),
            ...RowActionPresenter.buildRowScheduleActionProps(
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
      return RowBuilder.buildNamedRows(guardiansTalks, {
         normalizeItem: ItineraryItemFormatter.normalizeTalk,
         prepareItems: ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime,
         defaultName: Strings.entityLabels.guardiansTalk,
         imageDirectory: 'guardians-talks',
         getName: GuardiansTalkSelectorModel.getGuardiansTalkName,
         getImageName: GuardiansTalkSelectorModel.getGuardiansTalkName,
         getNameSuffix: GuardiansTalkSelectorModel.getGuardiansTalkTitleSuffix,
         getMetaLines: (talk) => [
            RowPresenter.buildFieldLine(Strings.labels.location, talk.location),
            RowPresenter.buildScheduledTimeFieldLine(talk),
         ],
         getAlertLine: RowAlertPresenter.buildGuardiansRemovalReasonLine,
         getLink: (talk) => talk.link,
         extendRowProps: (talk) => ({
            ...(
               GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal(talk)
                  ? {
                     onNameClick: () => {
                        void GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal(talk);
                     },
                  }
                  : {}
            ),
            ...RowActionPresenter.buildRemoveRowProps(
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
      return RowBuilder.buildNamedRows(wildEncounters, {
         normalizeItem: ItineraryItemFormatter.normalizeWild,
         prepareItems: ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime,
         defaultName: Strings.entityLabels.wildEncounter,
         imageDirectory: 'wild-encounters',
         getName: WildEncounterSelectorModel.getWildEncounterName,
         getImageName: WildEncounterSelectorModel.getWildEncounterName,
         getNameSuffix: WildEncounterSelectorModel.getWildEncounterTitleSuffix,
         getMetaLines: (wild) => [
            RowPresenter.buildFieldLine(
               Strings.itinerary.selectors.meetingSpot,
               wild.meeting_spot
            ),
            RowPresenter.buildScheduledTimeFieldLine(wild),
         ],
         getAlertLine: RowAlertPresenter.buildWildRemovalReasonLine,
         extendRowProps: (wild) => ({
            ...RowPresenter.buildTitleLinkRowProps(wild.link),
            ...RowActionPresenter.buildRemoveRowProps('wild_encounters', wild, onRemoveItem),
         }),
      });
   }
}
