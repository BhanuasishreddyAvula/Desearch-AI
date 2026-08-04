/**
 * Conversation Messages API Client
 * Fetches persistent conversation messages from the backend.
 * Messages are stored in the conversation_messages table (not session metadata).
 */

import { apiFetch } from './client';
import type { BaseResponse } from '../../types';

export interface ConversationMessage {
  id: string;
  session_id: string;
  role: 'user' | 'assistant';
  content: string;
  metadata: {
    pair_id?: string;
    title?: string;
    full_markdown?: string;
    sources_cited?: string[];
    word_count?: number;
    sections_count?: number;
  };
  created_at: string;
}

export interface ConversationMessagesListData {
  messages: ConversationMessage[];
  total: number;
}

export const conversationsApi = {
  /**
   * List all conversation messages for a session, ordered by created_at ASC.
   * Returns paired user + assistant messages that form the conversation.
   */
  listMessages: async (
    sessionId: string,
    signal?: AbortSignal
  ): Promise<ConversationMessage[]> => {
    const res = await apiFetch<BaseResponse<ConversationMessagesListData>>(
      `/api/v1/sessions/${sessionId}/messages`,
      { method: 'GET', signal }
    );
    return res.data?.messages || [];
  },
};
