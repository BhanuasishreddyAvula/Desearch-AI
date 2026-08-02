/**
 * Citation Intelligence Engine Data Models
 * Separates Source, Evidence, and Citation domain entities.
 */

export type ConfidenceLevel = 'High' | 'Medium' | 'Low';

export type SourceCategory =
  | 'Official Documentation'
  | 'Research Paper'
  | 'Government'
  | 'GitHub'
  | 'Engineering Blog'
  | 'Community Forum'
  | 'General Web';

export interface Source {
  id: string;
  title: string;
  url: string;
  domain: string;
  favicon?: string;
  category: SourceCategory;
  retrievedAt: string;
  qualityScore: number; // 0 - 100
  trustScore: ConfidenceLevel;
}

export interface Evidence {
  id: string;
  sourceId: string;
  snippet: string;
  startOffset?: number;
  endOffset?: number;
  retrievalPhase?: string;
  confidence: ConfidenceLevel;
}

export interface Citation {
  id: string;
  reportSectionId?: string;
  evidenceIds: string[];
  citationNumber: number;
  claimText?: string;
  confidence: ConfidenceLevel;
}
