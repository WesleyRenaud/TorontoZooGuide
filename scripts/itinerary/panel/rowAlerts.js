function toPercent(value) {
   if (typeof value !== 'number' || !Number.isFinite(value)) return null;
   return Math.round(value > 1 ? value : value * 100);
}

function getLikelihoodPair(animal) {
   const beforeRaw = animal?.likelihoodBefore;
   const afterRaw = animal?.likelihoodAfter;

   const before = toPercent(Number(beforeRaw));
   const after = toPercent(Number(afterRaw));

   return { before, after };
}

function buildAnimalRemovalReasonLine(animal) {
   const reason = animal.removalReason ?? '';

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
   const reason = attraction.removalReason ?? '';

   if (!reason) return '';

   return `Not available on this date: ${reason}`;
}

export function buildGuardiansRemovalReasonLine(guardiansTalk) {
   const reason = guardiansTalk.removalReason ?? '';

   if (!reason) return '';

   return `Not available on this date: ${reason}`;
}

export function buildWildRemovalReasonLine(wildEncounter) {
   const reason = wildEncounter.removalReason ?? '';

   if (!reason) return '';

   return `Not available on this date: ${reason}`;
}
