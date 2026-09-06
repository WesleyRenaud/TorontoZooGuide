import { AnimalSelector } from '../selectors/animalSelector.js';
import { AttractionSelector } from '../selectors/attractionSelector.js';
import { GuardiansTalkSelector } from '../selectors/guardiansTalkSelector.js';
import { RegionSelector } from '../selectors/regionSelector.js';
import { TransportationSelector } from '../selectors/transportationSelector.js';
import { WildEncounterSelector } from '../selectors/wildEncounterSelector.js';
import { WizardStepConfigs } from './wizardStepConfigs.js';

const WIZARD_SELECTION_STEP_FACTORIES = Object.freeze({
   transportations: TransportationSelector.createItineraryTransportationSelectorController,
   wildEncounters: WildEncounterSelector.createItineraryWildEncounterSelectorController,
   guardiansTalks: GuardiansTalkSelector.createItineraryGuardiansTalkSelectorController,
   attractions: AttractionSelector.createItineraryAttractionSelectorController,
   animals: AnimalSelector.createItineraryAnimalSelectorController,
   regions: RegionSelector.createItineraryRegionSelectorController,
});

export class WizardSelectionStepFactories {
   static buildWizardSelectionStepConfigs(
      definitions = WizardStepConfigs.WIZARD_SELECTION_STEP_DEFINITIONS,
      factoriesByStepKey = WIZARD_SELECTION_STEP_FACTORIES
   ) {
      return definitions.map((definition) => ({
         ...definition,
         factory: factoriesByStepKey[definition.stepKey],
      }));
   }
}
