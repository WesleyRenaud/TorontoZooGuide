import { makeItemRow } from './components/itemRow.js';
import { RowPresentation } from './rowPresentation.js';
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

export class RowBuilders {
   static buildUniqueAnimals(animals = []) {
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

   static buildRows(
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

   static buildNamedRows(
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
      return RowBuilders.buildRows(items, {
         normalizeItem,
         prepareItems,
         buildRowProps: (item) => {
            const name = getName(item) || defaultName;
            const imageName = getImageName(item) || name;

            return {
               name,
               nameSuffix: getNameSuffix(item),
               imageSrc: RowPresentation.buildImageSrc(imageDirectory, imageName),
               metaLines: RowPresentation.buildMetaLines(getMetaLines(item)),
               alertLine: getAlertLine(item),
               ...RowPresentation.buildLinkRowProps(getLink(item)),
               ...(typeof extendRowProps === 'function' ? extendRowProps(item) : {}),
            };
         },
      });
   }
}
