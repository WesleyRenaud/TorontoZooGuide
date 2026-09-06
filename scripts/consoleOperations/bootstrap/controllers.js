import { AnimalOffDisplay } from '../animals/controllers/animalOffDisplay.js';
import { AnimalOnDisplay } from '../animals/controllers/animalOnDisplay.js';
import { AnimalSpeciesAutocomplete } from '../animals/controllers/animalSpeciesAutocomplete.js';
import { AnimalViewingAlert } from '../animals/controllers/animalViewingAlert.js';
import { AnimalVisibilitySchedule } from '../animals/controllers/animalVisibilitySchedule.js';
import { RemoveViewingAlert } from '../animals/controllers/removeViewingAlert.js';
import { RemoveVisibilitySchedule } from '../animals/controllers/removeVisibilitySchedule.js';
import { AttractionClosed } from '../attractions/controllers/attractionClosed.js';
import { AttractionClosureOverride } from '../attractions/controllers/attractionClosureOverride.js';
import { AttractionHoursSchedule } from '../attractions/controllers/attractionHoursSchedule.js';
import { AttractionOpeningSchedule } from '../attractions/controllers/attractionOpeningSchedule.js';
import { DrinkingFountainsClosed } from '../drinkingFountains/controllers/drinkingFountainsClosed.js';
import { DrinkingFountainsOpen } from '../drinkingFountains/controllers/drinkingFountainsOpen.js';
import { CreateEvent } from '../events/controllers/createEvent.js';
import { ExhibitClosed } from '../exhibits/controllers/exhibitClosed.js';
import { ExhibitOpen } from '../exhibits/controllers/exhibitOpen.js';
import { GiftShopClosed } from '../giftShops/controllers/giftShopClosed.js';
import { GiftShopClosureOverride } from '../giftShops/controllers/giftShopClosureOverride.js';
import { GiftShopOpeningSchedule } from '../giftShops/controllers/giftShopOpeningSchedule.js';
import { AddGuardiansTalkOccurrence } from '../guardiansTalks/controllers/addGuardiansTalkOccurrence.js';
import { CancelGuardiansTalkOccurrence } from '../guardiansTalks/controllers/cancelGuardiansTalkOccurrence.js';
import { EndGuardiansTalkSchedule } from '../guardiansTalks/controllers/endGuardiansTalkSchedule.js';
import { GuardiansTalkLocationFilter } from '../guardiansTalks/controllers/guardiansTalkLocationFilter.js';
import { GuardiansTalkOccurrenceFilter } from '../guardiansTalks/controllers/guardiansTalkOccurrenceFilter.js';
import { GuardiansTalkSchedule } from '../guardiansTalks/controllers/guardiansTalkSchedule.js';
import { GuardiansTalkScheduleTimesFilter } from '../guardiansTalks/controllers/guardiansTalkScheduleTimesFilter.js';
import { RestaurantClosed } from '../restaurants/controllers/restaurantClosed.js';
import { RestaurantClosureOverride } from '../restaurants/controllers/restaurantClosureOverride.js';
import { RestaurantOpeningSchedule } from '../restaurants/controllers/restaurantOpeningSchedule.js';
import { RemoveRestroomAlert } from '../restrooms/controllers/removeRestroomAlert.js';
import { RestroomAlert } from '../restrooms/controllers/restroomAlert.js';
import { RestroomClosed } from '../restrooms/controllers/restroomClosed.js';
import { RestroomOpen } from '../restrooms/controllers/restroomOpen.js';
import { TransportationRoute } from '../transportation/controllers/transportationRoute.js';
import { TransportationStationClosed } from '../transportation/controllers/transportationStationClosed.js';
import { TransportationStationOpen } from '../transportation/controllers/transportationStationOpen.js';
import { CreateUpdate } from '../updates/controllers/createUpdate.js';
import { EditUpdate } from '../updates/controllers/editUpdate.js';
import { EndUpdate } from '../updates/controllers/endUpdate.js';
import { CancelWildEncounterOccurrence } from '../wildEncounters/controllers/cancelWildEncounterOccurrence.js';
import { EndWildEncounterSchedule } from '../wildEncounters/controllers/endWildEncounterSchedule.js';
import { WildEncounterOccurrenceFilter } from '../wildEncounters/controllers/wildEncounterOccurrenceFilter.js';
import { WildEncounterSchedule } from '../wildEncounters/controllers/wildEncounterSchedule.js';
import { WildEncounterScheduleTimesFilter } from '../wildEncounters/controllers/wildEncounterScheduleTimesFilter.js';

const ANIMAL_SPECIES_AUTOCOMPLETE_KEYS = [
   'offDisplay',
   'onDisplay',
   'visibilitySchedule',
   'removeVisibilitySchedule',
   'viewingAlert',
   'removeViewingAlert',
];

const CONTROLLER_BINDINGS = [
   {
      createController: AnimalOffDisplay.createAnimalOffDisplayController,
      getRefs: refs => refs.animals.offDisplay,
   },
   {
      createController: AnimalOnDisplay.createAnimalOnDisplayController,
      getRefs: refs => refs.animals.onDisplay,
   },
   {
      createController: AnimalVisibilitySchedule.createAnimalVisibilityScheduleController,
      getRefs: refs => refs.animals.visibilitySchedule,
   },
   {
      createController: RemoveVisibilitySchedule.createRemoveVisibilityScheduleController,
      getRefs: refs => refs.animals.removeVisibilitySchedule,
   },
   {
      createController: AnimalViewingAlert.createAnimalViewingAlertController,
      getRefs: refs => refs.animals.viewingAlert,
   },
   {
      createController: RemoveViewingAlert.createRemoveViewingAlertController,
      getRefs: refs => refs.animals.removeViewingAlert,
   },
   {
      createController: ExhibitClosed.createExhibitClosedController,
      getRefs: refs => refs.exhibits.closed,
   },
   {
      createController: ExhibitOpen.createExhibitOpenController,
      getRefs: refs => refs.exhibits.open,
   },
   {
      createController: RestaurantClosed.createRestaurantClosedController,
      getRefs: refs => refs.restaurants.closed,
   },
   {
      createController: RestaurantClosureOverride.createRestaurantClosureOverrideController,
      getRefs: refs => refs.restaurants.closureOverride,
   },
   {
      createController: RestaurantOpeningSchedule.createRestaurantOpeningScheduleController,
      getRefs: refs => refs.restaurants.openingSchedule,
   },
   {
      createController: RestroomClosed.createRestroomClosedController,
      getRefs: refs => refs.restrooms.closed,
   },
   {
      createController: RestroomOpen.createRestroomOpenController,
      getRefs: refs => refs.restrooms.open,
   },
   {
      createController: RestroomAlert.createRestroomAlertController,
      getRefs: refs => refs.restrooms.alert,
   },
   {
      createController: RemoveRestroomAlert.createRemoveRestroomAlertController,
      getRefs: refs => refs.restrooms.removeAlert,
   },
   {
      createController: GiftShopClosed.createGiftShopClosedController,
      getRefs: refs => refs.giftShops.closed,
   },
   {
      createController: GiftShopClosureOverride.createGiftShopClosureOverrideController,
      getRefs: refs => refs.giftShops.closureOverride,
   },
   {
      createController: GiftShopOpeningSchedule.createGiftShopOpeningScheduleController,
      getRefs: refs => refs.giftShops.openingSchedule,
   },
   {
      createController: AttractionClosed.createAttractionClosedController,
      getRefs: refs => refs.attractions.closed,
   },
   {
      createController: AttractionClosureOverride.createAttractionClosureOverrideController,
      getRefs: refs => refs.attractions.closureOverride,
   },
   {
      createController: AttractionOpeningSchedule.createAttractionOpeningScheduleController,
      getRefs: refs => refs.attractions.openingSchedule,
   },
   {
      createController: AttractionHoursSchedule.createAttractionHoursScheduleController,
      getRefs: refs => refs.attractions.hoursSchedule,
   },
   {
      createController: TransportationStationClosed.createTransportationStationClosedController,
      getRefs: refs => refs.transportation.stationClosed,
   },
   {
      createController: TransportationStationOpen.createTransportationStationOpenController,
      getRefs: refs => refs.transportation.stationOpen,
   },
   {
      createController: TransportationRoute.createTransportationRouteController,
      getRefs: refs => refs.transportation.route,
   },
   {
      createController: GuardiansTalkSchedule.createGuardiansTalkScheduleController,
      getRefs: refs => refs.guardiansTalks.schedule,
      getExtraOptions: ({ guardiansTalkScheduleLocationFilterController }) => ({
         talkLocationFilterController: guardiansTalkScheduleLocationFilterController,
      }),
   },
   {
      createController: EndGuardiansTalkSchedule.createEndGuardiansTalkScheduleController,
      getRefs: refs => refs.guardiansTalks.endSchedule,
      getExtraOptions: ({
         endGuardiansTalkScheduleLocationFilterController,
         guardiansTalkScheduleTimesFilterController,
      }) => ({
         talkLocationFilterController: endGuardiansTalkScheduleLocationFilterController,
         scheduleTimesFilterController: guardiansTalkScheduleTimesFilterController,
      }),
   },
   {
      createController: AddGuardiansTalkOccurrence.createAddGuardiansTalkOccurrenceController,
      getRefs: refs => refs.guardiansTalks.addOccurrence,
      getExtraOptions: ({
         addGuardiansTalkOccurrenceLocationFilterController,
      }) => ({
         talkLocationFilterController: addGuardiansTalkOccurrenceLocationFilterController,
      }),
   },
   {
      createController: CancelGuardiansTalkOccurrence.createCancelGuardiansTalkOccurrenceController,
      getRefs: refs => refs.guardiansTalks.cancelOccurrence,
      getExtraOptions: ({
         cancelGuardiansTalkOccurrenceLocationFilterController,
         cancelGuardiansTalkOccurrenceFilterController,
      }) => ({
         talkLocationFilterController: cancelGuardiansTalkOccurrenceLocationFilterController,
         occurrenceFilterController: cancelGuardiansTalkOccurrenceFilterController,
      }),
   },
   {
      createController: WildEncounterSchedule.createWildEncounterScheduleController,
      getRefs: refs => refs.wildEncounters.schedule,
   },
   {
      createController: EndWildEncounterSchedule.createEndWildEncounterScheduleController,
      getRefs: refs => refs.wildEncounters.endSchedule,
      getExtraOptions: ({ wildEncounterScheduleTimesFilterController }) => ({
         scheduleTimesFilterController: wildEncounterScheduleTimesFilterController,
      }),
   },
   {
      createController: CancelWildEncounterOccurrence.createCancelWildEncounterOccurrenceController,
      getRefs: refs => refs.wildEncounters.cancelOccurrence,
      getExtraOptions: ({ wildEncounterOccurrenceFilterController }) => ({
         occurrenceFilterController: wildEncounterOccurrenceFilterController,
      }),
   },
   {
      createController: DrinkingFountainsClosed.createDrinkingFountainsClosedController,
      getRefs: refs => refs.drinkingFountains.closed,
   },
   {
      createController: DrinkingFountainsOpen.createDrinkingFountainsOpenController,
      getRefs: refs => refs.drinkingFountains.open,
   },
   {
      createController: CreateEvent.createCreateEventController,
      getRefs: refs => refs.events.create,
   },
   {
      createController: CreateUpdate.createCreateUpdateController,
      getRefs: refs => refs.updates.create,
   },
   {
      createController: EndUpdate.createEndUpdateController,
      getRefs: refs => refs.updates.end,
   },
   {
      createController: EditUpdate.createEditUpdateController,
      getRefs: refs => refs.updates.edit,
   },
];

function initAnimalSpeciesAutocompletes(animals) {
   ANIMAL_SPECIES_AUTOCOMPLETE_KEYS.forEach(key => {
      const { speciesEl, speciesResultsEl, exhibitEl } = animals[key];

      AnimalSpeciesAutocomplete.createAnimalSpeciesAutocompleteController({
         inputEl: speciesEl,
         resultsEl: speciesResultsEl,
         exhibitEl,
      });
   });
}

function createControllerOptions({
   refs,
   activatePanel,
   getExtraOptions,
   specialControllers,
} = {}) {
   return {
      ...refs,
      activatePanel,
      ...(getExtraOptions ? getExtraOptions(specialControllers) : {}),
   };
}

function wireControllerBindings({
   refs,
   activatePanel,
   specialControllers,
} = {}) {
   CONTROLLER_BINDINGS.forEach(({ createController, getRefs, getExtraOptions }) => {
      createController(
         createControllerOptions({
            refs: getRefs(refs),
            activatePanel,
            getExtraOptions,
            specialControllers,
         })
      );
   });
}

export class Controllers {
   static createConsoleSpecialControllers({ guardiansTalks, wildEncounters }) {
      return {
         guardiansTalkScheduleLocationFilterController:
            GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
               locationEl: guardiansTalks.schedule.locationEl,
               talkNameEl: guardiansTalks.schedule.talkNameEl,
            }),
         endGuardiansTalkScheduleLocationFilterController:
            GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
               locationEl: guardiansTalks.endSchedule.locationEl,
               talkNameEl: guardiansTalks.endSchedule.talkNameEl,
            }),
         addGuardiansTalkOccurrenceLocationFilterController:
            GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
               locationEl: guardiansTalks.addOccurrence.locationEl,
               talkNameEl: guardiansTalks.addOccurrence.talkNameEl,
            }),
         cancelGuardiansTalkOccurrenceLocationFilterController:
            GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
               locationEl: guardiansTalks.cancelOccurrence.locationEl,
               talkNameEl: guardiansTalks.cancelOccurrence.talkNameEl,
            }),
         cancelGuardiansTalkOccurrenceFilterController:
            GuardiansTalkOccurrenceFilter.createGuardiansTalkOccurrenceFilterController({
               locationEl: guardiansTalks.cancelOccurrence.locationEl,
               talkNameEl: guardiansTalks.cancelOccurrence.talkNameEl,
               dateEl: guardiansTalks.cancelOccurrence.dateEl,
               timesEl: guardiansTalks.cancelOccurrence.timesEl,
            }),
         guardiansTalkScheduleTimesFilterController:
            GuardiansTalkScheduleTimesFilter.createGuardiansTalkScheduleTimesFilterController({
               locationEl: guardiansTalks.endSchedule.locationEl,
               talkNameEl: guardiansTalks.endSchedule.talkNameEl,
               timesEl: guardiansTalks.endSchedule.timesEl,
            }),
         wildEncounterOccurrenceFilterController:
            WildEncounterOccurrenceFilter.createWildEncounterOccurrenceFilterController({
               wildEncounterEl: wildEncounters.cancelOccurrence.wildEncounterEl,
               dateEl: wildEncounters.cancelOccurrence.dateEl,
               timesEl: wildEncounters.cancelOccurrence.timesEl,
            }),
         wildEncounterScheduleTimesFilterController:
            WildEncounterScheduleTimesFilter.createWildEncounterScheduleTimesFilterController({
               wildEncounterEl: wildEncounters.endSchedule.wildEncounterEl,
               timesEl: wildEncounters.endSchedule.timesEl,
            }),
      };
   }

   static wireConsoleOperationControllers({
   refs,
   activatePanel,
   guardiansTalkScheduleLocationFilterController,
   endGuardiansTalkScheduleLocationFilterController,
   addGuardiansTalkOccurrenceLocationFilterController,
   cancelGuardiansTalkOccurrenceLocationFilterController,
   cancelGuardiansTalkOccurrenceFilterController,
   guardiansTalkScheduleTimesFilterController,
   wildEncounterOccurrenceFilterController,
   wildEncounterScheduleTimesFilterController,
}) {
      initAnimalSpeciesAutocompletes(refs.animals);

      wireControllerBindings({
         refs,
         activatePanel,
         specialControllers: {
            guardiansTalkScheduleLocationFilterController,
            endGuardiansTalkScheduleLocationFilterController,
            addGuardiansTalkOccurrenceLocationFilterController,
            cancelGuardiansTalkOccurrenceLocationFilterController,
            cancelGuardiansTalkOccurrenceFilterController,
            guardiansTalkScheduleTimesFilterController,
            wildEncounterOccurrenceFilterController,
            wildEncounterScheduleTimesFilterController,
         },
      });
   }
}
