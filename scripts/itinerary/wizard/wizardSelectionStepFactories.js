import { createItineraryAnimalSelectorController } from '../selectors/animalSelector.js';
import { createItineraryAttractionSelectorController } from '../selectors/attractionSelector.js';
import { createItineraryGuardiansTalkSelectorController } from '../selectors/guardiansTalkSelector.js';
import { createItineraryRegionSelectorController } from '../selectors/regionSelector.js';
import { createItineraryWildEncounterSelectorController } from '../selectors/wildEncounterSelector.js';
import { WIZARD_SELECTION_STEP_DEFINITIONS } from './wizardStepConfigs.js';

const WIZARD_SELECTION_STEP_FACTORIES = Object.freeze({
   wildEncounters: createItineraryWildEncounterSelectorController,
   guardiansTalks: createItineraryGuardiansTalkSelectorController,
   attractions: createItineraryAttractionSelectorController,
   animals: createItineraryAnimalSelectorController,
   regions: createItineraryRegionSelectorController,
});

export function buildWizardSelectionStepConfigs(
   definitions = WIZARD_SELECTION_STEP_DEFINITIONS,
   factoriesByStepKey = WIZARD_SELECTION_STEP_FACTORIES
) {
   return definitions.map((definition) => ({
      ...definition,
      factory: factoriesByStepKey[definition.stepKey],
   }));
}
