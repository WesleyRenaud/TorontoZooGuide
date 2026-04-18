export function likelihoodToColor(likelihood) {
   const value = Math.max(0, Math.min(100, Number(likelihood) || 0));
   const colors = [
      '#7a0000', '#9c0d00', '#be1a00', '#e03f00', '#ff6500',
      '#ff7f00', '#ff9900', '#ffb300', '#ffcc33', '#ffff33',
      '#e0ff33', '#c4ff33', '#a8ff33', '#8cff33', '#70ff33',
      '#55cc33', '#3abb33', '#2eb33a', '#259933', '#1fa544',
   ];
   const index = Math.round((value / 100) * (colors.length - 1));

   return colors[index];
}
