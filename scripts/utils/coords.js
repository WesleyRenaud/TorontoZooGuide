export function coordKey(x, y) {
   const nx = Number(x);
   const ny = Number(y);
   return `${nx.toFixed(4)}|${ny.toFixed(4)}`;
}