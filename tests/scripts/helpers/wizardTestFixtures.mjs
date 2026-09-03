export function createStubStepController(stepKey, shownSteps) {
   return {
      show() {
         shownSteps.push(stepKey);
      },
      getSelectionSnapshot: async () => [],
      shouldSkipClosingSelectionSync: () => true,
   };
}

export function syncedSelection() {
   return [{ species: 'African Lion', exhibit: 'Africa Savanna' }];
}
