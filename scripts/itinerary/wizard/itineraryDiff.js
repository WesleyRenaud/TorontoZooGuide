function buildKey(item, fields = []) {
   if (typeof item === 'string') {
      return item.trim().toLowerCase();
   }

   for (const field of fields) {
      const value = item?.[field];
      if (typeof value === 'string' && value.trim()) {
         return value.trim().toLowerCase();
      }
   }

   return '';
}

function findRemovedItems(previousItems, validatedItems, fields = []) {
   const validatedKeys = new Set(
      validatedItems
         .map(item => buildKey(item, fields))
         .filter(Boolean)
   );

   return previousItems.filter(item => {
      const key = buildKey(item, fields);
      return key && !validatedKeys.has(key);
   });
}

function getLikelihoodValue(animal) {
   const raw =
      animal?.likelihood ??
      animal?.LIKELIHOOD ??
      animal?.likelihood_value ??
      animal?.LIKELIHOOD_VALUE ??
      null;

   const value = Number(raw);
   return Number.isFinite(value) ? value : null;
}

function toNormalizedLikelihood(value) {
   if (typeof value !== 'number' || !Number.isFinite(value)) return null;
   return value > 1 ? value / 100 : value;
}

function getBestAnimalsBySpecies(animals = []) {
   const bestByKey = new Map();

   animals.forEach((animal) => {
      const key = buildKey(animal, ['species', 'name']);
      if (!key) return;

      const likelihood = toNormalizedLikelihood(getLikelihoodValue(animal));
      const currentBest = bestByKey.get(key);
      const currentBestLikelihood = currentBest == null
         ? null
         : toNormalizedLikelihood(getLikelihoodValue(currentBest));

      if (currentBest == null) {
         bestByKey.set(key, animal);
         return;
      }

      if (likelihood == null) {
         return;
      }

      if (currentBestLikelihood == null || likelihood > currentBestLikelihood) {
         bestByKey.set(key, animal);
      }
   });

   return bestByKey;
}

function findReducedVisibilityAnimals(
   previousAnimals,
   validatedAnimals,
   removedAnimals = [],
   minDrop = 0.2
) {
   const previousByKey = getBestAnimalsBySpecies(previousAnimals);
   const validatedByKey = getBestAnimalsBySpecies(validatedAnimals);

   const removedKeys = new Set(
      removedAnimals
         .map(animal => buildKey(animal, ['species', 'name']))
         .filter(Boolean)
   );

   return Array.from(previousByKey.entries())
      .map(([key, previousAnimal]) => {
         if (removedKeys.has(key)) return null;

         const validatedAnimal = validatedByKey.get(key);
         if (!validatedAnimal) return null;

         const before = toNormalizedLikelihood(getLikelihoodValue(previousAnimal));
         const after = toNormalizedLikelihood(getLikelihoodValue(validatedAnimal));

         if (before == null || after == null) return null;
         if (after >= before) return null;
         if ((before - after) < minDrop) return null;

         return {
            ...validatedAnimal,
            likelihoodBefore: before,
            likelihoodAfter: after,
         };
      })
      .filter(Boolean);
}

function findImprovedVisibilityAnimals(
   previousAnimals,
   validatedAnimals,
   removedAnimals = [],
   minIncrease = 0.2
) {
   const previousByKey = getBestAnimalsBySpecies(previousAnimals);
   const validatedByKey = getBestAnimalsBySpecies(validatedAnimals);

   const removedKeys = new Set(
      removedAnimals
         .map(animal => buildKey(animal, ['species', 'name']))
         .filter(Boolean)
   );

   return Array.from(previousByKey.entries())
      .map(([key, previousAnimal]) => {
         if (removedKeys.has(key)) return null;

         const validatedAnimal = validatedByKey.get(key);
         if (!validatedAnimal) return null;

         const before = toNormalizedLikelihood(getLikelihoodValue(previousAnimal));
         const after = toNormalizedLikelihood(getLikelihoodValue(validatedAnimal));

         if (before == null || after == null) return null;
         if (after <= before) return null;
         if ((after - before) < minIncrease) return null;

         return {
            ...validatedAnimal,
            likelihoodBefore: before,
            likelihoodAfter: after,
         };
      })
      .filter(Boolean);
}

export function buildRemovedItems(previous, validated, backendRemoved = {}) {
   return {
      animals: Array.isArray(backendRemoved?.animals)
         ? backendRemoved.animals
         : findRemovedItems(previous.animals, validated.animals, ['species', 'name']),
      attractions: Array.isArray(backendRemoved?.attractions)
         ? backendRemoved.attractions
         : findRemovedItems(previous.attractions, validated.attractions, ['name']),
      guardiansTalks: Array.isArray(backendRemoved?.guardiansTalks)
         ? backendRemoved.guardiansTalks
         : findRemovedItems(previous.guardiansTalks, validated.guardiansTalks, ['name']),
      wildEncounters: Array.isArray(backendRemoved?.wildEncounters)
         ? backendRemoved.wildEncounters
         : findRemovedItems(previous.wildEncounters, validated.wildEncounters, ['name']),
   };
}

export function buildReducedVisibility(previous, validated, removed) {
   return {
      animals: findReducedVisibilityAnimals(
         previous.animals,
         validated.animals,
         removed.animals,
         0.2
      ),
   };
}

export function buildImprovedVisibility(previous, validated, removed) {
   return {
      animals: findImprovedVisibilityAnimals(
         previous.animals,
         validated.animals,
         removed.animals,
         0.2
      ),
   };
}