/**
 * Splits paragraph text into discrete sentences for sentence-by-sentence progressive streaming.
 * Preserves sentence terminal punctuation (. ! ?).
 */
export function splitIntoSentences(text: string): string[] {
  if (!text) return [];

  // Match sentences ending in . ! or ? followed by whitespace or end of line
  const sentenceRegex = /[^.!?]+[.!?]+(\s+|$)|[^.!?]+$/g;
  const matches = text.match(sentenceRegex);

  if (!matches) {
    return [text];
  }

  return matches.map((s) => s.trim()).filter((s) => s.length > 0);
}
