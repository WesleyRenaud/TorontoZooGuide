import { createItineraryAnimalSelectorController } from '../selectors/animalSelector.js';
import { createItineraryAttractionSelectorController } from '../selectors/attractionSelector.js';
import { createItineraryGuardiansTalkSelectorController } from '../selectors/guardiansTalkSelector.js';
import { createItineraryRegionSelectorController } from '../selectors/regionSelector.js';
import { createItineraryTransportationSelectorController } from '../selectors/transportationSelector.js';
import { createItineraryWildEncounterSelectorController } from '../selectors/wildEncounterSelector.js';
import { WizardStepConfigs } from './wizardStepConfigs.js';

const WIZARD_SELECTION_STEP_FACTORIES = Object.freeze({
   transportations: createItineraryTransportationSelectorController,
   wildEncounters: createItineraryWildEncounterSelectorController,
   guardiansTalks: createItineraryGuardiansTalkSelectorController,
   attractions: createItineraryAttractionSelectorController,
   animals: createItineraryAnimalSelectorController,
   regions: createItineraryRegionSelectorController,
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
