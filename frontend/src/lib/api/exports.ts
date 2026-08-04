import { API_BASE_URL, ApiClientError } from './client';
import type { ExportFormat } from '../../types';

export const exportsApi = {
  getExportUrl: (sessionId: string, format: ExportFormat): string => {
    return `${API_BASE_URL}/api/v1/reports/${sessionId}/export?format=${format}`;
  },

  downloadExport: async (sessionId: string, format: ExportFormat, signal?: AbortSignal): Promise<Blob> => {
    const url = exportsApi.getExportUrl(sessionId, format);
    try {
      const response = await fetch(url, { method: 'GET', signal });
      if (!response.ok) {
        throw new ApiClientError(
          `Export failed: ${response.statusText}`,
          response.status
        );
      }
      return await response.blob();
    } catch (error) {
      if (error instanceof ApiClientError) throw error;
      throw new ApiClientError(
        error instanceof Error ? error.message : 'Export download failed',
        500
      );
    }
  },
};
