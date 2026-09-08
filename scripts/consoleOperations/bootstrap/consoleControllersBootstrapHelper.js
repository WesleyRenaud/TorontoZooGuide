import { AnimalOffController } from '../animals/controllers/animalOffController.js';
import { AnimalOnController } from '../animals/controllers/animalOnController.js';
import { AnimalSpeciesController } from '../animals/controllers/animalSpeciesController.js';
import { AnimalViewingController } from '../animals/controllers/animalViewingController.js';
import { AnimalVisibilityController } from '../animals/controllers/animalVisibilityController.js';
import { RemoveViewingController } from '../animals/controllers/removeViewingController.js';
import { RemoveVisibilityController } from '../animals/controllers/removeVisibilityController.js';
import { AttractionClosureController } from '../attractions/controllers/attractionClosureController.js';
import { AttractionController } from '../attractions/controllers/attractionController.js';
import { AttractionHoursController } from '../attractions/controllers/attractionHoursController.js';
import { AttractionOpeningController } from '../attractions/controllers/attractionOpeningController.js';
import { DrinkingFountainsController } from '../drinkingFountains/controllers/drinkingFountainsController.js';
import { DrinkingFountainsOpenController } from '../drinkingFountains/controllers/drinkingFountainsOpenController.js';
import { EventController } from '../events/controllers/eventController.js';
import { ExhibitController } from '../exhibits/controllers/exhibitController.js';
import { ExhibitOpenController } from '../exhibits/controllers/exhibitOpenController.js';
import { GiftShopClosureController } from '../giftShops/controllers/giftShopClosureController.js';
import { GiftShopController } from '../giftShops/controllers/giftShopController.js';
import { GiftShopOpeningController } from '../giftShops/controllers/giftShopOpeningController.js';
import { AddGuardiansTalkController } from '../guardiansTalks/controllers/addGuardiansTalkController.js';
import { CancelGuardiansTalkController } from '../guardiansTalks/controllers/cancelGuardiansTalkController.js';
import { EndGuardiansTalkController } from '../guardiansTalks/controllers/endGuardiansTalkController.js';
import { GuardiansTalkController } from '../guardiansTalks/controllers/guardiansTalkController.js';
import { RestaurantClosureController } from '../restaurants/controllers/restaurantClosureController.js';
import { RestaurantController } from '../restaurants/controllers/restaurantController.js';
import { RestaurantOpeningController } from '../restaurants/controllers/restaurantOpeningController.js';
import { RemoveRestroomController } from '../restrooms/controllers/removeRestroomController.js';
import { RestroomClosedController } from '../restrooms/controllers/restroomClosedController.js';
import { RestroomController } from '../restrooms/controllers/restroomController.js';
import { RestroomOpenController } from '../restrooms/controllers/restroomOpenController.js';
import { TransportationRouteController } from '../transportation/controllers/transportationRouteController.js';
import { TransportationStationController } from '../transportation/controllers/transportationStationController.js';
import { TransportationStationOpenController } from '../transportation/controllers/transportationStationOpenController.js';
import { UpdateCreateController } from '../updates/controllers/updateCreateController.js';
import { UpdateEditController } from '../updates/controllers/updateEditController.js';
import { UpdateEndController } from '../updates/controllers/updateEndController.js';
import { CancelWildEncounterController } from '../wildEncounters/controllers/cancelWildEncounterController.js';
import { EndWildEncounterController } from '../wildEncounters/controllers/endWildEncounterController.js';
import { WildEncounterController } from '../wildEncounters/controllers/wildEncounterController.js';

export class ConsoleControllersBootstrapHelper {
   static ANIMAL_SPECIES_AUTOCOMPLETE_KEYS = [
   'offDisplay',
   'onDisplay',
   'visibilitySchedule',
   'removeVisibilitySchedule',
   'viewingAlert',
   'removeViewingAlert',
];
   static CONTROLLER_BINDINGS = [
   {
      createController: AnimalOffController.createAnimalOffDisplayController,
      getRefs: refs => refs.animals.offDisplay,
   },
   {
      createController: AnimalOnController.createAnimalOnDisplayController,
      getRefs: refs => refs.animals.onDisplay,
   },
   {
      createController: AnimalVisibilityController.createAnimalVisibilityScheduleController,
      getRefs: refs => refs.animals.visibilitySchedule,
   },
   {
      createController: RemoveVisibilityController.createRemoveVisibilityScheduleController,
      getRefs: refs => refs.animals.removeVisibilitySchedule,
   },
   {
      createController: AnimalViewingController.createAnimalViewingAlertController,
      getRefs: refs => refs.animals.viewingAlert,
   },
   {
      createController: RemoveViewingController.createRemoveViewingAlertController,
      getRefs: refs => refs.animals.removeViewingAlert,
   },
   {
      createController: ExhibitController.createExhibitClosedController,
      getRefs: refs => refs.exhibits.closed,
   },
   {
      createController: ExhibitOpenController.createExhibitOpenController,
      getRefs: refs => refs.exhibits.open,
   },
   {
      createController: RestaurantController.createRestaurantClosedController,
      getRefs: refs => refs.restaurants.closed,
   },
   {
      createController: RestaurantClosureController.createRestaurantClosureOverrideController,
      getRefs: refs => refs.restaurants.closureOverride,
   },
   {
      createController: RestaurantOpeningController.createRestaurantOpeningScheduleController,
      getRefs: refs => refs.restaurants.openingSchedule,
   },
   {
      createController: RestroomClosedController.createRestroomClosedController,
      getRefs: refs => refs.restrooms.closed,
   },
   {
      createController: RestroomOpenController.createRestroomOpenController,
      getRefs: refs => refs.restrooms.open,
   },
   {
      createController: RestroomController.createRestroomAlertController,
      getRefs: refs => refs.restrooms.alert,
   },
   {
      createController: RemoveRestroomController.createRemoveRestroomAlertController,
      getRefs: refs => refs.restrooms.removeAlert,
   },
   {
      createController: GiftShopController.createGiftShopClosedController,
      getRefs: refs => refs.giftShops.closed,
   },
   {
      createController: GiftShopClosureController.createGiftShopClosureOverrideController,
      getRefs: refs => refs.giftShops.closureOverride,
   },
   {
      createController: GiftShopOpeningController.createGiftShopOpeningScheduleController,
      getRefs: refs => refs.giftShops.openingSchedule,
   },
   {
      createController: AttractionController.createAttractionClosedController,
      getRefs: refs => refs.attractions.closed,
   },
   {
      createController: AttractionClosureController.createAttractionClosureOverrideController,
      getRefs: refs => refs.attractions.closureOverride,
   },
   {
      createController: AttractionOpeningController.createAttractionOpeningScheduleController,
      getRefs: refs => refs.attractions.openingSchedule,
   },
   {
      createController: AttractionHoursController.createAttractionHoursScheduleController,
      getRefs: refs => refs.attractions.hoursSchedule,
   },
   {
      createController: TransportationStationController.createTransportationStationClosedController,
      getRefs: refs => refs.transportation.stationClosed,
   },
   {
      createController: TransportationStationOpenController.createTransportationStationOpenController,
      getRefs: refs => refs.transportation.stationOpen,
   },
   {
      createController: TransportationRouteController.createTransportationRouteController,
      getRefs: refs => refs.transportation.route,
   },
   {
      createController: GuardiansTalkController.createGuardiansTalkScheduleController,
      getRefs: refs => refs.guardiansTalks.schedule,
      getExtraOptions: ({ guardiansTalkScheduleLocationFilterController }) => ({
         talkLocationFilterController: guardiansTalkScheduleLocationFilterController,
      }),
   },
   {
      createController: EndGuardiansTalkController.createEndGuardiansTalkScheduleController,
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
      createController: AddGuardiansTalkController.createAddGuardiansTalkOccurrenceController,
      getRefs: refs => refs.guardiansTalks.addOccurrence,
      getExtraOptions: ({
         addGuardiansTalkOccurrenceLocationFilterController,
      }) => ({
         talkLocationFilterController: addGuardiansTalkOccurrenceLocationFilterController,
      }),
   },
   {
      createController: CancelGuardiansTalkController.createCancelGuardiansTalkOccurrenceController,
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
      createController: WildEncounterController.createWildEncounterScheduleController,
      getRefs: refs => refs.wildEncounters.schedule,
   },
   {
      createController: EndWildEncounterController.createEndWildEncounterScheduleController,
      getRefs: refs => refs.wildEncounters.endSchedule,
      getExtraOptions: ({ wildEncounterScheduleTimesFilterController }) => ({
         scheduleTimesFilterController: wildEncounterScheduleTimesFilterController,
      }),
   },
   {
      createController: CancelWildEncounterController.createCancelWildEncounterOccurrenceController,
      getRefs: refs => refs.wildEncounters.cancelOccurrence,
      getExtraOptions: ({ wildEncounterOccurrenceFilterController }) => ({
         occurrenceFilterController: wildEncounterOccurrenceFilterController,
      }),
   },
   {
      createController: DrinkingFountainsController.createDrinkingFountainsClosedController,
      getRefs: refs => refs.drinkingFountains.closed,
   },
   {
      createController: DrinkingFountainsOpenController.createDrinkingFountainsOpenController,
      getRefs: refs => refs.drinkingFountains.open,
   },
   {
      createController: EventController.createCreateEventController,
      getRefs: refs => refs.events.create,
   },
   {
      createController: UpdateCreateController.createCreateUpdateController,
      getRefs: refs => refs.updates.create,
   },
   {
      createController: UpdateEndController.createEndUpdateController,
      getRefs: refs => refs.updates.end,
   },
   {
      createController: UpdateEditController.createEditUpdateController,
      getRefs: refs => refs.updates.edit,
   },
];

   static initAnimalSpeciesAutocompletes(animals) {
      ConsoleControllersBootstrapHelper.ANIMAL_SPECIES_AUTOCOMPLETE_KEYS.forEach(key => {
         const { speciesEl, speciesResultsEl, exhibitEl } = animals[key];

         AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
            inputEl: speciesEl,
            resultsEl: speciesResultsEl,
            exhibitEl,
         });
      });
   }

   static createControllerOptions({
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

   static wireControllerBindings({
      refs,
      activatePanel,
      specialControllers,
   } = {}) {
      ConsoleControllersBootstrapHelper.CONTROLLER_BINDINGS.forEach(({ createController, getRefs, getExtraOptions }) => {
         createController(
            ConsoleControllersBootstrapHelper.createControllerOptions({
               refs: getRefs(refs),
               activatePanel,
               getExtraOptions,
               specialControllers,
            })
         );
      });
   }
}
