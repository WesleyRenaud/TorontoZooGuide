import { makeItemRow } from './components/itemRow.js';
import {
   buildImageSrc,
   buildLinkRowProps,
   buildMetaLines,
} from './rowPresentation.js';
import { SpeciesExhibitKey } from '../speciesExhibitKey.js';

function normalizeItems(items = [], normalizeItem) {
   return items.map((item) => normalizeItem(item));
}

function maxStoredLikelihood(...values) {
   const likelihoods = values
      .map((value) => (
         value == null || value === '' ? NaN : Number(value)
      ))
      .filter((value) => Number.isFinite(value));

   if (!likelihoods.length) {
      return null;
   }

   return Math.max(...likelihoods);
}

export function buildUniqueAnimals(animals = []) {
   return SpeciesExhibitKey.buildUniqueSpeciesExhibitEntries(animals, {
      buildKey: SpeciesExhibitKey.buildAnimalViewingSpotKey,
      mergeAnimals: (existing, animal) => ({
         ...existing,
         likelihood: maxStoredLikelihood(existing.likelihood, animal.likelihood),
         old_likelihood: maxStoredLikelihood(
            existing.old_likelihood,
            animal.old_likelihood
         ),
         likelihoodBefore: maxStoredLikelihood(
            existing.likelihoodBefore,
            animal.likelihoodBefore
         ),
         likelihoodAfter: maxStoredLikelihood(
            existing.likelihoodAfter,
            animal.likelihoodAfter
         ),
      }),
      requireExhibit: false,
   }).map(({ item }) => item);
}

export function buildRows(
   items = [],
   {
      normalizeItem,
      prepareItems = (normalizedItems) => normalizedItems,
      buildRowProps,
   } = {}
) {
   const preparedItems = prepareItems(
      normalizeItems(items, normalizeItem)
   );

   return preparedItems.map((item) => makeItemRow(buildRowProps(item)));
}

export function buildNamedRows(
   items = [],
   {
      normalizeItem,
      prepareItems = (normalizedItems) => normalizedItems,
      defaultName,
      imageDirectory,
      getName,
      getImageName = getName,
      getNameSuffix = () => '',
      getMetaLines = () => [],
      getAlertLine = () => '',
      getLink = () => null,
      extendRowProps = null,
   } = {}
) {
   return buildRows(items, {
      normalizeItem,
      prepareItems,
      buildRowProps: (item) => {
         const name = getName(item) || defaultName;
         const imageName = getImageName(item) || name;

         return {
            name,
            nameSuffix: getNameSuffix(item),
            imageSrc: buildImageSrc(imageDirectory, imageName),
            metaLines: buildMetaLines(getMetaLines(item)),
            alertLine: getAlertLine(item),
            ...buildLinkRowProps(getLink(item)),
            ...(typeof extendRowProps === 'function' ? extendRowProps(item) : {}),
         };
      },
   });
}
