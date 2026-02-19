import { animalRenderer } from './renderers/animals.js';
import { pavilionRenderer } from './renderers/pavilions.js';

export const TYPE_REGISTRY = {
   animal: animalRenderer,
   pavilion: pavilionRenderer,
};

export function getRendererForItem(item) {
   const key = String(item?.type || '').toLowerCase();
   return TYPE_REGISTRY[key] ?? TYPE_REGISTRY.animal;
}