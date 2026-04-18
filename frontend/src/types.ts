/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export type Screen = 'dashboard' | 'intel' | 'emails' | 'talent' | 'leads' | 'cs-bot' | 'brief';

export interface Lead {
  id: string;
  name: string;
  role: string;
  company: string;
  avatar: string;
  fitScore: number;
  description: string;
  tags: string[];
}

export interface EmailDraft {
  id: string;
  recipient: string;
  type: string;
  subject: string;
  preview: string;
}

export interface Metric {
  label: string;
  value: string;
  change?: string;
  status?: string;
  icon: 'trending_up' | 'schedule' | 'badge' | 'security';
}
