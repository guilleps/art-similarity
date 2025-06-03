export function formatSimilarity(similarity: number): string {
    return (similarity * 100).toFixed(1) + '%';
}

export function getHighestSimilarity(transformations: { similarity: number }[]): number {
    return Math.max(...transformations.map(t => t.similarity));
}

export function getHighestTransformation(transformations: { similarity: number }[]): any {
    const highest = getHighestSimilarity(transformations);
    return transformations.find(t => t.similarity === highest);
}
