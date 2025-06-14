export const formatSimilarity = (value: number): string => {
    return `${(value * 100).toFixed(1)}%`;
}

export function getHighestSimilarity(transformations: { similarity: number }[]): number {
    return Math.max(...transformations.map(t => t.similarity));
}

export function getHighestTransformation(transformations: { similarity: number }[]): any {
    const highest = getHighestSimilarity(transformations);
    return transformations.find(t => t.similarity === highest);
}
