function toPercent(value) {
   if (typeof value !== 'number' || !Number.isFinite(value)) return null;
   return Math.round(value > 1 ? value : value * 100);
}

function getLikelihoodPair(animal) {
   const beforeRaw =
      animal?.likelihoodBefore ??
      animal?.likelihood_before ??
      animal?.previousLikelihood ??
      animal?.previous_likelihood ??
      animal?.oldLikelihood ??
      animal?.old_likelihood;

   const afterRaw =
      animal?.likelihoodAfter ??
      animal?.likelihood_after ??
      animal?.currentLikelihood ??
      animal?.current_likelihood ??
      animal?.newLikelihood ??
      animal?.new_likelihood ??
      animal?.likelihood ??
      animal?.LIKELIHOOD;

   const before = toPercent(Number(beforeRaw));
   const after = toPercent(Number(afterRaw));

   return { before, after };
}

function buildAnimalRemovalReasonLine(animal) {
   const reason =
      animal.removalReason ??
      animal.removal_reason ??
      animal.off_display_message ??
      animal.OFF_DISPLAY_MESSAGE ??
      animal.display_message ??
      animal.DISPLAY_MESSAGE ??
      '';

   if (!reason) return '';

   return `Unavailable: ${reason}`;
}

function buildAnimalVisibilityChange(animal) {
   const { before, after } = getLikelihoodPair(animal);

   if (before == null || after == null || before === after) {
      return {
         line: '',
         tone: 'default',
      };
   }

   if (after < before) {
      return {
         line: `Projected visibility changed from ${before}% to ${after}% on your new date.`,
         tone: 'default',
      };
   }

   return {
      line: `Projected visibility changed from ${before}% to ${after}% on your new date.`,
      tone: 'positive',
   };
}

export function buildAnimalAlert(animal) {
   const removalLine = buildAnimalRemovalReasonLine(animal);

   if (removalLine) {
      return {
         line: removalLine,
         tone: 'default',
      };
   }

   return buildAnimalVisibilityChange(animal);
}

export function buildAttractionRemovalReasonLine(attraction) {
   const reason =
      attraction.removalReason ??
      attraction.removal_reason ??
      attraction.closed_message ??
      attraction.CLOSED_MESSAGE ??
      attraction.display_message ??
      attraction.DISPLAY_MESSAGE ??
      '';

   if (!reason) return '';

   return `Not available on this date: ${reason}`;
}

export function buildGuardiansRemovalReasonLine(guardiansTalk) {
   const reason =
      guardiansTalk.removalReason ??
      guardiansTalk.removal_reason ??
      guardiansTalk.unavailable_message ??
      guardiansTalk.UNAVAILABLE_MESSAGE ??
      guardiansTalk.display_message ??
      guardiansTalk.DISPLAY_MESSAGE ??
      '';

   if (!reason) return '';

   return `Not available on this date: ${reason}`;
}

export function buildWildRemovalReasonLine(wildEncounter) {
   const reason =
      wildEncounter.removalReason ??
      wildEncounter.removal_reason ??
      wildEncounter.unavailable_message ??
      wildEncounter.UNAVAILABLE_MESSAGE ??
      wildEncounter.display_message ??
      wildEncounter.DISPLAY_MESSAGE ??
      '';

   if (!reason) return '';

   return `Not available on this date: ${reason}`;
}