export class WizardControllerHelpers {
   static async loadDefaultSelectionStepConfigs() {
      const { WizardSelectionStepFactories } = await import(
         './wizardSelectionStepFactories.js'
      );

      return WizardSelectionStepFactories.buildWizardSelectionStepConfigs();
   }

   static clearWizard(mountEl) {
      mountEl?.replaceChildren();
   }

   static closeWizard(mountEl) {
      WizardControllerHelpers.clearWizard(mountEl);
   }
}
